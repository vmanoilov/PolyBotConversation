from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase

from chat.helpers import get_system_prompt
from chat.models import Bot, Conversation, CoreMemory, LLMRequest, Message, Participant, Trigger
from chat.prompt_templates import prompts


class BotModelTest(TestCase):
    def setUp(self):
        self.bot = Bot.objects.create(name="TestBot", model="gpt-4", prompt="You are a test bot.")
        CoreMemory.objects.create(bot=self.bot, memory="First memory")
        CoreMemory.objects.create(bot=self.bot, memory="Second memory")

    def test_str(self):
        self.assertEqual(str(self.bot), f"Bot {self.bot.id} TestBot (gpt-4)")

    def test_get_core_memories_for_prompt(self):
        memories = self.bot.get_core_memories_for_prompt()
        self.assertIn("- First memory", memories)
        self.assertIn("- Second memory", memories)

        # Checking order (recent first)
        memories_list = memories.split("\n")
        self.assertEqual(memories_list[0], "- Second memory")
        self.assertEqual(memories_list[1], "- First memory")


class TriggerModelTest(TestCase):
    def setUp(self):
        self.trigger = Trigger.objects.create(name="TestTrigger")

    def test_str(self):
        self.assertEqual(str(self.trigger), f"Trigger {self.trigger.id}: TestTrigger")


class ConversationModelTest(TestCase):
    def setUp(self):
        self.conversation = Conversation.objects.create(title="Test Conversation")
        self.user = User.objects.create(username="testuser")
        self.bot = Bot.objects.create(name="TestBot", model="gpt-4", prompt="Test")
        self.participant_user = Participant.objects.create(participant_type="user", user=self.user)
        self.participant_bot = Participant.objects.create(participant_type="bot", bot=self.bot)

        self.conversation.participants.add(self.participant_user)
        self.conversation.participants.add(self.participant_bot)

    def test_str(self):
        self.assertEqual(str(self.conversation), f"Conversation {self.conversation.uuid} created on {self.conversation.creation_date}")

    def test_list_of_bots(self):
        self.assertEqual(self.conversation.list_of_bots(), "TestBot")

    def test_list_of_humans(self):
        self.assertEqual(self.conversation.list_of_humans(), "testuser")


class ParticipantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.bot = Bot.objects.create(name="TestBot", model="gpt-4", prompt="Test")
        self.participant_user = Participant.objects.create(participant_type="user", user=self.user)
        self.participant_bot = Participant.objects.create(participant_type="bot", bot=self.bot)

    def test_str(self):
        self.assertEqual(str(self.participant_user), "Participant (user) - User: testuser")
        self.assertEqual(str(self.participant_bot), "Participant (bot) - Bot: TestBot")

    def test_name(self):
        self.assertEqual(self.participant_user.name(), "testuser")
        self.assertEqual(self.participant_bot.name(), "TestBot")


class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.bot = Bot.objects.create(name="TestBot", model="gpt-4", prompt="Test")
        self.conversation = Conversation.objects.create(title="Test Conversation")
        self.participant_user = Participant.objects.create(participant_type="user", user=self.user)
        self.participant_bot = Participant.objects.create(participant_type="bot", bot=self.bot)

        self.message_user = Message.objects.create(conversation=self.conversation, participant=self.participant_user, message="Hello from user")
        self.message_bot = Message.objects.create(conversation=self.conversation, participant=self.participant_bot, message="Hello from bot")

    def test_str(self):
        self.assertEqual(str(self.message_user), f"Message from {self.participant_user} at {self.message_user.timestamp} in conversation {self.conversation.uuid}")
        self.assertEqual(str(self.message_bot), f"Message from {self.participant_bot} at {self.message_bot.timestamp} in conversation {self.conversation.uuid}")

    def test_participant_name(self):
        self.assertEqual(self.message_user.participant_name(), "testuser")
        self.assertEqual(self.message_bot.participant_name(), "TestBot")


class LLMRequestModelTest(TestCase):
    def setUp(self):
        self.llm_request = LLMRequest.objects.create(request_type="test", model="gpt-4", temperature=0.8, prompt="Test prompt", response="Test response", total_tokens=10, completion_tokens=5)

    def test_str(self):
        self.assertEqual(str(self.llm_request), f"LLMRequest {self.llm_request.id} at {self.llm_request.timestamp}")


class CoreMemoryModelTest(TestCase):
    def setUp(self):
        self.bot = Bot.objects.create(name="TestBot", model="gpt-4", prompt="Test")
        self.core_memory = CoreMemory.objects.create(memory="This is a memory", bot=self.bot)

    def test_str(self):
        self.assertEqual(str(self.core_memory), f"CoreMemory {self.core_memory.id} for Bot TestBot at {self.core_memory.timestamp}")


class HelpersTest(TestCase):
    def test_get_system_prompt(self):
        # Create mock conversation
        mock_conversation = Mock()
        mock_conversation.list_of_bots.return_value = "BotA, BotB"
        mock_conversation.list_of_humans.return_value = "User1, User2"

        # Create mock bot
        mock_bot = Mock()
        mock_bot.name = "TestBot"
        mock_bot.prompt = "You are a friendly test bot."
        mock_bot.get_core_memories_for_prompt.return_value = "- Memory 1\n- Memory 2"

        # Expected prompt string
        expected_prompt = prompts["bots_in_conversation"].format(
            bot_name="TestBot", list_of_bots="BotA, BotB", list_of_humans="User1, User2", bot_prompt="You are a friendly test bot.", core_memories="- Memory 1\n- Memory 2"
        )

        # Test get_system_prompt
        with patch("chat.helpers.settings") as mock_settings:
            mock_settings.MAX_CORE_MEMORIES_PER_PROMPT = 3
            result = get_system_prompt(mock_conversation, mock_bot)

        # Verify method calls
        mock_conversation.list_of_bots.assert_called_once()
        mock_conversation.list_of_humans.assert_called_once()
        mock_bot.get_core_memories_for_prompt.assert_called_once_with(n_last_memories=3)

        # Verify result
        self.assertEqual(result, expected_prompt)
