# skills/ctr_adjuster.py

from typing import Dict, List, Optional


def adjust_ctr_output(
    ctr_output: Dict[str, List[str]],
    viewer_intent: Optional[Dict] = None
) -> Dict[str, List[str]]:
    """
    Adjusts / reorders CTR candidates based on viewer intent signals.
    Safe to skip if viewer_intent is None.
    """

    if not viewer_intent:
        return ctr_output

    risk = viewer_intent.get("risk_level", "medium")
    curiosity = viewer_intent.get("curiosity_type", "general")

    def score(text: str) -> int:
        s = 0
        if risk == "high" and any(w in text.lower() for w in ["mistake", "trap", "destroy"]):
            s += 2
        if curiosity == "why-driven" and "why" in text.lower():
            s += 1
        return s

    return {
        "hooks": sorted(ctr_output["hooks"], key=score, reverse=True),
        "titles": sorted(ctr_output["titles"], key=score, reverse=True),
        "thumbnail_texts": sorted(ctr_output["thumbnail_texts"], key=score, reverse=True),
    }
