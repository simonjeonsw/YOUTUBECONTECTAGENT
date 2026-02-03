from agent.main_agent import MainAgent


def main():
    """
    Entry point for YouTube Content Agent.
    """

    decision_policy = {
    "max_ctr_retries": 3,
    "max_eval_retries": 2
    }

    user_goal = {
        "topic": "Short-form dopamine addiction",
        "target_audience": "YouTube Shorts viewers",
        "constraints": {},
        "framing_clear": False,
    }

    agent = MainAgent(decision_policy=decision_policy)

    result = agent.run(user_goal)

    print("\n=== FINAL OUTPUT ===")
    print(result)


if __name__ == "__main__":
    main()
