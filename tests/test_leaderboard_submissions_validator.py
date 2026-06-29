from __future__ import annotations

from scripts.validate_leaderboard_submissions_v0_1 import MAX_SUBMISSIONS, validate_store


def valid_row(index: int) -> dict[str, object]:
    timestamp = f"2026-06-27T00:{index % 60:02d}:00Z"
    return {
        "id": f"row-{index}",
        "model_name": f"Model {index}",
        "huggingface_link": f"https://huggingface.co/org/model-{index}",
        "benchmark_scores": {
            "safety_score": 80,
            "source_support_score": 70,
            "clinical_boundary_score": 60,
        },
        "notes": "",
        "status": "pending review",
        "submitted_at": timestamp,
        "first_submitted_at": timestamp,
        "huggingface_reachable": True,
        "huggingface_status": "200",
    }


def test_validate_store_rejects_unbounded_submission_store() -> None:
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [valid_row(index) for index in range(MAX_SUBMISSIONS + 1)],
    }

    errors = validate_store(store)

    assert f"submissions must contain {MAX_SUBMISSIONS} rows or fewer" in errors
