# core/skills/script_skill.py

from typing import Dict, Any


def script_skill(input_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates a structured video script optimized for retention.
    """

    click_thesis = input_data["click_thesis"]
    top_hook = input_data["top_hook"]
    top_title = input_data["top_title"]
    supporting_fact = input_data["supporting_fact"]
    credibility_boost = input_data["credibility_boost"]
    context_note = input_data["context_note"]

    opening = (
        f"{top_hook} "
        "And once you see it, you can't unsee it."
    )

    body = (
        f"Most people assume this is harmless. "
        f"But {supporting_fact} "
        f"{credibility_boost} "
        f"{context_note}"
    )

    payoff = (
        "So the real question is not whether this exists, "
        "but how often it's quietly shaping your decisions without you noticing."
    )

    full_script = (
        f"TITLE: {top_title}\n\n"
        f"OPENING:\n{opening}\n\n"
        f"BODY:\n{body}\n\n"
        f"PAYOFF:\n{payoff}"
    )

    return {
        "opening": opening,
        "body": body,
        "payoff": payoff,
        "full_script": full_script
    }
