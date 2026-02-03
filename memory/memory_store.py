# memory/memory_store.py

from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import Counter


class MemoryStore:
    """
    Phase2–3 Memory Store (Stable & Defensive)

    Responsibilities:
    - channel_state: strategic, slow-changing signals
    - history: append-only execution / failure log
    - pattern memory: fatigue & repetition signals (soft)
    """

    def __init__(self):
        # ---- Channel State (Strategic Summary) ----
        self.channel_state: Dict[str, Any] = {
            "dominant_angle": None,          # str | None
            "angle_counts": {},              # angle -> count
            "last_updated": None,
        }

        # ---- Execution History (Immutable log) ----
        self.history: List[Dict[str, Any]] = []

        # ---- Pattern Memory (Derived, non-authoritative) ----
        self._hook_counter = Counter()
        self._title_counter = Counter()

    # =====================================================
    # Channel State
    # =====================================================

    def update_angle(self, angle: str) -> None:
        """
        Update channel-level dominant angle.
        This is the ONLY place dominant_angle should change.
        """
        counts = self.channel_state["angle_counts"]
        counts[angle] = counts.get(angle, 0) + 1

        self.channel_state["dominant_angle"] = max(
            counts.items(), key=lambda x: x[1]
        )[0]

        self.channel_state["last_updated"] = datetime.utcnow().isoformat()

    def get_channel_state(self) -> Dict[str, Any]:
        return self.channel_state.copy()

    # =====================================================
    # Execution / Failure Logging
    # =====================================================

    def log_execution(
        self,
        snapshot: Dict[str, Any],
        angle: Optional[str] = None,
        status: str = "PASS",
        reason: Optional[str] = None,
    ) -> None:
        """
        Unified logging for PASS / FAIL.
        History is append-only.
        """

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "snapshot": snapshot,
        }

        if reason:
            record["reason"] = reason

        self.history.append(record)

        # ---- Pattern counters (Phase2-3 signals) ----
        hook = snapshot.get("selected_hook")
        title = snapshot.get("selected_title")

        if hook:
            self._hook_counter[hook] += 1
        if title:
            self._title_counter[title] += 1

        # ---- Strategic update ----
        if status == "PASS" and angle:
            self.update_angle(angle)

    def get_history(self) -> List[Dict[str, Any]]:
        # Defensive copy (do NOT allow mutation)
        return list(self.history)

    # =====================================================
    # Fatigue / Repetition Signals
    # =====================================================

    def fatigue_penalty(self, candidate: Dict[str, str]) -> float:
        """
        Soft penalty for repeated hook/title patterns.
        - Never blocks selection
        - DecisionEngine decides how to use it
        """

        hook = candidate.get("hook", "")
        title = candidate.get("title", "")

        hook_freq = self._hook_counter.get(hook, 0)
        title_freq = self._title_counter.get(title, 0)

        raw_penalty = 0.1 * (hook_freq + title_freq)

        # Hard cap to avoid runaway suppression
        return min(raw_penalty, 0.5)
