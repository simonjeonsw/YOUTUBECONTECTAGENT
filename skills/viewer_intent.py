# /skills/viewer_intent.py

from typing import Dict


INTENT_TAXONOMY = {
    "curiosity": ["why", "hidden", "secret"],
    "fear_correction": ["mistake", "wrong", "trap", "danger"],
    "authority": ["fact", "truth", "study"],
}


def viewer_intent_score(
    candidate: Dict[str, str],
    target_intent: str,
) -> float:
    """
    Phase2-2:
    - Soft influence only
    - Never filters candidates
    """

    keywords = INTENT_TAXONOMY.get(target_intent, [])
    if not keywords:
        return 0.0

    text = f"{candidate['hook']} {candidate['title']}".lower()
    hits = sum(1 for k in keywords if k in text)

    return hits / len(keywords)
