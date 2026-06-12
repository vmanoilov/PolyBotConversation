"""
Conversation state management.
Holds the shared conversation history and context.
"""

from typing import List, Optional

from gauntlet_lite.models.message import Message


class ConversationContext:
    """
    Maintains conversation state and history.

    Attributes:
        messages: List of all messages in the conversation
        participants: Set of participant IDs (bot IDs and users)
    """

    def __init__(self):
        self.messages: List[Message] = []
        self.participants: set = set()

    def add_message(self, message: Message):
        """Add a message to the conversation history."""
        self.messages.append(message)
        self.participants.add(message.from_)
        if message.to:
            self.participants.add(message.to)

    def get_messages(self, limit: Optional[int] = None) -> List[Message]:
        """Get messages, optionally limited to the most recent N messages."""
        if limit:
            return self.messages[-limit:]
        return self.messages

    def get_messages_from(self, participant_id: str) -> List[Message]:
        """Get all messages from a specific participant."""
        return [msg for msg in self.messages if msg.from_ == participant_id]

    def get_last_message(self) -> Optional[Message]:
        """Get the most recent message."""
        return self.messages[-1] if self.messages else None

    def get_history_for_llm(self, bot_name: str = None) -> List[dict]:
        """
        Convert message history to LLM-compatible format.

        Args:
            bot_name: Name of the bot requesting history (for role assignment)

        Returns:
            List of message dicts in OpenAI format
        """
        llm_messages = []
        for msg in self.messages:
            # Messages from this bot are "assistant", others are "user"
            role = "assistant" if msg.from_ == bot_name else "user"
            llm_messages.append({
                "role": role,
                "name": msg.from_,
                "content": msg.content
            })
        return llm_messages

    def clear(self):
        """Clear all messages and reset conversation."""
        self.messages = []
        self.participants = set()

    def __len__(self):
        return len(self.messages)

    def __repr__(self):
        return f"ConversationContext(messages={len(self.messages)}, participants={self.participants})"
