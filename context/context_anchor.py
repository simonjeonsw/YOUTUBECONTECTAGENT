from typing import Dict, Any
from datetime import datetime
import json


def create_context_snapshot(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates an immutable decision snapshot for one content unit.
    """

    snapshot = {
        "project_id": input_data["project_id"],
        "content_id": input_data["content_id"],
        "created_at": datetime.utcnow().isoformat(),

        "click_thesis": input_data["click_thesis"],

        "selected_assets": {
            "title": input_data["selected_title"],
            "hook": input_data["selected_hook"],
            "thumbnail_text": input_data["selected_thumbnail_text"],
        },

        "pipeline_state": {
            "researched": True,
            "ctr_generated": True,
            "ranked": True,
            "scripted": True,
            "evaluated": True,
            "packaged": True,
        },

        "rationale": {
            "title": input_data.get(
                "why_this_title",
                "Highest combined emotional clarity and curiosity."
            ),
            "hook": input_data.get(
                "why_this_hook",
                "Strong contrast and immediate attention trigger."
            ),
            "thumbnail": input_data.get(
                "why_this_thumbnail",
                "Short, emotional, and visually readable."
            ),
        },
    }

    return snapshot


def serialize_snapshot(snapshot: Dict[str, Any]) -> str:
    return json.dumps(snapshot, indent=2)
