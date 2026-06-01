"""
GauntletFuse - Phase 0 (Lite)

A simple, hackable multi-bot conversation framework.
Extracted and adapted from PolyBotConversation.

This is "Slack for bots" - simple, reliable, readable.
Intelligence comes later.
"""

__version__ = "0.1.0"

from gauntlet_lite.models import Message, ConversationContext
from gauntlet_lite.agents import BotAgent
from gauntlet_lite.controller import ConversationController

__all__ = [
    "Message",
    "ConversationContext",
    "BotAgent",
    "ConversationController",
]
