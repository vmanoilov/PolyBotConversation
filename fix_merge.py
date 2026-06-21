import re

with open('chat/bot.py', 'r') as f:
    content = f.read()

content = content.replace('''<<<<<<< HEAD
    for msg in conversation.messages.all().select_related('participant__user', 'participant__bot'):
=======
    for msg in conversation.messages.all():
>>>>>>> origin/main''', "    for msg in conversation.messages.all().select_related('participant__user', 'participant__bot'):")

content = content.replace('''<<<<<<< HEAD
    conversation_messages = Message.objects.filter(conversation=conversation).order_by("timestamp").select_related('participant__user', 'participant__bot')
=======
    conversation_messages = Message.objects.filter(conversation=conversation).order_by("timestamp")
>>>>>>> origin/main''', "    conversation_messages = Message.objects.filter(conversation=conversation).order_by(\"timestamp\").select_related('participant__user', 'participant__bot')")

with open('chat/bot.py', 'w') as f:
    f.write(content)
