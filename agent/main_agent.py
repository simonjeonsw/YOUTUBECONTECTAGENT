# agent/main_agent.py

from typing import Dict, Any, Optional

# --- Skill Interfaces (to be implemented separately) ---

def research_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def ctr_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def script_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


def eval_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError


# --- Main Agent ---

class MainAgent:
    def __init__(self, decision_policy: Dict[str, Any]):
        self.policy = decision_policy

    # -------- Core Flow --------

    def run(self, user_goal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates the full pipeline:
        Research → ClickThesis → CTR → Script → Eval → Retry
        """

        # 1. Research (optional)
        research = None
        if self._should_run_research(user_goal):
            research = research_skill({
                "topic": user_goal.get("topic"),
                "target_audience": user_goal.get("target_audience"),
                "constraints": user_goal.get("constraints")
            })

        # 2. Click Thesis
        click_thesis = self._generate_click_thesis(user_goal, research)

        # 3. CTR Loop
        ctr_output = self._run_ctr_with_retry(click_thesis, research)

        # 4. Select strongest candidates (simple heuristic v1)
        selected = self._select_best_ctr_candidate(ctr_output)

        # 5. Script
        script = script_skill({
            "selected_hook": selected["hook"],
            "selected_title": selected["title"],
            "click_thesis": click_thesis
        })

        # 6. Final Eval
        evaluation = eval_skill({
            "click_thesis": click_thesis,
            "hook": selected["hook"],
            "title": selected["title"],
            "thumbnail_text": selected["thumbnail_text"],
            "script": script["script"]
        })

        if evaluation["result"] == "FAIL":
            return {
                "status": "FAIL",
                "reason": evaluation["failure_reason"],
                "best_attempt": {
                    "click_thesis": click_thesis,
                    "hook": selected["hook"],
                    "title": selected["title"],
                    "thumbnail_text": selected["thumbnail_text"],
                    "script": script["script"]
                }
            }

        return {
            "status": "PASS",
            "output": {
                "click_thesis": click_thesis,
                "hook": selected["hook"],
                "title": selected["title"],
                "thumbnail_text": selected["thumbnail_text"],
                "script": script["script"],
                "confidence": evaluation["confidence"]
            }
        }

    # -------- Decision Logic --------

    def _should_run_research(self, user_goal: Dict[str, Any]) -> bool:
        return not user_goal.get("framing_clear", False)

    def _generate_click_thesis(
        self,
        user_goal: Dict[str, Any],
        research: Optional[Dict[str, Any]]
    ) -> str:
        """
        ClickThesis is a logical artifact.
        For now, generated inline (later can be its own Skill).
        """

        topic = user_goal.get("topic", "")
        pain = ""
        if research:
            pain = research.get("audience_pain", [""])[0]

        thesis = (
            f"Most people think {topic} is harmless, "
            f"but this video shows why it quietly causes {pain}."
        )

        # Basic validation
        if thesis.count(".") != 1:
            raise ValueError("Invalid ClickThesis: must be single sentence")

        return thesis

    def _run_ctr_with_retry(
        self,
        click_thesis: str,
        research: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        retries = 0

        while retries < self.policy.get("max_ctr_retries", 3):
            ctr_output = ctr_skill({
                "click_thesis": click_thesis,
                "research": research
            })

            if self._is_ctr_output_valid(ctr_output):
                return ctr_output

            retries += 1

        raise RuntimeError("CTRSkill failed after max retries")

    def _is_ctr_output_valid(self, ctr_output: Dict[str, Any]) -> bool:
        return (
            len(ctr_output.get("hooks", [])) >= 5 and
            len(ctr_output.get("titles", [])) >= 5 and
            len(ctr_output.get("thumbnail_texts", [])) >= 5
        )

    def _select_best_ctr_candidate(self, ctr_output: Dict[str, Any]) -> Dict[str, str]:
        """
        v1 heuristic:
        - shortest thumbnail
        - most provocative hook (length-based proxy)
        """

        hook = sorted(ctr_output["hooks"], key=len, reverse=True)[0]
        title = ctr_output["titles"][0]
        thumbnail = sorted(ctr_output["thumbnail_texts"], key=len)[0]

        return {
            "hook": hook,
            "title": title,
            "thumbnail_text": thumbnail
        }
