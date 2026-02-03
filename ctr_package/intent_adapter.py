# ctr_package/intent_adapter.py

def adapt_research_with_intent(research: dict, viewer_intent: dict | None) -> dict:
    """
    viewer_intent는 CTR의 '방향성 힌트'일 뿐이다.
    연구 결과를 수정하되, 절대 새로운 의미를 만들지 않는다.
    """

    if viewer_intent is None:
        return research

    adapted = research.copy()

    intent_tags = viewer_intent.get("intent_tags", [])
    risk_level = viewer_intent.get("risk_level")
    curiosity_type = viewer_intent.get("curiosity_type")

    # 예시: curiosity_type에 따라 우선순위 조정
    if curiosity_type == "implicit":
        adapted["curiosity_gaps"] = (
            adapted["curiosity_gaps"][:2]
            + adapted["controversial_angles"][:1]
        )

    if risk_level == "high":
        adapted["emotional_triggers"] = (
            ["위험", "손실", "실수"]
            + adapted["emotional_triggers"]
        )

    return adapted
