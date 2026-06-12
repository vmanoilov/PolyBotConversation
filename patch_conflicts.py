import re

with open('chat/bot.py', 'r') as f:
    content = f.read()

# Replace check_turn conflict
content = re.sub(
    r'<<<<<<< HEAD\n    for msg in conversation\.messages\.select_related\("participant__user", "participant__bot"\)\.all\(\):\n=======\n    for msg in conversation\.messages\.all\(\):\n>>>>>>> origin/main',
    '    for msg in conversation.messages.select_related("participant__user", "participant__bot").all():',
    content
)

# Replace generate_message_mention conflict
content = re.sub(
    r'<<<<<<< HEAD\n    conversation_messages = Message\.objects\.filter\(conversation=conversation\)\.select_related\("participant__user", "participant__bot"\)\.order_by\("timestamp"\)\n=======\n    conversation_messages = Message\.objects\.filter\(conversation=conversation\)\.order_by\("timestamp"\)\n>>>>>>> origin/main',
    '    conversation_messages = Message.objects.filter(conversation=conversation).select_related("participant__user", "participant__bot").order_by("timestamp")',
    content
)

with open('chat/bot.py', 'w') as f:
    f.write(content)
