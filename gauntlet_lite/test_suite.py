"""
Test suite for GauntletFuse Phase 0 (Lite)

Run this file to verify that all components are working correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gauntlet_lite import BotAgent, ConversationContext, ConversationController, Message


def test_message_creation():
    """Test Message class creation and methods."""
    print("Testing Message creation...", end=" ")

    msg = Message(from_="bot1", content="Hello", to="bot2")
    assert msg.from_ == "bot1"
    assert msg.content == "Hello"
    assert msg.to == "bot2"
    assert msg.id is not None
    assert msg.timestamp is not None

    # Test repr with short and long content
    short = Message(from_="bot", content="Hi")
    assert "Hi" in repr(short)

    long = Message(from_="bot", content="x" * 100)
    assert "..." in repr(long)

    print("✓")


def test_conversation_context():
    """Test ConversationContext management."""
    print("Testing ConversationContext...", end=" ")

    context = ConversationContext()
    assert len(context) == 0

    msg1 = Message(from_="user", content="Hello")
    context.add_message(msg1)
    assert len(context) == 1
    assert "user" in context.participants

    msg2 = Message(from_="bot", content="Hi there")
    context.add_message(msg2)
    assert len(context) == 2

    last = context.get_last_message()
    assert last.from_ == "bot"

    history = context.get_history_for_llm("bot")
    assert len(history) == 2

    context.clear()
    assert len(context) == 0

    print("✓")


def test_bot_agent():
    """Test BotAgent creation and behavior."""
    print("Testing BotAgent...", end=" ")

    bot = BotAgent(id="test-bot", name="TestBot", prompt="You are a test bot.", temperature=0.7, use_llm=False)

    assert bot.id == "test-bot"
    assert bot.name == "TestBot"
    assert len(bot.memory) == 0

    # Test response generation
    context = ConversationContext()
    msg = Message(from_="user", content="Test message")
    context.add_message(msg)

    response = bot.respond(msg, context)
    assert response.from_ == "TestBot"
    assert len(response.content) > 0
    assert len(bot.memory) == 2  # Input + response

    print("✓")


def test_bot_should_respond():
    """Test bot response logic."""
    print("Testing bot response logic...", end=" ")

    bot = BotAgent("bot1", "Bot1", "Test", use_llm=False)
    context = ConversationContext()

    # Should respond to messages from others
    msg1 = Message(from_="user", content="Hello")
    assert bot.should_respond(msg1, context) == True

    # Should not respond to own messages (by name)
    msg2 = Message(from_="Bot1", content="Test")
    assert bot.should_respond(msg2, context) == False

    # Should not respond to own messages (by ID)
    msg3 = Message(from_="bot1", content="Test")
    assert bot.should_respond(msg3, context) == False

    # Should not respond if just responded
    context.add_message(Message(from_="user", content="Hi"))
    context.add_message(Message(from_="Bot1", content="Response"))
    msg4 = Message(from_="user", content="Another message")
    assert bot.should_respond(msg4, context) == False

    print("✓")


def test_conversation_controller():
    """Test ConversationController orchestration."""
    print("Testing ConversationController...", end=" ")

    controller = ConversationController()

    bot1 = BotAgent("b1", "Bot1", "Test bot 1", use_llm=False)
    bot2 = BotAgent("b2", "Bot2", "Test bot 2", use_llm=False)

    controller.register_bot(bot1)
    controller.register_bot(bot2)

    assert len(controller.bots) == 2
    assert len(controller.turn_order) == 2

    # Test message addition
    msg = Message(from_="user", content="Hello")
    controller.add_message(msg)
    assert len(controller.context) == 1

    # Test turn processing
    response = controller.process_turn()
    assert response is not None
    assert len(controller.context) == 2

    print("✓")


def test_conversation_flow():
    """Test full conversation flow."""
    print("Testing conversation flow...", end=" ")

    controller = ConversationController()

    bot1 = BotAgent("b1", "Alice", "Pragmatic bot", use_llm=False)
    bot2 = BotAgent("b2", "Bob", "Creative bot", use_llm=False)

    controller.register_bot(bot1)
    controller.register_bot(bot2)

    # Run conversation
    controller.run_conversation(initial_message="Let's discuss testing.", max_turns=4, verbose=False)

    # Should have initial message + 4 bot responses
    assert len(controller.context) >= 5
    assert "user" in controller.context.participants
    assert "Alice" in controller.context.participants
    assert "Bob" in controller.context.participants

    print("✓")


def test_broadcast_message():
    """Test broadcast messaging."""
    print("Testing broadcast messaging...", end=" ")

    controller = ConversationController()

    bot1 = BotAgent("b1", "Bot1", "Test", use_llm=False)
    bot2 = BotAgent("b2", "Bot2", "Test", use_llm=False)

    controller.register_bot(bot1)
    controller.register_bot(bot2)

    responses = controller.broadcast_message("Hello everyone!")

    # Both bots should respond
    assert len(responses) == 2
    assert responses[0].from_ in ["Bot1", "Bot2"]
    assert responses[1].from_ in ["Bot1", "Bot2"]

    print("✓")


def test_conversation_summary():
    """Test conversation summary generation."""
    print("Testing conversation summary...", end=" ")

    controller = ConversationController()
    bot = BotAgent("b1", "Bot1", "Test", use_llm=False)
    controller.register_bot(bot)

    controller.run_conversation("Test", max_turns=2, verbose=False)

    summary = controller.get_conversation_summary()
    assert "CONVERSATION SUMMARY" in summary
    assert "Total messages:" in summary
    assert "Bot1" in summary

    print("✓")


def test_reset_functionality():
    """Test conversation reset."""
    print("Testing reset functionality...", end=" ")

    controller = ConversationController()
    bot = BotAgent("b1", "Bot1", "Test", use_llm=False)
    controller.register_bot(bot)

    controller.run_conversation("Test", max_turns=3, verbose=False)
    assert len(controller.context) > 0
    assert len(bot.memory) > 0

    controller.reset()
    assert len(controller.context) == 0
    assert len(bot.memory) == 0

    print("✓")


def test_targeted_messaging():
    """Test targeted message routing."""
    print("Testing targeted messaging...", end=" ")

    controller = ConversationController()

    bot1 = BotAgent("b1", "Bot1", "Test", use_llm=False)
    bot2 = BotAgent("b2", "Bot2", "Test", use_llm=False)

    controller.register_bot(bot1)
    controller.register_bot(bot2)

    # Send message to specific bot
    msg = Message(from_="user", content="Bot1, respond", to="Bot1")
    controller.add_message(msg)

    # Process Bot1's turn
    response = controller.process_turn("b1")
    assert response is not None
    assert response.from_ == "Bot1"

    print("✓")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "=" * 70)
    print("GauntletFuse Phase 0 - Test Suite")
    print("=" * 70 + "\n")

    test_functions = [
        test_message_creation,
        test_conversation_context,
        test_bot_agent,
        test_bot_should_respond,
        test_conversation_controller,
        test_conversation_flow,
        test_broadcast_message,
        test_conversation_summary,
        test_reset_functionality,
        test_targeted_messaging,
    ]

    failed = 0
    for test_func in test_functions:
        try:
            test_func()
        except Exception as e:
            print(f"✗ FAILED: {e}")
            failed += 1

    print("\n" + "=" * 70)
    if failed == 0:
        print("ALL TESTS PASSED ✅")
        print("=" * 70)
        print("\nGauntletFuse Phase 0 is working correctly!")
        return 0
    else:
        print(f"{failed} TEST(S) FAILED ❌")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
