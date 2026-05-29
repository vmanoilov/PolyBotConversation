"""
BotAgent abstraction for bot-to-bot conversations.
Each bot has a personality, memory, and can respond to messages.
"""

import os
import logging
from typing import List
from gauntlet_lite.models.message import Message
from gauntlet_lite.models.conversation_state import ConversationContext

logger = logging.getLogger(__name__)


class BotAgent:
    """
    Represents a bot agent in the conversation system.
    
    Each bot has:
    - Unique ID and name
    - Personality prompt
    - LLM model and temperature settings
    - Memory of previous interactions
    - Ability to respond to messages
    
    Attributes:
        id: Unique identifier for this bot
        name: Display name
        prompt: Personality/system prompt that defines bot behavior
        model: LLM model to use (e.g., "gpt-3.5-turbo")
        temperature: LLM temperature setting (0.0-2.0)
        memory: List of messages this bot has seen
        use_llm: Whether to use real LLM or mock responses
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        use_llm: bool = False
    ):
        self.id = id
        self.name = name
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.memory: List[Message] = []
        self.use_llm = use_llm
        
        # Only import OpenAI if we're actually using it
        if self.use_llm:
            try:
                import openai
                self.openai = openai
                self.api_key = os.environ.get("OPENAI_API_KEY")
                if not self.api_key:
                    logger.warning(f"Bot {self.name}: OPENAI_API_KEY not set, falling back to mock responses")
                    self.use_llm = False
            except ImportError:
                logger.warning(f"Bot {self.name}: openai package not installed, using mock responses")
                self.use_llm = False
    
    def respond(self, input_message: Message, context: ConversationContext) -> Message:
        """
        Generate a response to a message given the conversation context.
        
        Args:
            input_message: The message to respond to
            context: Full conversation context
            
        Returns:
            Message object containing the bot's response
        """
        # Add the input message to memory
        self.memory.append(input_message)
        
        if self.use_llm and self.api_key:
            response_content = self._generate_llm_response(context)
        else:
            response_content = self._generate_mock_response(input_message, context)
        
        # Create and return response message
        response = Message(
            from_=self.name,
            content=response_content,
            meta={"bot_id": self.id}
        )
        
        self.memory.append(response)
        return response
    
    def _generate_llm_response(self, context: ConversationContext) -> str:
        """Generate response using actual LLM."""
        try:
            client = self.openai.OpenAI(api_key=self.api_key)
            
            # Build messages for LLM
            messages = [
                {
                    "role": "system",
                    "content": self._build_system_prompt(context)
                }
            ]
            
            # Add conversation history
            messages.extend(context.get_history_for_llm(bot_name=self.name))
            
            # Call LLM
            response = client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Bot {self.name}: LLM error: {e}, falling back to mock")
            return self._generate_mock_response(context.get_last_message(), context)
    
    def _generate_mock_response(self, input_message: Message, context: ConversationContext) -> str:
        """Generate a mock response without calling LLM."""
        # Simple mock responses based on conversation state
        message_count = len(context.messages)
        
        responses = [
            f"Interesting point about '{input_message.content[:30]}...'. I'd like to add my perspective.",
            f"I see what you mean, {input_message.from_}. From my viewpoint, that's quite insightful.",
            "Building on that thought - I think there's more to consider here.",
            "That's a valid observation. Let me contribute to this discussion.",
            f"I appreciate your input, {input_message.from_}. Here's my take on this.",
        ]
        
        # Use message count to deterministically select response
        return responses[message_count % len(responses)]
    
    def _build_system_prompt(self, context: ConversationContext) -> str:
        """Build the system prompt including bot personality and context."""
        participants = ", ".join(sorted(context.participants))
        
        system_prompt = f"""You are a bot called {self.name}. You are communicating with other participants.
The participants in this conversation are: {participants}.

Your personality and role:
{self.prompt}

Important guidelines:
- Keep responses short and natural (1-3 sentences)
- Stay in character based on your personality
- Reference previous messages when relevant
- Don't mention that you're an AI or bot
- Contribute meaningfully to the conversation
"""
        return system_prompt
    
    def should_respond(self, message: Message, context: ConversationContext) -> bool:
        """
        Determine if this bot should respond to a message.
        
        Simple logic for now:
        - Don't respond to own messages
        - Can respond to any other message
        
        Args:
            message: The message to consider
            context: Current conversation context
            
        Returns:
            True if bot should respond
        """
        # Don't respond to own messages (check both name and ID for consistency)
        if message.from_ == self.name or message.from_ == self.id:
            return False
        
        # Don't respond if we just responded
        if context.messages and (context.messages[-1].from_ == self.name or context.messages[-1].from_ == self.id):
            return False
        
        return True
    
    def __repr__(self):
        return f"BotAgent(id={self.id}, name={self.name}, model={self.model})"
    
    def __str__(self):
        return f"Bot: {self.name}"
