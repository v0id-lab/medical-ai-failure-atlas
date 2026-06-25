#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

sys.dont_write_bytecode = True

from score_multilingual_medical_intelligence_rewrite_candidates_v0_1_20260625 import (
    DRIFT_NEGATIVE_CONTROLS,
    DRIFT_SCORE_REPORT,
    OUTPUT_JSON,
    OUTPUT_MARKDOWN,
    PUBLIC_WORDING_BANK,
    REWRITE_CANDIDATES,
    as_json_text,
    build_report,
    load_jsonl,
    load_score_profile,
    render_markdown,
    repo_relative,
    validate_candidate_rows,
    validate_markdown,
    validate_report,
)


def main() -> int:
    errors: list[str] = []
    for path in (
        PUBLIC_WORDING_BANK,
        DRIFT_NEGATIVE_CONTROLS,
        DRIFT_SCORE_REPORT,
        REWRITE_CANDIDATES,
        OUTPUT_JSON,
        OUTPUT_MARKDOWN,
    ):
        if not path.exists():
            errors.append(f"missing required file: {repo_relative(path)}")

    if errors:
        print("FAIL rewrite candidate score report validation")
        for error in errors:
            print(f"- {error}")
        return 1

    try:
        public_rows = load_jsonl(PUBLIC_WORDING_BANK)
        controls = load_jsonl(DRIFT_NEGATIVE_CONTROLS)
        candidates = load_jsonl(REWRITE_CANDIDATES)
        score_profile = load_score_profile(DRIFT_SCORE_REPORT)
        actual_json = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    except (ValueError, json.JSONDecodeError) as error:
        print(f"FAIL rewrite candidate score report validation: {error}")
        return 1

    errors.extend(validate_candidate_rows(candidates, public_rows, controls, score_profile))
    expected_report = build_report(public_rows, controls, candidates, score_profile)
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
        print("FAIL rewrite candidate score report validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS rewrite candidate score report validation")
    print(f"json={repo_relative(OUTPUT_JSON)}")
    print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
    print(f"candidate_count={actual_json['score_summary']['candidate_count']}")
    print(f"blocked_candidates={actual_json['score_summary']['observed_blocked_candidates']}")
    print(f"pass_candidates={actual_json['score_summary']['observed_pass_candidates']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
