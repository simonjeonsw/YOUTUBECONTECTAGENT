# /skills/script_skill.py

from typing import Dict, Any


def script_skill(input_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates a structured video script optimized for retention.
    """

    click_thesis: str = input_data["click_thesis"]
    top_hook: str = input_data["top_hook"]
    top_title: str = input_data["top_title"]

    supporting_fact: str = input_data["supporting_fact"]
    credibility_boost: str = input_data["credibility_boost"]
    context_note: str = input_data["context_note"]

    opening = (
        f"{top_hook} "
        "And once you notice it, you can’t unsee it."
    )

    body = (
        "Most people assume this is harmless. "
        f"But {supporting_fact} "
        f"{credibility_boost} "
        f"{context_note}"
    )

    payoff = (
        "So the real question isn’t whether this exists, "
        "but how often it quietly shapes your decisions without you realizing it."
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
