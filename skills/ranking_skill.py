# core/skills/ranking_skill.py

from typing import Dict, List


EMOTION_WORDS = [
    "hidden", "mistake", "trap", "danger", "nobody",
    "secret", "problem", "wrong", "silent", "damage"
]


def emotion_score(text: str) -> int:
    text = text.lower()
    return sum(1 for word in EMOTION_WORDS if word in text)


def hook_score(hook: str) -> int:
    score = emotion_score(hook)
    if "but" in hook.lower():
        score += 2
    if "why" in hook.lower():
        score += 1
    length = len(hook.split())
    if 8 <= length <= 16:
        score += 1
    return score


def title_score(title: str) -> int:
    score = emotion_score(title)
    if "why" in title.lower():
        score += 2
    if "how" in title.lower():
        score -= 1
    return score


def thumbnail_score(text: str) -> int:
    score = emotion_score(text)
    length = len(text.split())
    if length == 2 or length == 3:
        score += 2
    return score


def ranking_skill(input_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Ranks CTR candidates by relative click potential.
    """

    hooks = sorted(
        input_data["hooks"],
        key=hook_score,
        reverse=True
    )

    titles = sorted(
        input_data["titles"],
        key=title_score,
        reverse=True
    )

    thumbnails = sorted(
        input_data["thumbnail_texts"],
        key=thumbnail_score,
        reverse=True
    )

    return {
        "hooks": hooks,
        "titles": titles,
        "thumbnail_texts": thumbnails
    }
