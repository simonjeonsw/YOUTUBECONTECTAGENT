# /skills/research_skill.py

from typing import Dict, Any


def research_skill(input_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Lightweight credibility layer.
    Supports script authority and emotional grounding.
    Not a deep research engine.
    """

    click_thesis: str = input_data["click_thesis"]
    top_title: str = input_data["top_title"]
    top_hook: str = input_data["top_hook"]

    supporting_fact = (
        "Multiple studies and repeated real-world patterns show this behavior "
        "emerges far more often than people assume."
    )

    credibility_boost = (
        "This isn’t speculation — it’s a consistently observed outcome."
    )

    context_note = (
        "The topic attracts attention because it contradicts common beliefs "
        "while remaining uncomfortably relatable."
    )

    return {
        "supporting_fact": supporting_fact,
        "credibility_boost": credibility_boost,
        "context_note": context_note
    }
