#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TEKNOFEST_PUBLIC_SHARE_CLEARANCE_PACKET_20260618.md"
DATA = ROOT / "docs" / "teknofest_public_share_clearance_packet_20260618.json"


SOURCE_FACTS = [
    {
        "fact_id": "TPSCP001",
        "source": "TEKNOFEST Sağlıkta Yapay Zeka Yarışması",
        "url": "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
        "checked_fact": "The public page says the competition aims to support AI solutions for health problems and increase knowledge and trained workforce.",
        "share_value": "A public safety checklist fits the education and workforce readiness aim without claiming official status.",
    },
    {
        "fact_id": "TPSCP002",
        "source": "TEKNOFEST Sağlıkta Yapay Zeka Yarışması",
        "url": "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
        "checked_fact": "The public page says university and above teams develop AI models that predict whether genetic variants are pathogenic or benign.",
        "share_value": "The share can focus on variant label uncertainty, leakage, population limits, source support, and human review.",
    },
    {
        "fact_id": "TPSCP003",
        "source": "TEKNOFEST Sağlıkta Yapay Zeka Yarışması",
        "url": "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
        "checked_fact": "The public page lists the project detail report deadline as 29 June 2026 at 17:00.",
        "share_value": "The time window supports a concise public share if Dr. Ozkan clears it.",
    },
    {
        "fact_id": "TPSCP004",
        "source": "Medical AI Failure Atlas public repository",
        "url": "https://github.com/v0id-lab/medical-ai-failure-atlas",
        "checked_fact": "The repository contains a TEKNOFEST Health AI Safety Addendum and Goktug Field Action Review Packet.",
        "share_value": "The share can point to existing public artifacts rather than inventing new authority.",
    },
]


SHARE_OPTIONS = [
    {
        "option_id": "TPSCO001",
        "name": "Short public post",
        "channel": "Public social post",
        "text": "TEKNOFEST health AI teams preparing project detail reports may find this independent safety addendum useful. It focuses on genetic variant model risks: label uncertainty, leakage, source support, population limits, human review, and avoiding clinical deployment claims. This is not an official TEKNOFEST document.",
        "use_when": "Use if Dr. Ozkan wants maximum speed and low friction public visibility.",
        "clearance_needed": "Needs explicit public post clearance.",
    },
    {
        "option_id": "TPSCO002",
        "name": "Long public post",
        "channel": "LinkedIn style public post",
        "text": "For TEKNOFEST Sağlıkta Yapay Zeka teams working on genetic variant model projects, I prepared an independent safety addendum for project detail report review. The note is built for practical checks before claims are made: label uncertainty, leakage, source support, population and context limits, human review handoff, and clear boundaries against clinical deployment or validation claims. It is a public medical AI safety resource, not an official TEKNOFEST document and not a submission claim.",
        "use_when": "Use if Dr. Ozkan wants a more explanatory public positioning post.",
        "clearance_needed": "Needs explicit public post clearance.",
    },
    {
        "option_id": "TPSCO003",
        "name": "Repository only note",
        "channel": "GitHub only",
        "text": "This repository includes an independent TEKNOFEST health AI safety addendum for teams reviewing genetic variant model projects before the project detail report deadline. The note is for safety literacy and project review only.",
        "use_when": "Use if Dr. Ozkan wants visibility without social posting.",
        "clearance_needed": "No social post, but public repository wording still needs review before reuse.",
    },
]


BOUNDARIES = [
    "No public post is made.",
    "No email is sent.",
    "No submission is made.",
    "No application is submitted.",
    "No official TEKNOFEST role is claimed.",
    "No official TEKNOFEST endorsement is claimed.",
    "No team relationship is claimed.",
    "No finalist or score claim is made.",
    "No patient data is used.",
    "No clinical deployment is claimed.",
    "No clinical validation is claimed.",
    "No medical advice is given.",
    "No payment is made.",
    "No terms are accepted.",
]


def write_json() -> None:
    payload = {
        "artifact": "teknofest_public_share_clearance_packet_20260618",
        "status": "public_share_clearance_packet",
        "source_fact_count": len(SOURCE_FACTS),
        "share_option_count": len(SHARE_OPTIONS),
        "source_facts": SOURCE_FACTS,
        "share_options": SHARE_OPTIONS,
        "boundaries": BOUNDARIES,
        "recommended_option": "Short public post after Dr. Ozkan clearance",
        "requires_goktug_clearance_before_public_post": True,
        "contains_patient_data": False,
        "claims_submission": False,
        "claims_application": False,
        "claims_official_role": False,
        "claims_endorsement": False,
        "claims_team_relationship": False,
        "claims_clinical_validation": False,
        "claims_clinical_deployment": False,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines = [
        "# TEKNOFEST Public Share Clearance Packet",
        "",
        "Date: 2026 06 18",
        "",
        "Status: public share clearance packet.",
        "",
        "Purpose: prepare exact public share options for the TEKNOFEST Health AI Safety Addendum while blocking any post, email, submission, official role claim, endorsement claim, patient data use, clinical deployment claim, or clinical validation claim until Dr. Ozkan clears the action.",
        "",
        "## Recommendation",
        "",
        "Recommended action if cleared: use the short public post because the project detail report deadline is 29 June 2026 at 17:00 and the safety note can help teams quickly.",
        "",
        "Do not post anything from this packet without explicit clearance.",
        "",
        "## Source facts",
        "",
    ]
    for fact in SOURCE_FACTS:
        lines.extend(
            [
                f"### {fact['fact_id']}: {fact['source']}",
                "",
                f"Official or public source: {fact['url']}",
                "",
                f"Checked fact: {fact['checked_fact']}",
                "",
                f"Share value: {fact['share_value']}",
                "",
            ]
        )
    lines.extend(["## Share options for review", ""])
    for option in SHARE_OPTIONS:
        lines.extend(
            [
                f"### {option['option_id']}: {option['name']}",
                "",
                f"Channel: {option['channel']}",
                "",
                "Text candidate:",
                "",
                option["text"],
                "",
                f"Use when: {option['use_when']}",
                "",
                f"Clearance needed: {option['clearance_needed']}",
                "",
            ]
        )
    lines.extend(["## Boundary", ""])
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Clearance question",
            "",
            "Dr. Ozkan should choose one of four options: approve short public post, approve long public post, keep repository only, or do not share.",
            "",
            "## Runnable check",
            "",
            "```bash",
            "make teknofest_public_share_clearance_packet",
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
    print(f"source_facts={len(SOURCE_FACTS)}")
    print(f"share_options={len(SHARE_OPTIONS)}")


if __name__ == "__main__":
    main()
