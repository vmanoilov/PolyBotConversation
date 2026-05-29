from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from chat.models import Conversation, Participant


class ChatDeleteTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.conversation = Conversation.objects.create()

        # user1 is a participant
        self.participant1 = Participant.objects.create(participant_type="user", user=self.user1)
        self.conversation.participants.add(self.participant1)

    def test_delete_conversation_as_participant(self):
        self.client.login(username='user1', password='password123')
        url = reverse('chat:chat_delete', kwargs={'conversation_uuid': self.conversation.uuid})
        response = self.client.get(url) # Assuming get based on views, usually should be post

        self.assertEqual(response.status_code, 302) # Redirects to index
        self.assertFalse(Conversation.objects.filter(uuid=self.conversation.uuid).exists())

    def test_delete_conversation_as_non_participant(self):
        self.client.login(username='user2', password='password123')
        url = reverse('chat:chat_delete', kwargs={'conversation_uuid': self.conversation.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Conversation.objects.filter(uuid=self.conversation.uuid).exists())

    def test_delete_conversation_unauthenticated(self):
        url = reverse('chat:chat_delete', kwargs={'conversation_uuid': self.conversation.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302) # Redirect to login
        self.assertTrue(Conversation.objects.filter(uuid=self.conversation.uuid).exists())
