"""
Message model for bot-to-bot communication.
Defines a canonical message format for all conversations.
"""

import time
import uuid
from typing import Optional


class Message:
    """
    Canonical message format for all communication in the system.

    Attributes:
        id: Unique identifier for the message
        from_: ID of the sender (bot id or "user")
        to: Optional target recipient (bot id or None for broadcast)
        content: The actual message content
        timestamp: Unix timestamp when message was created
        meta: Optional metadata dictionary
    """

    def __init__(self, from_: str, content: str, to: Optional[str] = None, id: Optional[str] = None, timestamp: Optional[float] = None, meta: Optional[dict] = None):
        self.id = id or str(uuid.uuid4())
        self.from_ = from_
        self.to = to
        self.content = content
        self.timestamp = timestamp or time.time()
        self.meta = meta or {}

    def __repr__(self):
        target = f" -> {self.to}" if self.to else ""
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Message(from={self.from_}{target}, content='{content_preview}')"

    def __str__(self):
        return f"[{self.from_}]: {self.content}"

    def to_dict(self):
        """Convert message to dictionary format."""
        return {"id": self.id, "from": self.from_, "to": self.to, "content": self.content, "timestamp": self.timestamp, "meta": self.meta}
