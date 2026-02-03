# core/skills/packaging_skill.py

from typing import Dict, List, Any


def packaging_skill(input_data: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
    """
    Packages titles, thumbnail texts, and hooks into upload-ready variants.
    """

    hooks = input_data["hooks"]
    titles = input_data["titles"]
    thumbnails = input_data["thumbnail_texts"]
    full_script = input_data["full_script"]

    packages = []

    max_packages = min(3, len(hooks), len(titles), len(thumbnails))

    for i in range(max_packages):
        package = {
            "package_id": f"variant_{i+1}",
            "title": titles[i],
            "thumbnail_text": thumbnails[i],
            "opening_hook": hooks[i],
            "script": full_script
        }
        packages.append(package)

    return {
        "packages": packages
    }
