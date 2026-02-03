# core/skills/research_skill.py

from typing import Dict, Any


def research_skill(input_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Minimal research layer to support CTR-driven content.
    Focuses on credibility, not depth.
    """

    click_thesis = input_data["click_thesis"]
    top_title = input_data["top_title"]
    top_hook = input_data["top_hook"]

    supporting_fact = (
        "Multiple studies and real-world cases show this pattern appears "
        "more frequently than most people expect."
    )

    credibility_boost = (
        "This isn’t an opinion — it’s a consistently observed behavior."
    )

    context_note = (
        "The topic triggers attention because it contradicts common assumptions "
        "while remaining relatable to everyday experience."
    )

    return {
        "supporting_fact": supporting_fact,
        "credibility_boost": credibility_boost,
        "context_note": context_note
    }
