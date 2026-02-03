# /skills/evaluator.py

from typing import Dict


EMOTION_WORDS = [
    "hidden", "mistake", "trap", "danger", "nobody",
    "secret", "problem", "wrong", "silent", "damage"
]


def _emotion_score(text: str) -> float:
    text = text.lower()
    return sum(1 for w in EMOTION_WORDS if w in text) / len(EMOTION_WORDS)


def _clarity_score(text: str) -> float:
    words = len(text.split())
    if words == 0:
        return 0.0
    return max(0.0, 1.0 - abs(words - 8) / 8)


def _novelty_score(text: str) -> float:
    text = text.lower()
    return 1.0 if ("but" in text or "why" in text) else 0.4


def eval_skill(input_data: Dict[str, str]) -> Dict[str, Dict[str, float]]:
    """
    Phase2-2:
    - No filtering
    - No PASS / FAIL
    - Only returns evaluation signals
    """

    hook = input_data.get("hook", "")
    title = input_data.get("title", "")
    thumbnail = input_data.get("thumbnail_text", "")

    combined = f"{hook} {title} {thumbnail}"

    return {
        "signals": {
            "emotion": _emotion_score(combined),
            "clarity": _clarity_score(title),
            "novelty": _novelty_score(hook),
        }
    }
