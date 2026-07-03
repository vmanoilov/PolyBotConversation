"""
Main demo script for GauntletFuse - Phase 0 (Lite)

Demonstrates a working multi-bot conversation with:
- Multiple bots with different personalities
- Bot-to-bot communication
- Maintained conversation context
- Clear identity and role management
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path to import gauntlet_lite
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

from gauntlet_lite import BotAgent, ConversationController


def create_demo_bots(use_llm=False):
    """
    Create demo bots with different personalities.

    Args:
        use_llm: Whether to use real LLM (requires OPENAI_API_KEY) or mock responses

    Returns:
        List of BotAgent instances
    """
    bot_alpha = BotAgent(
        id="bot-alpha",
        name="Alpha",
        prompt="""You are Alpha, a pragmatic and analytical bot. 
You focus on practical solutions and logical analysis. 
You prefer concrete examples and tend to be direct and concise.
You value efficiency and clear thinking.""",
        temperature=0.7,
        use_llm=use_llm,
    )

    bot_beta = BotAgent(
        id="bot-beta",
        name="Beta",
        prompt="""You are Beta, a creative and exploratory bot.
You enjoy thinking about possibilities and alternative perspectives.
You tend to ask questions and challenge assumptions in a constructive way.
You value innovation and creative problem-solving.""",
        temperature=0.9,
        use_llm=use_llm,
    )

    bot_gamma = BotAgent(
        id="bot-gamma",
        name="Gamma",
        prompt="""You are Gamma, a balanced and diplomatic bot.
You try to find common ground and synthesize different viewpoints.
You're good at seeing both sides of an issue.
You value collaboration and consensus-building.""",
        temperature=0.8,
        use_llm=use_llm,
    )

    return [bot_alpha, bot_beta, bot_gamma]


def demo_simple_conversation():
    """Demo: Simple round-robin conversation."""
    print("\n" + "=" * 70)
    print("DEMO 1: Simple Round-Robin Conversation")
    print("=" * 70)
    print("Three bots discussing a topic with fixed turn-taking.\n")

    # Create controller and bots
    controller = ConversationController()
    bots = create_demo_bots(use_llm=False)  # Use mock responses

    # Register bots
    for bot in bots:
        controller.register_bot(bot)

    # Run conversation
    controller.run_conversation(initial_message="Let's discuss the future of artificial intelligence and how it might impact society.", max_turns=6, verbose=True)


def demo_targeted_conversation():
    """Demo: Conversation with explicit bot addressing."""
    print("\n" + "=" * 70)
    print("DEMO 2: Multi-Turn Conversation")
    print("=" * 70)
    print("Multiple rounds of bot interactions.\n")

    # Create controller and bots (only 2 for this demo)
    controller = ConversationController()
    bots = create_demo_bots(use_llm=False)[:2]  # Just Alpha and Beta

    # Register bots
    for bot in bots:
        controller.register_bot(bot)

    # First topic
    print("\n--- Round 1: Initial Topic ---\n")
    controller.run_conversation(initial_message="What are the key challenges in building reliable AI systems?", max_turns=4, verbose=True)

    # Follow-up topic
    print("\n--- Round 2: Follow-up Question ---\n")
    from gauntlet_lite.models import Message

    follow_up = Message(from_="user", content="How would you prioritize these challenges?")
    controller.add_message(follow_up)
    print(f"[user]: {follow_up.content}\n")

    # Continue conversation
    for _ in range(4):
        response = controller.process_turn()
        if response:
            print(f"{response}\n")


def demo_conversation_summary():
    """Demo: Conversation with summary at the end."""
    print("\n" + "=" * 70)
    print("DEMO 3: Conversation with Summary")
    print("=" * 70)
    print("Running a conversation and displaying a summary.\n")

    # Create controller with all bots
    controller = ConversationController()
    bots = create_demo_bots(use_llm=False)

    for bot in bots:
        controller.register_bot(bot)

    # Run conversation (less verbose this time)
    controller.run_conversation(initial_message="What makes a good software architecture?", max_turns=6, verbose=False)

    # Print summary
    print(controller.get_conversation_summary())


def demo_with_llm():
    """Demo: Conversation using real LLM (requires OPENAI_API_KEY)."""
    print("\n" + "=" * 70)
    print("DEMO 4: Conversation with Real LLM")
    print("=" * 70)
    print("Using actual OpenAI API for responses.")
    print("NOTE: Requires OPENAI_API_KEY environment variable to be set.\n")

    # Create controller with LLM-enabled bots
    controller = ConversationController()
    bots = create_demo_bots(use_llm=True)[:2]  # Just 2 bots to save API calls

    for bot in bots:
        controller.register_bot(bot)

    # Run shorter conversation to save API costs
    controller.run_conversation(initial_message="What's more important in software: simplicity or flexibility?", max_turns=4, verbose=True)


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  GauntletFuse - Phase 0 (Lite)".center(68) + "║")
    print("║" + "  Multi-Bot Conversation Framework Demo".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")

    # Run demos
    demo_simple_conversation()

    input("\n\nPress Enter to continue to Demo 2...")
    demo_targeted_conversation()

    input("\n\nPress Enter to continue to Demo 3...")
    demo_conversation_summary()

    # Ask about LLM demo
    print("\n" + "=" * 70)
    response = input("\nWould you like to try Demo 4 with real LLM? (requires OPENAI_API_KEY) [y/N]: ")
    if response.lower() in ["y", "yes"]:
        demo_with_llm()
    else:
        print("\nSkipping LLM demo. Set OPENAI_API_KEY environment variable to enable.")

    print("\n" + "=" * 70)
    print("All demos complete!")
    print("=" * 70 + "\n")

    print("\nTo add your own bot:")
    print("  1. Create a BotAgent with a unique ID, name, and personality prompt")
    print("  2. Register it with a ConversationController")
    print("  3. Call run_conversation() or process_turn()")
    print("\nSee README.md for more details.\n")


if __name__ == "__main__":
    main()
