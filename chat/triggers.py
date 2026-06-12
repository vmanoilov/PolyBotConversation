import logging
from datetime import timedelta

from chat.bot import generate_message_general, generate_message_mention
from chat.helpers import detect_mention
from django.utils import timezone
from django_q.models import Schedule
from django_q.tasks import schedule

logger = logging.getLogger(__name__)


def mention(conversation):
    bots = [participant.bot for participant in conversation.participants.filter(participant_type="bot")]

    for bot in bots:
        messages = conversation.messages.exclude(triggered_bots__id=bot.id).exclude(participant__bot__id=bot.id)

        for message in messages:
            if detect_mention(bot.name, message.message):
                logger.info(f'Mention detected: {bot.name} in "{message.message}"')
                message.triggered_bots.add(bot)
                generate_message_mention(conversation, message, bot)


def general(conversation):
    bots = [participant.bot for participant in conversation.participants.filter(participant_type="bot")]

    for i, bot in enumerate(bots):
        schedule("chat.bot.generate_message_general", conversation, bot, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(seconds=i * 5))
