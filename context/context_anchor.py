# core/context/context_anchor.py

from typing import Dict, Any
import json
from datetime import datetime


def create_context_snapshot(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates an immutable context snapshot for a content package.
    """

    snapshot = {
        "project_id": input_data["project_id"],
        "content_id": input_data["content_id"],
        "created_at": datetime.utcnow().isoformat(),

        "click_thesis": input_data["click_thesis"],

        "decisions": {
            "selected_title": input_data["selected_title"],
            "selected_hook": input_data["selected_hook"],
            "selected_thumbnail_text": input_data["selected_thumbnail_text"],
        },

        "pipeline_state": {
            "ctr_generated": True,
            "eval_passed": True,
            "ranked": True,
            "researched": True,
            "scripted": True,
            "packaged": True
        },

        "rationale": {
            "why_this_title": input_data.get(
                "why_this_title",
                "Highest combined emotional clarity and curiosity."
            ),
            "why_this_hook": input_data.get(
                "why_this_hook",
                "Strong contrast and immediate attention trigger."
            ),
            "why_this_thumbnail": input_data.get(
                "why_this_thumbnail",
                "Short, emotional, and visually readable."
            )
        }
    }

    return snapshot


def serialize_snapshot(snapshot: Dict[str, Any]) -> str:
    """
    Serializes snapshot to JSON string for storage.
    """
    return json.dumps(snapshot, indent=2)
