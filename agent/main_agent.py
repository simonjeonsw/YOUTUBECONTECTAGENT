from typing import Dict, Any, Optional
from context.context_anchor import create_context_snapshot

# --- Skill Interfaces (Injected later) ---

def research_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def ctr_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def script_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def eval_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


class MainAgent:
    """
    High-level orchestration agent.
    Owns flow control, retries, and final decisions.
    """

    def __init__(self, decision_policy: Dict[str, Any]):
        self.decision_policy = decision_policy

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

        # 3. CTR + Eval retry loop
        max_eval_retries = self.decision_policy.get("max_eval_retries", 2)
        eval_attempts = 0

        while eval_attempts < max_eval_retries:
            ctr_candidates = self._generate_ctr_candidates(
                click_thesis, research_result
            )
            selected = self._select_best_candidate(ctr_candidates)

            script_output = script_skill({
                "click_thesis": click_thesis,
                "top_title": selected["title"],
                "top_hook": selected["hook"],
                **(research_result or {}),
            })

            evaluation = eval_skill({
                "click_thesis": click_thesis,
                "hook": selected["hook"],
                "title": selected["title"],
                "thumbnail_text": selected["thumbnail_text"],
                "script": script_output.get("full_script"),
            })

            if evaluation.get("result") == "PASS":
                snapshot = create_context_snapshot({
                    "project_id": user_goal.get("project_id", "yt-agent"),
                    "content_id": user_goal.get("content_id", "content-001"),
                    "click_thesis": click_thesis,
                    "selected_title": selected["title"],
                    "selected_hook": selected["hook"],
                    "selected_thumbnail_text": selected["thumbnail_text"],
                })

                return {
                    "status": "PASS",
                    "output": {
                        "click_thesis": click_thesis,
                        **selected,
                        "script": script_output.get("full_script"),
                        "confidence": evaluation.get("confidence"),
                        "context_snapshot": snapshot,
                    }
                }

            eval_attempts += 1

        return {
            "status": "FAIL",
            "reason": "Evaluation failed after retries",
        }

    # -------- Helpers --------

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
            raise ValueError("ClickThesis must be one sentence.")

        return thesis

    def _generate_ctr_candidates(
        self,
        click_thesis: str,
        research_result: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return ctr_skill({
            "click_thesis": click_thesis,
            "research": research_result,
        })

    def _select_best_candidate(self, ctr_output: Dict[str, Any]) -> Dict[str, str]:
        return {
            "hook": max(ctr_output["hooks"], key=len),
            "title": ctr_output["titles"][0],
            "thumbnail_text": min(ctr_output["thumbnail_texts"], key=len),
        }
