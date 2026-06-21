import logging

from django.core.management.base import BaseCommand

from chat.models import Conversation
from chat.triggers import general

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Test command"

    def add_arguments(self, parser):
        parser.add_argument("conversation_id", type=int)

    def handle(self, *args, **options):
        conversation_id = options["conversation_id"]
        conversation = Conversation.objects.get(id=conversation_id)

        bot = conversation.participants.filter(participant_type="bot").first().bot
        general(conversation=conversation)
