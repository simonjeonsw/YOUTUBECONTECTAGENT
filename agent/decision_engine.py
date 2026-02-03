# agent/decision_engine.py

from typing import Dict, Any, List


class DecisionEngine:
    """
    Phase2 Decision Engine

    - Single source of truth for selection
    - Policy-weighted
    - Memory-aware (fatigue)
    """
    """
    Phase2-3 Decision Engine
    - Policy-weighted
    - Memory-aware
    - Channel-state biased
    """

    def __init__(self, policy: Dict[str, Any]):
        self.policy = policy

    def select(
        self,
        evaluated_candidates: List[Dict[str, Any]],
        channel_state: Dict[str, Any],
    ) -> Dict[str, str]:

        scored = []

        dominant_angle = channel_state.get("dominant_angle")

        for item in evaluated_candidates:
            signals = item["evaluation"]["signals"]
            intent_score = item.get("intent_score", 0.0)
            fatigue_penalty = item.get("fatigue_penalty", 0.0)

            base_score = (
                signals.get("emotion", 0.0) * self.policy.get("emotion_weight", 1.0)
                + signals.get("clarity", 0.0) * self.policy.get("clarity_weight", 1.0)
                + signals.get("novelty", 0.0) * self.policy.get("novelty_weight", 1.0)
                + intent_score * self.policy.get("intent_weight", 1.0)
            )

            # --- Channel Bias ---
            angle = item["evaluation"]["signals"].get("angle")
            angle_bonus = 0.0

            if dominant_angle and angle == dominant_angle:
                angle_bonus = self.policy.get("dominant_angle_bonus", 0.2)

            final_score = base_score + angle_bonus - fatigue_penalty

            scored.append((final_score, item["candidate"]))

        if not scored:
            raise ValueError("No candidates to select.")

        return max(scored, key=lambda x: x[0])[1]
