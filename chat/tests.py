from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from chat.models import Conversation, Participant


class ChatClearTest(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Create clients
        self.client1 = Client()
        self.client1.login(username="user1", password="password123")
        self.client2 = Client()
        self.client2.login(username="user2", password="password123")

        # Create conversations
        self.conv1 = Conversation.objects.create()
        self.part1 = Participant.objects.create(participant_type="user", user=self.user1)
        self.conv1.participants.add(self.part1)

        self.conv2 = Conversation.objects.create()
        self.part2 = Participant.objects.create(participant_type="user", user=self.user2)
        self.conv2.participants.add(self.part2)

        self.conv3 = Conversation.objects.create()
        self.part3_1 = Participant.objects.create(participant_type="user", user=self.user1)
        self.part3_2 = Participant.objects.create(participant_type="user", user=self.user2)
        self.conv3.participants.add(self.part3_1)
        self.conv3.participants.add(self.part3_2)

    def test_chat_clear_only_deletes_user_conversations(self):
        # Ensure we start with 3 conversations
        self.assertEqual(Conversation.objects.count(), 3)

        # User 1 clears their chats
        response = self.client1.post(reverse("chat:chat_clear"))

        # Assert redirect
        self.assertEqual(response.status_code, 302)

        # Ensure User 1's conversations (conv1, conv3) are deleted, but User 2's exclusive one (conv2) remains
        self.assertEqual(Conversation.objects.count(), 1)

        remaining_conv = Conversation.objects.first()
        self.assertEqual(remaining_conv.uuid, self.conv2.uuid)
