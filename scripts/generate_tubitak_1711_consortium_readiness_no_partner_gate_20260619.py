#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUBITAK_1711_CONSORTIUM_READINESS_NO_PARTNER_GATE_20260619.md"
DATA = ROOT / "docs" / "tubitak_1711_consortium_readiness_no_partner_gate_20260619.json"


OFFICIAL_FACTS = [
    {
        "fact_id": "T1711NPG001",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The 2026 call was opened on 15 June 2026.",
        "readiness_meaning": "The call is live and can be tracked, but live status does not create fit or authority.",
    },
    {
        "fact_id": "T1711NPG002",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The official page lists application intake from 15 June 2026 to 18 September 2026.",
        "readiness_meaning": "There is time for route owner replies and consortium evidence before any formal move.",
    },
    {
        "fact_id": "T1711NPG003",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The official page lists pre registration completion by 14 September 2026 at 17:30.",
        "readiness_meaning": "A private decision deadline exists before the final application window.",
    },
    {
        "fact_id": "T1711NPG004",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The official page lists smart education technologies as one of five priority areas and does not list health as a direct priority area.",
        "readiness_meaning": "Any possible route must be treated as education adjacent, not a direct health priority claim.",
    },
    {
        "fact_id": "T1711NPG005",
        "source": "TÜBİTAK 1711 support page",
        "url": "https://tubitak.gov.tr/tr/destekler/sanayi/ulusal-destek-programlari/1711-yapay-zeka-ekosistem-cagrisi",
        "checked_fact": "The support page says applications without a consortium are not evaluated.",
        "readiness_meaning": "No single person public portfolio can be described as application ready.",
    },
    {
        "fact_id": "T1711NPG006",
        "source": "TÜBİTAK 1711 support page",
        "url": "https://tubitak.gov.tr/tr/destekler/sanayi/ulusal-destek-programlari/1711-yapay-zeka-ekosistem-cagrisi",
        "checked_fact": "The support page describes a customer organization, a technology provider company, an experienced research route, and TÜBİTAK Yapay Zekâ Enstitüsü in the model.",
        "readiness_meaning": "Readiness requires evidence for all route roles before any public or private application language.",
    },
]


READINESS_GATES = [
    {
        "gate_id": "NPG001",
        "gate": "Demand owner",
        "needed_evidence": "A real organization says clinician AI literacy or health AI safety education is an actual demand.",
        "current_state": "No route owner has replied with demand side fit.",
        "public_action": "Keep as open evidence gap.",
    },
    {
        "gate_id": "NPG002",
        "gate": "Education technology provider",
        "needed_evidence": "A provider route owner says the topic is in scope as smart education technology.",
        "current_state": "No provider route owner reply exists.",
        "public_action": "Keep as open evidence gap.",
    },
    {
        "gate_id": "NPG003",
        "gate": "Research route",
        "needed_evidence": "A university lab, center, public research center, or institute route gives substantive research fit feedback.",
        "current_state": "Only one Hacettepe acknowledgement exists, with no substantive research commitment.",
        "public_action": "Record as partial signal only.",
    },
    {
        "gate_id": "NPG004",
        "gate": "YZE pre application interface",
        "needed_evidence": "A confirmed consortium has reason to approach TÜBİTAK Yapay Zekâ Enstitüsü.",
        "current_state": "No consortium exists.",
        "public_action": "Do not request a meeting or intent declaration.",
    },
    {
        "gate_id": "NPG005",
        "gate": "Private authority",
        "needed_evidence": "Goktug confirms authority, time, role, budget boundary, terms boundary, and whether any formal move is allowed.",
        "current_state": "No clearance for application, partner, budget, terms, or formal route action.",
        "public_action": "Block all formal claims.",
    },
]


GMAIL_CHECK = {
    "checked_at": "2026 06 19 18:07 TRT",
    "threads": [
        "19edcafe5c2dfa60",
        "19eda863ce89f083",
        "19edaa3a3868fd0f",
        "19edac07e13052fa",
        "19edb2e645ca1f6d",
        "19edb491af3d687b",
        "19edb64c4ae9fec6",
        "19edb8289b165cc0",
        "19edb9dc297ad804",
    ],
    "result": "Prior Hacettepe health informatics acknowledgement only. No new route owner reply.",
}


BOUNDARIES = [
    "No application submission.",
    "No PRODİS action.",
    "No intent declaration.",
    "No YZE meeting request.",
    "No partner claim.",
    "No institution claim.",
    "No health priority fit claim.",
    "No budget claim.",
    "No terms acceptance.",
    "No payment.",
    "No patient data.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No model ranking.",
    "No score certification.",
    "No endorsement claim.",
]


def write_json() -> None:
    payload = {
        "artifact": "tubitak_1711_consortium_readiness_no_partner_gate_20260619",
        "status": "public readiness gate, not an application",
        "official_facts": OFFICIAL_FACTS,
        "readiness_gates": READINESS_GATES,
        "gmail_check": GMAIL_CHECK,
        "boundary_count": len(BOUNDARIES),
        "official_fact_count": len(OFFICIAL_FACTS),
        "readiness_gate_count": len(READINESS_GATES),
        "contains_patient_data": False,
        "claims_application": False,
        "claims_prodis_action": False,
        "claims_intent_declaration": False,
        "claims_yze_meeting_request": False,
        "claims_partner": False,
        "claims_institution": False,
        "claims_health_priority_fit": False,
        "claims_budget": False,
        "claims_terms_acceptance": False,
        "claims_payment": False,
        "claims_clinical_validation": False,
        "claims_clinical_deployment": False,
        "claims_ranking": False,
        "claims_score_certification": False,
        "claims_endorsement": False,
        "next_action": "Wait for a real route owner reply or build a private decision note for Goktug. Do not submit, request YZE contact, or claim a consortium.",
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines = [
        "# TÜBİTAK 1711 Consortium Readiness No Partner Gate",
        "",
        "Date: 2026 06 19",
        "",
        "Status: public readiness gate, not an application.",
        "",
        "Purpose: keep the TÜBİTAK 1711 route useful while blocking false consortium, partner, institution, health priority, budget, terms, patient data, clinical validation, deployment, ranking, score, and endorsement claims.",
        "",
        "This package is a readiness gate only. It is not a PRODİS action, not an intent declaration, not a YZE meeting request, not a partner commitment, not a budget plan, and not an institution statement.",
        "",
        "## Current verdict",
        "",
        "The route is actionable only as evidence building. A real TÜBİTAK 1711 path would need demand owner evidence, education technology provider evidence, research route evidence, YZE pre application readiness, and private authority clearance.",
        "",
        "The current public state is no partner gate. That means no consortium exists and no formal action is allowed from this package.",
        "",
        "## Official source facts",
        "",
    ]
    for fact in OFFICIAL_FACTS:
        lines.extend(
            [
                f"### {fact['fact_id']}: {fact['source']}",
                "",
                f"Official source: {fact['url']}",
                "",
                f"Checked fact: {fact['checked_fact']}",
                "",
                f"Readiness meaning: {fact['readiness_meaning']}",
                "",
            ]
        )
    lines.extend(["## Readiness gates", ""])
    for gate in READINESS_GATES:
        lines.extend(
            [
                f"### {gate['gate_id']}: {gate['gate']}",
                "",
                f"Needed evidence: {gate['needed_evidence']}",
                "",
                f"Current state: {gate['current_state']}",
                "",
                f"Public action: {gate['public_action']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Gmail state checked before this public package",
            "",
            f"Checked at: {GMAIL_CHECK['checked_at']}",
            "",
            "Threads checked:",
            "",
        ]
    )
    lines.extend(f"{index}. `{thread}` checked, no new route owner reply." for index, thread in enumerate(GMAIL_CHECK["threads"], start=1))
    lines.extend(
        [
            "",
            f"Reply state: {GMAIL_CHECK['result']}",
            "",
            "Targeted inbox searches by recipient, institution, subject keyword, route owner wording, funding route wording, and repository name found no separate new route owner reply.",
            "",
            "## Boundary",
            "",
        ]
    )
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Next action",
            "",
            "If a real route owner replies, convert that reply into a gate specific fit note before any new public package.",
            "",
            "If no reply exists, the useful private next step is a one page decision note for Goktug listing whether he wants to keep 1711 as an education adjacent scouting lane or close it until a demand owner appears.",
            "",
            "## Runnable check",
            "",
            "```bash",
            "make tubitak_1711_consortium_readiness_no_partner_gate",
            "```",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_json()
    write_doc()
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"facts={len(OFFICIAL_FACTS)}")
    print(f"gates={len(READINESS_GATES)}")


if __name__ == "__main__":
    main()
