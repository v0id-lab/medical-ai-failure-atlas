#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "data" / "clinical_state_language_v0_1_20260625.schema.json"
DEFAULT_INPUT = ROOT / "data" / "clinical_state_language_synthetic_fixture_v0_1_20260625.jsonl"


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{display_path(path)}: invalid JSON: {error}") from error


def load_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        records: list[dict[str, Any]] = []
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{display_path(path)} line {line_number}: invalid JSON: {error}"
                ) from error
            if not isinstance(item, dict):
                raise ValueError(f"{display_path(path)} line {line_number}: expected object")
            records.append(item)
        return records

    payload = load_json(path)
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list):
        bad_indexes = [
            str(index)
            for index, item in enumerate(payload, 1)
            if not isinstance(item, dict)
        ]
        if bad_indexes:
            raise ValueError(
                f"{display_path(path)}: non object records at indexes {', '.join(bad_indexes)}"
            )
        return payload
    raise ValueError(f"{display_path(path)}: expected object, array, or JSONL records")


def compact_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_array(value: Any) -> Any:
    if not isinstance(value, list):
        return value

    normalized: list[Any] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str):
            normalized.append(item)
            continue
        compacted = compact_text(item)
        if not compacted or compacted in seen:
            continue
        seen.add(compacted)
        normalized.append(compacted)
    return normalized


def normalize_record(record: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    normalized: dict[str, Any] = {}

    for field, details in properties.items():
        if field not in record:
            continue
        value = record[field]
        expected_type = details.get("type") if isinstance(details, dict) else None
        if expected_type == "string" and isinstance(value, str):
            value = compact_text(value)
        elif expected_type == "array":
            value = normalize_array(value)
        normalized[field] = value

    for field in sorted(set(record) - set(properties)):
        normalized[field] = record[field]

    return normalized


def record_label(record: dict[str, Any], index: int) -> str:
    state_id = record.get("state_id")
    if isinstance(state_id, str) and state_id.strip():
        return compact_text(state_id)
    return f"record {index}"


def validate_schema_shape(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("type") != "object":
        errors.append("schema root type must be object")
    if schema.get("additionalProperties") is not False:
        errors.append("schema must set additionalProperties to false")
    if not isinstance(schema.get("properties"), dict):
        errors.append("schema properties must be an object")
    if not isinstance(schema.get("required"), list):
        errors.append("schema required must be a list")
    return errors


def validate_record(record: dict[str, Any], schema: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    label = record_label(record, index)
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    if not isinstance(properties, dict) or not isinstance(required, list):
        return [f"{label}: schema is not usable"]

    extra_fields = sorted(set(record) - set(properties))
    if extra_fields:
        errors.append(f"{label}: unexpected fields: {', '.join(extra_fields)}")

    missing_fields = [field for field in required if field not in record]
    if missing_fields:
        errors.append(f"{label}: missing required fields: {', '.join(missing_fields)}")

    for field, details in properties.items():
        if field not in record or not isinstance(details, dict):
            continue
        expected_type = details.get("type")
        value = record[field]

        if expected_type == "string":
            if not isinstance(value, str):
                errors.append(f"{label}.{field}: expected string")
            elif not value:
                errors.append(f"{label}.{field}: cannot be empty")
        elif expected_type == "boolean":
            if type(value) is not bool:
                errors.append(f"{label}.{field}: expected boolean")
        elif expected_type == "array":
            if not isinstance(value, list):
                errors.append(f"{label}.{field}: expected array")
                continue
            for item_index, item in enumerate(value, 1):
                if not isinstance(item, str):
                    errors.append(f"{label}.{field}[{item_index}]: expected string")
                elif not item:
                    errors.append(f"{label}.{field}[{item_index}]: cannot be empty")

    if record.get("synthetic_only") is not True:
        errors.append(f"{label}.synthetic_only: must be true")
    if record.get("patient_data_used") is not False:
        errors.append(f"{label}.patient_data_used: must be false")
    if record.get("clinical_use_allowed") is not False:
        errors.append(f"{label}.clinical_use_allowed: must be false")
    if record.get("missing_data") == []:
        errors.append(f"{label}.missing_data: must name at least one missing item")
    if record.get("source_support_needed") == []:
        errors.append(f"{label}.source_support_needed: must name at least one support need")

    return errors


def canonical_jsonl(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    return "\n".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        for record in records
    ) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and normalize Clinical State Language v0.1 records."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="JSON, JSON array, or JSONL file with clinical state records.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Clinical State Language JSON schema.",
    )
    parser.add_argument(
        "--normalized-output",
        type=Path,
        help="Optional path to write canonical normalized JSONL.",
    )
    parser.add_argument(
        "--check-normalized",
        type=Path,
        help="Optional canonical JSONL file that must match the normalized records.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []

    try:
        schema = load_json(args.schema)
    except Exception as error:  # noqa: BLE001
        schema = {}
        errors.append(str(error))

    if isinstance(schema, dict):
        errors.extend(validate_schema_shape(schema))
    else:
        errors.append(f"{display_path(args.schema)}: expected schema object")
        schema = {}

    try:
        records = load_records(args.input)
    except Exception as error:  # noqa: BLE001
        records = []
        errors.append(str(error))

    if not records:
        errors.append(f"{display_path(args.input)}: no records found")

    normalized_records = [
        normalize_record(record, schema)
        for record in records
    ]

    for index, record in enumerate(normalized_records, 1):
        errors.extend(validate_record(record, schema, index))

    normalized_text = canonical_jsonl(normalized_records)

    if args.check_normalized:
        try:
            expected = args.check_normalized.read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"{display_path(args.check_normalized)}: cannot read: {error}")
        else:
            if expected != normalized_text:
                errors.append(f"{display_path(args.check_normalized)}: normalized output mismatch")

    if errors:
        print("FAIL Clinical State Language validation")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.normalized_output:
        args.normalized_output.parent.mkdir(parents=True, exist_ok=True)
        args.normalized_output.write_text(normalized_text, encoding="utf-8")

    digest = hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()
    print("PASS Clinical State Language validation")
    print(f"schema={display_path(args.schema)}")
    print(f"input={display_path(args.input)}")
    print(f"records={len(normalized_records)}")
    print(f"normalized_sha256={digest}")
    if args.check_normalized:
        print(f"checked_normalized={display_path(args.check_normalized)}")
    if args.normalized_output:
        print(f"normalized_output={display_path(args.normalized_output)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
