# core/skills/evaluator.py

from typing import Dict, List


EMOTION_WORDS = [
    "hidden", "mistake", "trap", "danger", "nobody",
    "secret", "problem", "wrong", "silent", "damage"
]


def contains_emotion(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in EMOTION_WORDS)


def eval_hook(hook: str) -> bool:
    if len(hook.split()) < 6:
        return False
    if not contains_emotion(hook):
        return False
    if "but" not in hook and "why" not in hook:
        return False
    return True


def eval_title(title: str) -> bool:
    if len(title) > 70:
        return False
    if not contains_emotion(title):
        return False
    if "about" in title and "why" not in title:
        return False
    return True


def eval_thumbnail(text: str) -> bool:
    if len(text.split()) > 4:
        return False
    if not contains_emotion(text):
        return False
    return True


def eval_skill(input_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Filters CTR candidates and returns only high-quality outputs.
    """

    hooks = [h for h in input_data["hooks"] if eval_hook(h)]
    titles = [t for t in input_data["titles"] if eval_title(t)]
    thumbnails = [t for t in input_data["thumbnail_texts"] if eval_thumbnail(t)]

    return {
        "hooks": hooks,
        "titles": titles,
        "thumbnail_texts": thumbnails
    }
