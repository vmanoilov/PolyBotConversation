"""
Simple example showing how to create and run a custom bot conversation.
This is the minimal code needed to get started with GauntletFuse Lite.
"""

import sys
from pathlib import Path

# Add parent directory to path to import gauntlet_lite
sys.path.insert(0, str(Path(__file__).parent.parent))

from gauntlet_lite import BotAgent, ConversationController


def main():
    """
    Create a simple 2-bot conversation about a topic.
    """

    # Step 1: Create bots with different personalities
    optimist = BotAgent(
        id="optimist-1",
        name="Optimist",
        prompt="You are an optimistic bot who sees the positive side of things. "
        "You're encouraging and forward-thinking.",
        use_llm=False,  # Use mock responses (no API key needed)
    )

    realist = BotAgent(
        id="realist-1",
        name="Realist",
        prompt="You are a realistic bot who focuses on practical concerns. "
        "You're grounded and analytical.",
        use_llm=False,
    )

    # Step 2: Create conversation controller
    controller = ConversationController()

    # Step 3: Register bots
    controller.register_bot(optimist)
    controller.register_bot(realist)

    # Step 4: Start conversation
    print("\n" + "=" * 60)
    print("Simple Bot Conversation Example")
    print("=" * 60 + "\n")

    controller.run_conversation(
        initial_message="What do you think about the future of technology?",
        max_turns=6,
        verbose=True,
    )

    # Optional: Print summary
    print("\n" + controller.get_conversation_summary())


if __name__ == "__main__":
    main()
