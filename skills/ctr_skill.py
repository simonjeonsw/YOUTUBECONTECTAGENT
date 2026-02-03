# core/skills/ctr_skill.py

from typing import Dict, Any, List


def ctr_skill(input_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Generates high-CTR hooks, titles, and thumbnail texts
    based on a single ClickThesis.
    """

    click_thesis = input_data["click_thesis"]

    # --- Hooks ---
    hooks = [
        f"Everyone thinks this is normal, but the truth behind it is disturbing.",
        f"This looks harmless, but it quietly destroys more than you think.",
        f"Nobody warns you about this part, and that’s the real problem.",
        f"Most people ignore this, and that mistake costs them years.",
        f"This is why smart people still fall into this trap."
    ]

    # --- Titles ---
    titles = [
        "The Hidden Cost Nobody Talks About",
        "Why This Seems Fine — Until It Isn’t",
        "This Quiet Problem Is Bigger Than You Think",
        "The Mistake Almost Everyone Makes",
        "What No One Tells You About This"
    ]

    # --- Thumbnail Texts ---
    thumbnail_texts = [
        "Nobody Warns You",
        "This Is The Trap",
        "Looks Safe",
        "Big Mistake",
        "Hidden Damage"
    ]

    return {
        "hooks": hooks,
        "titles": titles,
        "thumbnail_texts": thumbnail_texts
    }
