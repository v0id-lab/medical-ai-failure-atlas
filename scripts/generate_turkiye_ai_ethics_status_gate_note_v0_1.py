#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_AI_ETHICS_STATUS_GATE_NOTE_V0_1.md"
DATA = ROOT / "docs" / "turkiye_ai_ethics_status_gate_note_v0_1.json"


SOURCE_ROWS = [
    {
        "source_id": "TAESG001",
        "source_name": "Ankara İl Sağlık Müdürlüğü AI studies ethics page",
        "source_url": "https://ankaraism.saglik.gov.tr/TR-371527/yapay-zeka-ile-ilgili-calismalar.html",
        "source_date": "30 January 2026",
        "observed_claim": "The page says AI related studies presented to that ethics committee will be suspended until new regulation.",
        "gate_use": "treat as a local ethics status gate signal before any AI study route claim",
        "blocked_claim": "national ethics rule claim",
    },
    {
        "source_id": "TAESG002",
        "source_name": "Sağlık Bilgi Sistemleri Genel Müdürlüğü AI department page",
        "source_url": "https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html",
        "source_date": "21 August 2024",
        "observed_claim": "The page lists ministry AI department tasks around AI improvable processes, solutions, collaborations, interoperability, and education materials.",
        "gate_use": "keep public Track A wording aligned with education, interoperability, and assurance preparation without official role claims",
        "blocked_claim": "official ministry role claim",
    },
    {
        "source_id": "TAESG003",
        "source_name": "Current medical AI intelligence priority update",
        "source_url": "docs/current_medical_ai_intelligence_priority_update_20260618_v0_1.json",
        "source_date": "18 June 2026",
        "observed_claim": "The current intelligence pass elevated Türkiye ethics status gates as a safe next public build.",
        "gate_use": "connect ethics status verification to the public medical AI portfolio roadmap",
        "blocked_claim": "clinical readiness claim",
    },
]


GATE_ROWS = [
    {
        "gate_id": "TAESGATE001",
        "gate": "local ethics page scope",
        "question": "Which ethics committee page or portal is being referenced",
        "required_evidence": "committee specific page, portal notice, or official email",
        "public_action": "record local status only",
        "blocked_claim": "Türkiye wide rule claim",
    },
    {
        "gate_id": "TAESGATE002",
        "gate": "study type scope",
        "question": "Is the work synthetic infrastructure, retrospective data work, prospective clinical study, or deployment",
        "required_evidence": "study type and committee route statement",
        "public_action": "keep synthetic infrastructure separate from clinical study language",
        "blocked_claim": "clinical study submission claim",
    },
    {
        "gate_id": "TAESGATE003",
        "gate": "patient data scope",
        "question": "Will any identifiable, deidentified, or institutional patient data be used",
        "required_evidence": "data use decision and approval route",
        "public_action": "keep no patient data boundary visible",
        "blocked_claim": "patient data readiness claim",
    },
    {
        "gate_id": "TAESGATE004",
        "gate": "clinical validation scope",
        "question": "Is anyone claiming clinical validation, clinical usefulness, or clinical deployment readiness",
        "required_evidence": "formal study protocol and approvals before any claim",
        "public_action": "block validation and deployment language",
        "blocked_claim": "clinical validation claim",
    },
    {
        "gate_id": "TAESGATE005",
        "gate": "institutional role scope",
        "question": "Is any ministry, hospital, university, or ethics committee role being claimed",
        "required_evidence": "written authorization before role wording",
        "public_action": "use public source and no endorsement wording",
        "blocked_claim": "official role or endorsement claim",
    },
    {
        "gate_id": "TAESGATE006",
        "gate": "public build route",
        "question": "Can the next action be public infrastructure without portal submission",
        "required_evidence": "repo artifact and validation log",
        "public_action": "publish gate note, validator, and issue closeout only",
        "blocked_claim": "submission or approval claim",
    },
]


FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_submission_claim": True,
    "no_application_claim": True,
    "no_ethics_approval_claim": True,
    "no_national_rule_claim": True,
    "no_official_role_claim": True,
    "no_endorsement_claim": True,
    "no_patient_data_claim": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_terms_acceptance": True,
    "no_payment": True,
}


def build_payload() -> dict:
    return {
        "artifact": "turkiye_ai_ethics_status_gate_note_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source_row_count": len(SOURCE_ROWS),
        "gate_row_count": len(GATE_ROWS),
        "source_rows": SOURCE_ROWS,
        "gate_rows": GATE_ROWS,
        **FLAGS,
        "next_safe_public_build": "Add reviewer question maintainer public preview acceptance archive public handoff closure note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
    }


def build_markdown(payload: dict) -> str:
    lines = [
        "# Türkiye AI ethics status gate note v0.1",
        "",
        "Status: public preview.",
        "",
        "Date: 2026 06 18.",
        "",
        "This note turns the current Türkiye health AI ethics signal into a public verification gate for synthetic medical AI safety infrastructure.",
        "",
        "It is not an ethics submission, not an ethics approval, not a national rule claim, not a clinical study claim, not clinical advice, not clinical deployment, not clinical validation, not a route access claim, not an official role claim, and not an endorsement claim.",
        "",
        "It uses no patient data.",
        "",
        "## Source status",
        "",
        "1. Ankara İl Sağlık Müdürlüğü AI studies ethics page is treated as a local ethics status signal.",
        "2. The signal is not generalized into a Türkiye wide rule without separate committee or regulator verification.",
        "3. Sağlık Bilgi Sistemleri Genel Müdürlüğü AI department page is treated as a public source for education, interoperability, collaboration, and AI process language only.",
        "4. The current medical AI intelligence priority update elevated ethics status gates as a safe public build path.",
        "",
        "## Gate rows",
        "",
    ]
    for index, row in enumerate(payload["gate_rows"], start=1):
        lines.extend(
            [
                f"### {index}. {row['gate_id']}",
                "",
                f"Gate: {row['gate']}",
                "",
                f"Question: {row['question']}",
                "",
                f"Required evidence: {row['required_evidence']}",
                "",
                f"Public action: {row['public_action']}",
                "",
                f"Blocked claim: {row['blocked_claim']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary checklist",
            "",
            "1. No patient data.",
            "2. No ethics approval claim.",
            "3. No national rule claim.",
            "4. No submission claim.",
            "5. No application claim.",
            "6. No official role claim.",
            "7. No endorsement claim.",
            "8. No clinical validation claim.",
            "9. No clinical deployment claim.",
            "10. No terms acceptance and no payment.",
            "",
            "## Next safe public build",
            "",
            payload["next_safe_public_build"],
            "",
            "## Runnable check",
            "",
            "```bash",
            "make turkiye_ai_ethics_status_gate_note",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    payload = build_payload()
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    DOC.write_text(build_markdown(payload), encoding="utf-8")
    print(f"generated={DATA.relative_to(ROOT)}")
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"source_rows={payload['source_row_count']}")
    print(f"gate_rows={payload['gate_row_count']}")


if __name__ == "__main__":
    main()
