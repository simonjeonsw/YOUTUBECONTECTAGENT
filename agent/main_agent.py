from typing import Dict, Any, Optional, List

from context.context_anchor import create_context_snapshot
from agent.decision_engine import DecisionEngine
from memory.memory_store import MemoryStore
from skills.viewer_intent import viewer_intent_score
from skills.evaluator import eval_skill


# --- Skill Interfaces (Injected later) ---

def research_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def ctr_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def script_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


class MainAgent:
    """
    Phase2-3 MainAgent
    - Memory-aware
    - DecisionEngine-driven
    - Failure-learning enabled
    """

    def __init__(self, decision_policy: Dict[str, Any]):
        self.decision_policy = decision_policy
        self.decision_engine = DecisionEngine(decision_policy)
        self.memory = MemoryStore()

    # =========================
    # Public Entry
    # =========================

    def run(self, user_goal: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Research (optional)
        research_result = None
        if not user_goal.get("framing_clear", False):
            research_result = research_skill({
                "topic": user_goal.get("topic"),
                "target_audience": user_goal.get("target_audience"),
                "constraints": user_goal.get("constraints"),
            })

        # 2. Click Thesis
        click_thesis = self._build_click_thesis(user_goal, research_result)

        # 3. Generate CTR candidates
        ctr_output = ctr_skill({
            "click_thesis": click_thesis,
            "research": research_result,
        })

        # 4. Evaluate → build candidate objects
        evaluated_candidates = self._build_evaluated_candidates(
            ctr_output=ctr_output,
            user_goal=user_goal,
        )

        if not evaluated_candidates:
            self.memory.log_failure(
                snapshot={"click_thesis": click_thesis},
                reason="No candidates passed evaluation",
            )
            return {
                "status": "FAIL",
                "reason": "No valid CTR candidates",
            }

        # 5. DecisionEngine selection (policy + memory + intent)
        selected = self.decision_engine.select(
            evaluated_candidates=evaluated_candidates,
            channel_state=self.memory.get_channel_state(),
        )

        # 6. Script
        script_output = script_skill({
            "click_thesis": click_thesis,
            "top_hook": selected["hook"],
            "top_title": selected["title"],
            **(research_result or {}),
        })

        # 7. Snapshot + Memory log
        snapshot = create_context_snapshot({
            "project_id": user_goal.get("project_id", "yt-agent"),
            "content_id": user_goal.get("content_id", "content-001"),
            "click_thesis": click_thesis,
            "selected_title": selected["title"],
            "selected_hook": selected["hook"],
            "selected_thumbnail_text": selected["thumbnail_text"],
        })

        self.memory.log_execution(snapshot)

        return {
            "status": "PASS",
            "output": {
                "click_thesis": click_thesis,
                **selected,
                "script": script_output.get("full_script"),
                "context_snapshot": snapshot,
            },
        }

    # =========================
    # Internal helpers
    # =========================

    def _build_click_thesis(
        self,
        user_goal: Dict[str, Any],
        research_result: Optional[Dict[str, Any]],
    ) -> str:
        topic = user_goal.get("topic", "")
        pain = ""

        if research_result:
            pain = research_result.get("audience_pain", [""])[0]

        thesis = (
            f"Most people think {topic} is harmless, "
            f"but it quietly leads to {pain}."
        )

        if thesis.count(".") != 1:
            raise ValueError("ClickThesis must be exactly one sentence.")

        return thesis

    def _build_evaluated_candidates(
        self,
        ctr_output: Dict[str, Any],
        user_goal: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Converts raw CTR output into DecisionEngine-ready items.
        """

        candidates = []

        for hook, title, thumbnail in zip(
            ctr_output.get("hooks", []),
            ctr_output.get("titles", []),
            ctr_output.get("thumbnail_texts", []),
        ):
            evaluation = eval_skill({
                "hook": hook,
                "title": title,
                "thumbnail_text": thumbnail,
            })

            if evaluation.get("result") != "PASS":
                continue

            candidates.append({
                "candidate": {
                    "hook": hook,
                    "title": title,
                    "thumbnail_text": thumbnail,
                },
                "evaluation": evaluation,
                "intent_score": viewer_intent_score(user_goal),
                "fatigue_penalty": self.memory.fatigue_penalty({
                    "hook": hook,
                    "title": title,
                }),
            })

        return candidates
