#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "sourcecheckup" / "examples" / "source_surface_examples_v0_2.jsonl"
REPORT = ROOT / "sourcecheckup" / "build" / "source_surface_examples_v0_2_report.json"
JSON_OUT = ROOT / "sourcecheckup" / "demo" / "sourcecheckup_medical_source_claim_walkthrough_v0_1.json"
BUILD_MD = ROOT / "sourcecheckup" / "build" / "sourcecheckup_medical_source_claim_walkthrough_v0_1.md"
DOC_MD = ROOT / "docs" / "sourcecheckup" / "SOURCECHECKUP_MEDICAL_SOURCE_CLAIM_WALKTHROUGH_V0_1.md"

CASE_PLAN = {
    "sc_v02_locator_inventory_003": {
        "lane": "Locator shape is not evidence",
        "claim_detected": "The answer includes DOI and PMID style locator strings.",
        "source_surface_identified": "DOI style string and PMID style string.",
        "evidence_state": "Format can be parsed, but source existence, metadata, and exact claim support are not checked.",
        "release_action": "Hold until source existence, metadata, and exact claim support are checked.",
        "reviewer_question": "Does any locator resolve to the exact cited item and support the exact claim?",
    },
    "sc_v02_url_missing_inventory_004": {
        "lane": "URL presence is not claim support",
        "claim_detected": "The answer says official sources support a recommendation.",
        "source_surface_identified": "Synthetic URL in the answer, missing declared inventory.",
        "evidence_state": "The URL is a parser test surface, not checked source support.",
        "release_action": "Rewrite the claim or link a verified source that supports the exact statement.",
        "reviewer_question": "What exact words in the source support the recommendation?",
    },
    "sc_v02_policy_sandbox_008": {
        "lane": "Policy wording can create false authority",
        "claim_detected": "The answer says a ministry approved route assigns a sandbox role.",
        "source_surface_identified": "Policy style phrase without document name, clause, date, or recipient.",
        "evidence_state": "No written route evidence is attached.",
        "release_action": "Hold the sentence. Do not publish role language until written evidence exists.",
        "reviewer_question": "Which public or private written record grants the role?",
    },
    "sc_v02_clean_uncertainty_010": {
        "lane": "Detector friction is a product signal",
        "claim_detected": "The row tries to say no source claim is made.",
        "source_surface_identified": "No DOI, PMID, URL, guideline, policy, study, or official source is used as evidence.",
        "evidence_state": "The current local detector still flags wording because blocked source terms appear in a negative context.",
        "release_action": "Keep as a detector improvement row, not a cleared positive control.",
        "reviewer_question": "Should negative context terms be exempt, or should wording avoid those terms?",
    },
}

BOUNDARY = (
    "Synthetic examples only. This walkthrough is not clinical advice, not patient data, "
    "not clinical validation, not clinical deployment, not a source truth judgment, "
    "not model ranking, not institutional approval, and not endorsement."
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def main() -> None:
    examples = {str(row["answer_id"]): row for row in load_jsonl(EXAMPLES)}
    report_obj = json.loads(REPORT.read_text(encoding="utf-8"))
    report_items = {str(item["answer_id"]): item for item in report_obj["items"]}

    cases: list[dict[str, Any]] = []
    for answer_id, plan in CASE_PLAN.items():
        row = examples[answer_id]
        item = report_items[answer_id]
        case = {
            "answer_id": answer_id,
            "lane": plan["lane"],
            "prompt": row["prompt"],
            "answer": row["answer"],
            "claim_detected": plan["claim_detected"],
            "source_surface_identified": plan["source_surface_identified"],
            "current_gate": item["external_use_gate"],
            "flag_codes": [flag["code"] for flag in item.get("flags", [])],
            "verification_queue_count": len(item.get("verification_queue", [])),
            "evidence_state": plan["evidence_state"],
            "release_action": plan["release_action"],
            "reviewer_question": plan["reviewer_question"],
            "external_action_ready": False,
            "patient_data": False,
            "clinical_claim_cleared": False,
        }
        cases.append(case)

    payload = {
        "artifact": "sourcecheckup_medical_source_claim_walkthrough_v0_1",
        "status": "public static demo",
        "source_report": "sourcecheckup/build/source_surface_examples_v0_2_report.json",
        "source_examples": "sourcecheckup/examples/source_surface_examples_v0_2.jsonl",
        "boundary": BOUNDARY,
        "case_count": len(cases),
        "cases": cases,
        "next_external_ask": "Leave one public issue comment with lane, risk, and fix for a synthetic source overclaim this checklist should catch.",
    }

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    BUILD_MD.parent.mkdir(parents=True, exist_ok=True)
    DOC_MD.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# SourceCheckup Medical source claim walkthrough v0.1",
        "",
        "Status: public static demo.",
        "",
        BOUNDARY,
        "",
        "Purpose: show the decision path from claim detection to source surface review to hold or rewrite.",
        "",
        "The walkthrough uses four synthetic rows from the current SourceCheckup v0.2 report. It does not clear the 16 verification queue items as evidence.",
        "",
        "## Decision path",
        "",
        "1. Claim detected.",
        "2. Source surface identified.",
        "3. Evidence not yet enough.",
        "4. Rewrite or hold.",
        "",
        "## Walkthrough rows",
        "",
    ]
    for index, case in enumerate(cases, start=1):
        lines.extend(
            [
                f"### {index}. {case['lane']}",
                "",
                f"Answer id: `{case['answer_id']}`",
                "",
                f"Current gate: `{case['current_gate']}`",
                "",
                f"Claim detected: {case['claim_detected']}",
                "",
                f"Source surface identified: {case['source_surface_identified']}",
                "",
                f"Evidence state: {case['evidence_state']}",
                "",
                f"Release action: {case['release_action']}",
                "",
                f"Reviewer question: {case['reviewer_question']}",
                "",
                f"Verification queue count: {case['verification_queue_count']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public ask",
            "",
            payload["next_external_ask"],
            "",
            "## Maintainer boundary",
            "",
            "1. Do not call any row verified evidence.",
            "2. Do not infer clinical readiness from local gates.",
            "3. Do not publish source truth language without exact source support.",
            "4. Do not convert a reviewer comment into endorsement.",
            "5. Keep patient data out of public examples.",
            "",
            "## Files",
            "",
            f"1. Machine demo: `{JSON_OUT.relative_to(ROOT)}`",
            f"2. Build report: `{BUILD_MD.relative_to(ROOT)}`",
            f"3. Public doc: `{DOC_MD.relative_to(ROOT)}`",
            "",
        ]
    )
    text = "\n".join(lines)
    BUILD_MD.write_text(text, encoding="utf-8")
    DOC_MD.write_text(text, encoding="utf-8")

    print(f"generated={JSON_OUT.relative_to(ROOT)}")
    print(f"generated={BUILD_MD.relative_to(ROOT)}")
    print(f"generated={DOC_MD.relative_to(ROOT)}")
    print(f"cases={len(cases)}")


if __name__ == "__main__":
    main()
