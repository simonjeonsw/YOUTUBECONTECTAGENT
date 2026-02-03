# agent/planner_agent.py
from typing import Dict, List


class PlannerAgent:
    """
    Phase3:
    Plans multiple contents under a single meta-goal.
    """

    def __init__(self, meta_goal: Dict[str, Any], channel_state: Dict[str, Any]):
        self.meta_goal = meta_goal
        self.channel_state = channel_state

    def plan(self, slots: int = 3) -> List[Dict[str, Any]]:
        """
        Returns content briefs, not scripts.
        """
        plans = []

        for angle, ratio in self.meta_goal["angle_mix"].items():
            count = max(1, int(slots * ratio))
            for _ in range(count):
                plans.append({
                    "angle": angle,
                    "objective": self.meta_goal["primary_objective"],
                })

        return plans[:slots]
