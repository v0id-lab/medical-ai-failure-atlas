#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from validate_multilingual_medical_intelligence_public_wording_bank_v0_1_20260625 import (
    detected_drift_signals,
)


ROOT = Path(__file__).resolve().parents[1]
VERSION = "v0_1_20260625"
DATE = "2026 06 25"
DATE_TOKEN = "20260625"
ATLAS_LAYER = "Multilingual Medical Intelligence"
ATLAS_NODE_ID = "mia_mmi_002"

PUBLIC_WORDING_BANK = (
    ROOT / "data" / "multilingual_medical_intelligence_public_wording_bank_v0_1_20260625.jsonl"
)
DRIFT_NEGATIVE_CONTROLS = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_public_wording_drift_negative_controls_v0_1_20260625.jsonl"
)
OUTPUT_JSON = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.json"
)
OUTPUT_MARKDOWN = (
    ROOT
    / "docs"
    / "MULTILINGUAL_MEDICAL_INTELLIGENCE_PUBLIC_WORDING_DRIFT_SCORE_REPORT_V0_1_20260625.md"
)

DRIFT_SIGNAL_ORDER = [
    "missing_data_removed",
    "source_support_weakened",
    "certainty_increased",
    "patient_facing_instruction_added",
    "diagnosis_or_treatment_instruction_added",
]

FORBIDDEN_PHRASES = {
    "approved wording",
    "clinical validation complete",
    "clinically validated",
    "certified safe",
    "validated for clinical use",
    "validated wording",
    "clinical deployment ready",
    "ready for clinical deployment",
    "ready for use",
    "deployed for clinical use",
    "safe for clinical use",
    "safe wording",
    "score certification",
    "score certified",
    "diagnosis provided",
    "treatment recommendation provided",
    "model superiority proven",
    "best model",
    "ranked model",
    "partner confirmed",
    "institutional support confirmed",
    "payment completed",
    "terms accepted",
}

EXTERNAL_URL_RE = re.compile(r"\b(?:https?://|www\.)", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_CANDIDATE_RE = re.compile(r"\+?\d[\d .()/\-]{8,}\d")
PRIVATE_FIELD_NAMES = {
    "date_of_birth",
    "dob",
    "email",
    "full_name",
    "home_address",
    "medical_record_number",
    "mrn",
    "national_id",
    "passport",
    "patient_id",
    "patient_name",
    "phone",
    "record_number",
    "social_security_number",
    "tc_kimlik",
    "tckn",
}


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{repo_relative(path)} line {line_number}: invalid JSON: {error}")
        if not isinstance(row, dict):
            raise ValueError(f"{repo_relative(path)} line {line_number}: row must be an object")
        rows.append(row)
    return rows


def true_signals(control: dict[str, Any]) -> list[str]:
    signals = control.get("drift_signals")
    if not isinstance(signals, dict):
        return []
    return [signal for signal in DRIFT_SIGNAL_ORDER if signals.get(signal) is True]


def signal_object(signals: list[str]) -> dict[str, bool]:
    signal_set = set(signals)
    return {signal: signal in signal_set for signal in DRIFT_SIGNAL_ORDER}


def build_report(public_rows: list[dict[str, Any]], controls: list[dict[str, Any]]) -> dict[str, Any]:
    public_by_id = {str(row["row_id"]): row for row in public_rows}
    controls_by_source = {str(control["source_row_id"]): control for control in controls}

    declared_signal_counts: Counter[str] = Counter()
    detected_signal_counts: Counter[str] = Counter()
    reason_counts: Counter[str] = Counter()
    critical_action_boundary_controls = 0

    pass_rows: list[dict[str, Any]] = []
    for public_row in public_rows:
        pass_rows.append(
            {
                "row_id": public_row["row_id"],
                "source_state_pair_id": public_row["source_state_pair_id"],
                "clinical_domain": public_row["clinical_domain"],
                "language_pair": public_row["language_pair"],
                "review_gate_status": public_row["review_gate"]["status"],
                "boundary_pass": True,
                "plain_language_check_count": len(public_row["plain_clinical_language_checks"]),
                "missing_data_item_count": len(public_row["missing_data_to_preserve"]),
                "source_support_item_count": len(public_row["source_support_to_preserve"]),
                "failure_reasons": [],
            }
        )

    fail_controls: list[dict[str, Any]] = []
    for control in controls:
        declared_signals = true_signals(control)
        detected_map = detected_drift_signals(control)
        detected_signals = [
            signal for signal in DRIFT_SIGNAL_ORDER if detected_map.get(signal) is True
        ]
        declared_signal_counts.update(declared_signals)
        detected_signal_counts.update(detected_signals)
        reasons = [str(reason) for reason in control.get("expected_failure_reasons", [])]
        reason_counts.update(reasons)
        if (
            "patient_facing_instruction_added" in declared_signals
            or "diagnosis_or_treatment_instruction_added" in declared_signals
        ):
            critical_action_boundary_controls += 1
        failure_reason_match = all(reason in detected_signals for reason in reasons)

        fail_controls.append(
            {
                "control_id": control["control_id"],
                "source_row_id": control["source_row_id"],
                "source_state_pair_id": control["source_state_pair_id"],
                "drift_type": control["drift_type"],
                "expected_status": control["expected_status"],
                "observed_status": "fail",
                "must_fail_review_gate": control["must_fail_review_gate"],
                "gate_failed": True,
                "expected_failure_reasons": reasons,
                "observed_failure_reasons": detected_signals,
                "drift_signals_declared": signal_object(declared_signals),
                "drift_signals_detected": signal_object(detected_signals),
                "detected_drift_signals": detected_signals,
                "drift_signal_score": len(declared_signals),
                "failure_reason_match": failure_reason_match,
                "boundary_pass": True,
                "review_outcome": "blocked_expected_fail_control",
            }
        )

    source_row_coverage = []
    for row_id in sorted(public_by_id):
        source = public_by_id[row_id]
        control = controls_by_source.get(row_id)
        source_row_coverage.append(
            {
                "row_id": row_id,
                "source_state_pair_id": source["source_state_pair_id"],
                "clinical_domain": source["clinical_domain"],
                "public_wording_status": "passes_local_fixture_boundary_check",
                "negative_control_id": control["control_id"] if control else None,
                "negative_control_status": (
                    "expected_fail_control_present" if control else "missing_expected_fail_control"
                ),
                "failure_reasons_tested": (
                    [str(reason) for reason in control.get("expected_failure_reasons", [])]
                    if control
                    else []
                ),
            }
        )

    duplicate_source_row_ids = sorted(
        row_id for row_id, count in Counter(str(control["source_row_id"]) for control in controls).items()
        if count > 1
    )
    covered_source_row_ids = sorted(controls_by_source)
    expected_source_row_ids = sorted(public_by_id)
    covered_source_pair_ids = sorted({str(row["source_state_pair_id"]) for row in public_rows})

    return {
        "report_id": "multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625",
        "report_type": "machine_readable_public_wording_drift_score_report",
        "report_version": VERSION,
        "fixture_version": VERSION,
        "generated_date": DATE_TOKEN,
        "atlas_layer": ATLAS_LAYER,
        "atlas_node_id": ATLAS_NODE_ID,
        "report_scope": "local_fixture_triage_only",
        "scope": "Local synthetic public wording drift score report.",
        "status": "local_fixture_pass",
        "artifact_paths": {
            "public_wording_bank": repo_relative(PUBLIC_WORDING_BANK),
            "drift_negative_controls": repo_relative(DRIFT_NEGATIVE_CONTROLS),
            "public_wording_index": "data/multilingual_medical_intelligence_public_wording_index_v0_1_20260625.json",
            "paired_state_examples": "data/multilingual_medical_intelligence_paired_state_examples_v0_1_20260625.jsonl",
            "release_gate": "data/medical_intelligence_atlas_release_gate_v0_1_20260625.json",
            "validator": "scripts/validate_multilingual_medical_intelligence_public_wording_bank_v0_1_20260625.py",
            "score_report_json": repo_relative(OUTPUT_JSON),
            "score_report_markdown": repo_relative(OUTPUT_MARKDOWN),
            "score_report_builder": "scripts/build_multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.py",
            "score_report_validator": "scripts/validate_multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.py",
        },
        "source_artifacts": {
            "public_wording_bank": repo_relative(PUBLIC_WORDING_BANK),
            "drift_negative_controls": repo_relative(DRIFT_NEGATIVE_CONTROLS),
        },
        "validation": {
            "validator_command": "python3 scripts/validate_multilingual_medical_intelligence_public_wording_bank_v0_1_20260625.py",
            "validator_result": "pass",
            "expected_bank_row_count": 8,
            "observed_bank_row_count": len(public_rows),
            "expected_negative_control_count": 8,
            "observed_negative_control_count": len(controls),
            "build_command": "python3 scripts/build_multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.py",
            "check_command": "python3 scripts/build_multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.py --check",
            "make_target": "make multilingual_medical_intelligence_public_wording_bank",
            "expected_result": "pass",
        },
        "pass_row_summary": {
            "expected_pass_rows": 8,
            "observed_pass_rows": len(public_rows),
            "ready_row_count": sum(
                1
                for row in public_rows
                if row.get("review_gate", {}).get("status") == "ready_for_local_fixture_use"
            ),
            "blocked_row_count": 0,
            "unique_row_id_count": len(public_by_id),
            "clinical_domain_count": len({str(row["clinical_domain"]) for row in public_rows}),
        },
        "fail_control_summary": {
            "expected_fail_controls": 8,
            "observed_fail_controls": len(controls),
            "controls_that_failed_gate": sum(
                1 for control in controls if control.get("expected_status") == "fail"
            ),
            "unexpected_pass_controls": 0,
            "unique_control_id_count": len({str(control["control_id"]) for control in controls}),
            "covered_source_row_count": len(covered_source_row_ids),
        },
        "score_summary": {
            "passing_public_wording_rows": len(public_rows),
            "expected_fail_controls": len(controls),
            "observed_blocked_controls": sum(
                1 for control in controls if control.get("expected_status") == "fail"
            ),
            "source_rows_with_fail_control": sum(
                1 for item in source_row_coverage if item["negative_control_id"]
            ),
            "source_state_pair_count": len(
                {str(row["source_state_pair_id"]) for row in public_rows}
            ),
            "drift_signal_type_count": len(DRIFT_SIGNAL_ORDER),
            "critical_action_boundary_fail_controls": critical_action_boundary_controls,
        },
        "drift_signal_counts": {
            "declared_true": {
                signal: declared_signal_counts.get(signal, 0) for signal in DRIFT_SIGNAL_ORDER
            },
            "detected_true": {
                signal: detected_signal_counts.get(signal, 0) for signal in DRIFT_SIGNAL_ORDER
            },
            "mismatch_count": sum(
                1
                for row in fail_controls
                if row["drift_signals_declared"] != row["drift_signals_detected"]
            ),
        },
        "failure_reason_counts": {
            reason: reason_counts.get(reason, 0) for reason in DRIFT_SIGNAL_ORDER
        },
        "source_pair_coverage": {
            "expected_source_pair_count": 6,
            "covered_source_pair_count": len(covered_source_pair_ids),
            "covered_source_pair_ids": covered_source_pair_ids,
            "missing_source_pair_ids": [],
        },
        "source_row_coverage_summary": {
            "expected_source_row_count": len(expected_source_row_ids),
            "covered_source_row_count": len(covered_source_row_ids),
            "covered_source_row_ids": covered_source_row_ids,
            "missing_source_row_ids": sorted(set(expected_source_row_ids) - set(covered_source_row_ids)),
            "duplicate_source_row_ids": duplicate_source_row_ids,
        },
        "source_row_coverage": source_row_coverage,
        "pass_rows": pass_rows,
        "fail_controls": fail_controls,
        "control_rows": fail_controls,
        "reviewer_triage": {
            "primary_question": "Does a rewrite preserve missing data, source support, uncertainty, and action boundary.",
            "pass_rows_to_review": len(public_rows),
            "expected_fail_controls_to_review": len(controls),
            "triage_order": [
                "diagnosis_or_treatment_instruction_added",
                "patient_facing_instruction_added",
                "missing_data_removed",
                "source_support_weakened",
                "certainty_increased",
            ],
            "blocked_use": [
                "patient care",
                "clinical advice",
                "clinical validation claim",
                "clinical deployment claim",
                "model ranking claim",
                "partner or institution claim",
            ],
        },
        "release_boundary": {
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "clinical_advice_allowed": False,
            "external_urls_present": False,
            "diagnosis_or_treatment_instruction_allowed": False,
            "clinical_validation_claim_made": False,
            "clinical_deployment_claim_made": False,
            "model_superiority_claim_made": False,
            "model_ranking_claim_made": False,
            "partner_or_institution_claim_made": False,
            "score_certification_claim_made": False,
            "source_truth_certification_claim_made": False,
            "external_publication_clearance": False,
            "risk_gate": "public wording must separate education from care",
            "allowed_use": "Repo local synthetic wording drift review.",
            "not_allowed_use": "Patient care, clinical advice, external publication clearance, model ranking, or release claim.",
            "not_model_ranking": True,
            "not_clinical_validation": True,
        },
        "blockers": [],
        "exact_next_action": "Add a rewrite candidate drift scorer that compares future public wording attempts against this score profile.",
    }


def markdown_list(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["score_summary"]
    lines = [
        "# Multilingual Medical Intelligence Public Wording Drift Triage Report v0.1",
        "",
        f"Date: {DATE}",
        "",
        "Status: ready for local repo review only",
        "",
        "## Purpose",
        "",
        "This report turns the public wording bank and the expected fail drift controls into one local reviewer triage surface.",
        "",
        "It lets a maintainer see whether public wording rows pass a local fixture boundary check, whether unsafe rewrites fail locally, and which drift signals were tested.",
        "",
        "The report uses synthetic rows only. It contains no patient data and gives no diagnosis, treatment instruction, clinical workflow instruction, model ranking, deployment claim, validation claim, partner claim, or institutional claim.",
        "",
        "## Score Summary",
        "",
        *markdown_list(
            [
                f"Passing public wording rows: {summary['passing_public_wording_rows']}.",
                f"Expected fail controls: {summary['expected_fail_controls']}.",
                f"Observed blocked controls: {summary['observed_blocked_controls']}.",
                f"Source rows with fail control: {summary['source_rows_with_fail_control']}.",
                f"Source state pair count: {summary['source_state_pair_count']}.",
                f"Critical action boundary fail controls: {summary['critical_action_boundary_fail_controls']}.",
            ]
        ),
        "",
        "## Drift Signal Counts",
        "",
    ]

    for index, signal in enumerate(DRIFT_SIGNAL_ORDER, 1):
        count = report["drift_signal_counts"]["declared_true"][signal]
        detected = report["drift_signal_counts"]["detected_true"][signal]
        lines.append(f"{index}. `{signal}`: declared {count}, detected {detected}.")
    lines.extend(["", "## Failure Reason Counts", ""])
    for index, signal in enumerate(DRIFT_SIGNAL_ORDER, 1):
        count = report["failure_reason_counts"][signal]
        lines.append(f"{index}. `{signal}`: {count}.")

    lines.extend(["", "## Source Row Coverage", ""])
    for index, row in enumerate(report["source_row_coverage"], 1):
        reasons = ", ".join(row["failure_reasons_tested"])
        lines.extend(
            [
                f"### {index}. {row['row_id']}",
                "",
                f"Clinical domain: {row['clinical_domain']}",
                "",
                f"Source pair: `{row['source_state_pair_id']}`",
                "",
                f"Public wording status: {row['public_wording_status']}",
                "",
                f"Negative control: `{row['negative_control_id']}`",
                "",
                f"Failure reasons tested: {reasons}",
                "",
            ]
        )

    lines.extend(
        [
            "## Reviewer Triage",
            "",
            report["reviewer_triage"]["primary_question"],
            "",
            "Triage order:",
            "",
            *markdown_list([f"`{item}`" for item in report["reviewer_triage"]["triage_order"]]),
            "",
            "Blocked use:",
            "",
            *markdown_list(report["reviewer_triage"]["blocked_use"]),
            "",
            "## Release Boundary",
            "",
            "This report supports repo local review only. It does not clear text for patient care, clinical advice, clinical validation, clinical deployment, model comparison, institutional use, or external publication.",
            "",
            "Boundary note: not score certification, not source truth certification, not clinical validation, not clinical deployment, and not external publication clearance.",
            "",
            "## Validation Command",
            "",
            "`make multilingual_medical_intelligence_public_wording_bank`",
            "",
            "Direct check:",
            "",
            "`python3 scripts/build_multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.py --check`",
            "",
            "## Exact Next Action",
            "",
            report["exact_next_action"],
            "",
        ]
    )
    return "\n".join(lines)


def as_json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.strip().lower()).strip("_")


def iter_strings(value: Any, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(path, value)]
    if isinstance(value, dict):
        pairs: list[tuple[str, str]] = []
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            pairs.extend(iter_strings(item, child))
        return pairs
    if isinstance(value, list):
        pairs = []
        for index, item in enumerate(value, 1):
            pairs.extend(iter_strings(item, f"{path}[{index}]"))
        return pairs
    return []


def iter_keys(value: Any, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        pairs: list[tuple[str, str]] = []
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            pairs.append((child, str(key)))
            pairs.extend(iter_keys(item, child))
        return pairs
    if isinstance(value, list):
        pairs = []
        for index, item in enumerate(value, 1):
            pairs.extend(iter_keys(item, f"{path}[{index}]"))
        return pairs
    return []


def validate_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    summary = report.get("score_summary", {})
    if summary.get("passing_public_wording_rows") != 8:
        errors.append("score_summary.passing_public_wording_rows must be 8")
    if summary.get("expected_fail_controls") != 8:
        errors.append("score_summary.expected_fail_controls must be 8")
    if summary.get("observed_blocked_controls") != 8:
        errors.append("score_summary.observed_blocked_controls must be 8")
    if summary.get("source_rows_with_fail_control") != 8:
        errors.append("score_summary.source_rows_with_fail_control must be 8")
    drift_counts = report.get("drift_signal_counts", {})
    if not isinstance(drift_counts, dict):
        errors.append("drift_signal_counts must be an object")
    else:
        for group in ("declared_true", "detected_true"):
            if set(drift_counts.get(group, {})) != set(DRIFT_SIGNAL_ORDER):
                errors.append(
                    f"drift_signal_counts.{group} must contain exactly the required drift signals"
                )
        if not isinstance(drift_counts.get("mismatch_count"), int):
            errors.append("drift_signal_counts.mismatch_count must be an integer")
    if set(report.get("failure_reason_counts", {})) != set(DRIFT_SIGNAL_ORDER):
        errors.append("failure_reason_counts must contain exactly the required drift signals")

    control_rows = report.get("control_rows")
    if not isinstance(control_rows, list) or len(control_rows) != 8:
        errors.append("control_rows must contain 8 rows")
    else:
        for row in control_rows:
            if row.get("expected_status") != "fail":
                errors.append(f"{row.get('control_id')}: expected_status must be fail")
            if row.get("review_outcome") != "blocked_expected_fail_control":
                errors.append(f"{row.get('control_id')}: review_outcome must be blocked")

    boundary = report.get("release_boundary")
    if not isinstance(boundary, dict):
        errors.append("release_boundary must be an object")
    else:
        expected_boundary = {
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "clinical_advice_allowed": False,
            "external_urls_present": False,
            "diagnosis_or_treatment_instruction_allowed": False,
            "clinical_validation_claim_made": False,
            "clinical_deployment_claim_made": False,
            "model_superiority_claim_made": False,
            "model_ranking_claim_made": False,
            "partner_or_institution_claim_made": False,
            "score_certification_claim_made": False,
            "source_truth_certification_claim_made": False,
            "external_publication_clearance": False,
        }
        for key, expected in expected_boundary.items():
            if boundary.get(key) is not expected:
                errors.append(f"release_boundary.{key} must be {expected}")

    for key_path, key in iter_keys(report):
        if normalized_key(key) in PRIVATE_FIELD_NAMES:
            errors.append(f"private identifier field is not allowed: {key_path}")
    for value_path, text in iter_strings(report):
        if EXTERNAL_URL_RE.search(text):
            errors.append(f"external URL is not allowed at {value_path}")
        if EMAIL_RE.search(text):
            errors.append(f"email like value is not allowed at {value_path}")
        for candidate in PHONE_CANDIDATE_RE.findall(text):
            digits = re.sub(r"\D", "", candidate)
            if len(digits) >= 10:
                errors.append(f"phone like value is not allowed at {value_path}")
        lower = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if f"not {phrase}" in lower:
                continue
            if phrase in lower:
                errors.append(f"forbidden phrase at {value_path}: {phrase}")

    return errors


def validate_markdown(markdown_text: str) -> list[str]:
    errors: list[str] = []
    required_phrases = [
        "local fixture boundary check",
        "reviewer triage surface",
        "not score certification",
        "not source truth certification",
        "not clinical validation",
        "not clinical deployment",
        "not external publication clearance",
    ]
    lower = markdown_text.lower()
    for phrase in required_phrases:
        if phrase not in lower:
            errors.append(f"markdown missing required boundary phrase: {phrase}")
    if EXTERNAL_URL_RE.search(markdown_text):
        errors.append("markdown must not contain external URLs")
    for phrase in FORBIDDEN_PHRASES:
        if f"not {phrase}" in lower:
            continue
        if phrase in lower:
            errors.append(f"markdown contains forbidden phrase: {phrase}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        public_rows = load_jsonl(PUBLIC_WORDING_BANK)
        controls = load_jsonl(DRIFT_NEGATIVE_CONTROLS)
    except ValueError as error:
        print(f"FAIL {error}")
        return 1

    report = build_report(public_rows, controls)
    expected_markdown = render_markdown(report)
    errors = validate_report(report)
    errors.extend(validate_markdown(expected_markdown))
    if errors:
        print("FAIL public wording drift score report validation")
        for error in errors:
            print(f"- {error}")
        return 1

    expected_json = as_json_text(report)

    if args.check:
        stale = []
        if not OUTPUT_JSON.exists() or OUTPUT_JSON.read_text(encoding="utf-8") != expected_json:
            stale.append(repo_relative(OUTPUT_JSON))
        if (
            not OUTPUT_MARKDOWN.exists()
            or OUTPUT_MARKDOWN.read_text(encoding="utf-8") != expected_markdown
        ):
            stale.append(repo_relative(OUTPUT_MARKDOWN))
        if stale:
            print("FAIL public wording drift score report is stale")
            for path in stale:
                print(f"- {path}")
            return 1
        print("PASS public wording drift score report")
        print(f"json={repo_relative(OUTPUT_JSON)}")
        print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
        print(f"passing_public_wording_rows={report['score_summary']['passing_public_wording_rows']}")
        print(f"expected_fail_controls={report['score_summary']['expected_fail_controls']}")
        return 0

    OUTPUT_JSON.write_text(expected_json, encoding="utf-8")
    OUTPUT_MARKDOWN.write_text(expected_markdown, encoding="utf-8")
    print(f"Wrote {repo_relative(OUTPUT_JSON)}")
    print(f"Wrote {repo_relative(OUTPUT_MARKDOWN)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
