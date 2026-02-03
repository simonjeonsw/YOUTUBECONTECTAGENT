# agent/controller.py
from typing import Dict, Any

from agent.main_agent import MainAgent
from agent.decision_engine import DecisionEngine
from memory.memory_store import MemoryStore


class AgentController:
    """
    Top-level runtime controller.
    Owns memory + policy + agent lifecycle.
    """

    def __init__(self, decision_policy: Dict[str, Any]):
        self.memory = MemoryStore()
        self.decision_engine = DecisionEngine(decision_policy)
        self.agent = MainAgent(
            decision_engine=self.decision_engine,
            memory_store=self.memory,
        )

    def run(self, user_goal: Dict[str, Any]) -> Dict[str, Any]:
        return self.agent.run(user_goal)
