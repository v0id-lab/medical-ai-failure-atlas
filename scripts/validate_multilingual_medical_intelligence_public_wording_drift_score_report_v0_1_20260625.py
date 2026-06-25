#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

sys.dont_write_bytecode = True

from build_multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625 import (
    DRIFT_NEGATIVE_CONTROLS,
    OUTPUT_JSON,
    OUTPUT_MARKDOWN,
    PUBLIC_WORDING_BANK,
    as_json_text,
    build_report,
    load_jsonl,
    render_markdown,
    repo_relative,
    validate_markdown,
    validate_report,
)


def main() -> int:
    errors: list[str] = []
    for path in (PUBLIC_WORDING_BANK, DRIFT_NEGATIVE_CONTROLS, OUTPUT_JSON, OUTPUT_MARKDOWN):
        if not path.exists():
            errors.append(f"missing required file: {repo_relative(path)}")

    if errors:
        print("FAIL public wording drift score report validation")
        for error in errors:
            print(f"- {error}")
        return 1

    try:
        public_rows = load_jsonl(PUBLIC_WORDING_BANK)
        controls = load_jsonl(DRIFT_NEGATIVE_CONTROLS)
        actual_json = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    except (ValueError, json.JSONDecodeError) as error:
        print(f"FAIL public wording drift score report validation: {error}")
        return 1

    expected_report = build_report(public_rows, controls)
    expected_json_text = as_json_text(expected_report)
    expected_markdown = render_markdown(expected_report)
    actual_markdown = OUTPUT_MARKDOWN.read_text(encoding="utf-8")

    errors.extend(validate_report(actual_json))
    errors.extend(validate_markdown(actual_markdown))

    if OUTPUT_JSON.read_text(encoding="utf-8") != expected_json_text:
        errors.append(f"stale JSON report: {repo_relative(OUTPUT_JSON)}")
    if actual_markdown != expected_markdown:
        errors.append(f"stale Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")

    if errors:
        print("FAIL public wording drift score report validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public wording drift score report validation")
    print(f"json={repo_relative(OUTPUT_JSON)}")
    print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
    print(f"passing_public_wording_rows={actual_json['score_summary']['passing_public_wording_rows']}")
    print(f"expected_fail_controls={actual_json['score_summary']['expected_fail_controls']}")
    print(
        "critical_action_boundary_fail_controls="
        f"{actual_json['score_summary']['critical_action_boundary_fail_controls']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
