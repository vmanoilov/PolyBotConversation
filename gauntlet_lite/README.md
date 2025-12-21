# GauntletFuse - Phase 0 (Lite)

A simple, hackable multi-bot conversation framework. Think of it as **"Slack for bots"** - dumb, reliable, and readable. Intelligence comes later.

Extracted and adapted from [PolyBotConversation](https://github.com/IngoKl/PolyBotConversation/).

## What Is This?

GauntletFuse Lite is a minimal framework for orchestrating conversations between multiple LLM-powered bots (or mock bots). It provides:

- ✅ **Multiple bot agents** - Each with unique personality, memory, and response behavior
- ✅ **Bot-to-bot communication** - Bots can respond to each other's messages
- ✅ **Conversation context** - Full message history maintained and accessible
- ✅ **Identity management** - Clear tracking of who said what
- ✅ **Central orchestration** - ConversationController manages the conversation flow
- ✅ **Mock & LLM modes** - Run without API costs, or use real OpenAI models
- ✅ **Extensible design** - Easy to add new bots and features

## What This Is NOT

This is a **Phase 0** implementation. It deliberately excludes:

- ❌ Adversarial logic (Red/Blue/Purple teams)
- ❌ Scoring or evaluation systems
- ❌ Complex fusion or synthesis
- ❌ UI/frontend (this is a library)
- ❌ Authentication or security
- ❌ Persistent storage (memory-only for now)

These features are planned for future phases.

## Architecture

```
gauntlet_lite/
├── agents/
│   └── bot_agent.py          # BotAgent class - individual bot with personality
├── controller/
│   └── conversation_controller.py  # ConversationController - orchestrates conversations
├── models/
│   ├── message.py            # Message - canonical message format
│   └── conversation_state.py # ConversationContext - conversation history
└── main.py                   # Demo script showing usage
```

### Core Components

#### 1. Message (`models/message.py`)

Canonical message format for all communication:

```python
Message(
    from_="bot-alpha",      # Who sent it
    content="Hello!",        # Message content
    to="bot-beta",          # Optional: specific recipient
    timestamp=1234567890.0, # When it was sent
    meta={}                 # Optional metadata
)
```

#### 2. BotAgent (`agents/bot_agent.py`)

Represents a single bot with personality:

```python
bot = BotAgent(
    id="unique-bot-id",
    name="AlphaBot",
    prompt="You are a practical, analytical bot...",
    model="gpt-3.5-turbo",
    temperature=0.7,
    use_llm=True  # False for mock responses
)
```

Each bot:
- Has a unique identity and personality
- Maintains its own message memory
- Can respond to messages with context awareness
- Works with or without real LLM calls

#### 3. ConversationContext (`models/conversation_state.py`)

Holds shared conversation state:

```python
context = ConversationContext()
context.add_message(message)
context.get_messages(limit=10)  # Last 10 messages
context.get_history_for_llm()   # Format for LLM APIs
```

#### 4. ConversationController (`controller/conversation_controller.py`)

Central orchestrator:

```python
controller = ConversationController()
controller.register_bot(bot_alpha)
controller.register_bot(bot_beta)
controller.run_conversation(
    initial_message="Let's discuss AI ethics",
    max_turns=10
)
```

The controller:
- Manages multiple bots
- Routes messages between bots
- Coordinates turn-taking (round-robin by default)
- Provides conversation flow control

## Installation

### Prerequisites

- Python 3.8 or higher
- (Optional) OpenAI API key for real LLM responses

### Setup

1. **Clone the repository:**

```bash
git clone <repository-url>
cd PolyBotConversation
```

2. **Install dependencies:**

```bash
pip install openai  # Only if you want to use real LLM
```

3. **(Optional) Set OpenAI API key:**

```bash
# Linux/Mac
export OPENAI_API_KEY=sk-...

# Windows
set OPENAI_API_KEY=sk-...
```

## Usage

### Running the Demo

The easiest way to see it in action:

```bash
cd gauntlet_lite
python main.py
```

This runs several demos showing:
1. Simple round-robin conversation
2. Multi-turn interactions
3. Conversation summaries
4. (Optional) Real LLM usage

### Basic Usage Example

```python
from gauntlet_lite import BotAgent, ConversationController

# Create bots
bot1 = BotAgent(
    id="bot1",
    name="Alice",
    prompt="You are Alice, a pragmatic engineer.",
    use_llm=False  # Mock responses
)

bot2 = BotAgent(
    id="bot2", 
    name="Bob",
    prompt="You are Bob, a creative designer.",
    use_llm=False
)

# Create controller and register bots
controller = ConversationController()
controller.register_bot(bot1)
controller.register_bot(bot2)

# Start conversation
controller.run_conversation(
    initial_message="What makes good software?",
    max_turns=6,
    verbose=True
)

# Get summary
print(controller.get_conversation_summary())
```

### Adding a New Bot

To add a new bot to an existing conversation:

```python
# 1. Create the bot with a unique personality
new_bot = BotAgent(
    id="bot-gamma",
    name="Gamma",
    prompt="You are Gamma, a balanced mediator who seeks consensus.",
    temperature=0.8,
    use_llm=False
)

# 2. Register with controller
controller.register_bot(new_bot)

# 3. Bot automatically participates in subsequent turns
controller.run_conversation(
    initial_message="What's your perspective?",
    max_turns=3
)
```

### Using Real LLM

To use OpenAI API instead of mock responses:

```python
bot = BotAgent(
    id="smart-bot",
    name="SmartBot",
    prompt="Your personality here...",
    model="gpt-3.5-turbo",  # or gpt-4, etc.
    temperature=0.7,
    use_llm=True  # Enable LLM calls
)
```

Make sure `OPENAI_API_KEY` is set in your environment.

### Advanced Usage

#### Manual Turn Control

```python
# Process specific bot's turn
controller.process_turn(bot_id="bot-alpha")

# Process next bot in round-robin order
controller.process_turn()
```

#### Adding Messages Manually

```python
from gauntlet_lite.models import Message

# Add a user message
user_msg = Message(from_="user", content="What do you think?")
controller.add_message(user_msg)

# Let bots respond
for _ in range(3):
    controller.process_turn()
```

#### Broadcasting to All Bots

```python
# Get responses from all bots
responses = controller.broadcast_message(
    content="Everyone share your opinion!",
    from_="moderator"
)

for response in responses:
    print(f"{response.from_}: {response.content}")
```

## How It Works

### Conversation Flow

1. **Initialization**: Create bots and controller
2. **Registration**: Register bots with controller
3. **Message Input**: Add initial message (from user or system)
4. **Turn Processing**: Controller determines which bot's turn
5. **Bot Response**: Bot generates response based on:
   - Its personality prompt
   - Conversation history
   - Previous messages
6. **Context Update**: Response added to shared context
7. **Repeat**: Continue until max turns or natural end

### Turn-Taking Logic

By default, bots take turns in round-robin order:

```
User → Bot-Alpha → Bot-Beta → Bot-Gamma → Bot-Alpha → ...
```

Bots can choose not to respond if:
- The last message was from themselves
- They have nothing to add (in LLM mode)

### Message Flow

```
┌─────────────────────────────────────┐
│   ConversationController            │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   ConversationContext       │   │
│  │   (Shared Message History)  │   │
│  └─────────────────────────────┘   │
│              │                      │
│              │ Read/Write           │
│       ┌──────┴──────┐              │
│       ▼              ▼              │
│   BotAgent-A    BotAgent-B         │
│   (Memory)      (Memory)           │
└─────────────────────────────────────┘
```

## Configuration

### Bot Configuration

Key parameters when creating a bot:

- **`id`**: Unique identifier (string)
- **`name`**: Display name (used in messages)
- **`prompt`**: Personality/system prompt defining bot behavior
- **`model`**: LLM model name (e.g., "gpt-3.5-turbo")
- **`temperature`**: LLM creativity (0.0-2.0)
- **`use_llm`**: True for real LLM, False for mock responses

### Controller Configuration

The controller uses sensible defaults:
- Round-robin turn order
- All registered bots participate
- Bots can opt out of responding

## Extending the Framework

### Custom Bot Behaviors

Subclass `BotAgent` to add custom behavior:

```python
class SpecializedBot(BotAgent):
    def should_respond(self, message, context):
        # Custom logic for when to respond
        if "urgent" in message.content.lower():
            return True
        return super().should_respond(message, context)
    
    def _generate_mock_response(self, input_message, context):
        # Custom mock responses
        return "I specialize in urgent matters!"
```

### Custom Turn Logic

Subclass `ConversationController` for custom orchestration:

```python
class CustomController(ConversationController):
    def process_turn(self, bot_id=None):
        # Custom turn selection logic
        # e.g., priority-based, mention-based, etc.
        return super().process_turn(bot_id)
```

### Adding Metadata

Use the `meta` field in messages for custom data:

```python
message = Message(
    from_="bot",
    content="Hello",
    meta={
        "sentiment": "positive",
        "confidence": 0.95,
        "intent": "greeting"
    }
)
```

## Testing

Run the demo script to verify everything works:

```bash
python gauntlet_lite/main.py
```

You should see multiple demo conversations with clear bot interactions.

## Troubleshooting

### "OPENAI_API_KEY not set"

This is just a warning. The system falls back to mock responses automatically. Set the environment variable if you want real LLM:

```bash
export OPENAI_API_KEY=sk-your-key-here
```

### "openai package not installed"

If you want to use real LLM, install it:

```bash
pip install openai
```

For mock mode, no additional packages are needed.

### Import Errors

Make sure you're in the correct directory:

```bash
cd /path/to/PolyBotConversation
python gauntlet_lite/main.py
```

Or add to Python path:

```python
import sys
sys.path.append('/path/to/PolyBotConversation')
```

## Design Decisions

### Why Mock by Default?

- **No API costs** during development
- **Faster iteration** without network calls
- **Predictable behavior** for testing
- **Easy to switch** to real LLM when ready

### Why Round-Robin?

- **Simple and predictable** - easy to understand and debug
- **Fair participation** - all bots get equal turns
- **Deterministic** - same input → same flow
- **Easy to extend** - can add smarter logic later

### Why Memory-Only?

- **Simplicity** - no database setup required
- **Fast prototyping** - instant startup
- **Minimal dependencies** - just Python
- **Clear upgrade path** - easy to add persistence later

## Future Roadmap

This is Phase 0. Future phases may include:

- **Phase 1**: Persistence (save/load conversations)
- **Phase 2**: Advanced orchestration (mentions, priorities, interrupts)
- **Phase 3**: Adversarial modes (Red/Blue team dynamics)
- **Phase 4**: Fusion and synthesis
- **Phase 5**: Evaluation and scoring
- **Phase 6**: Web UI and API

## Contributing

Contributions welcome! This is designed to be hackable. Fork it, modify it, extend it.

Keep changes:
- **Simple** - Prefer clarity over cleverness
- **Readable** - Code should be self-documenting
- **Minimal** - Don't add what you don't need

## License

Same as the parent PolyBotConversation project.

## Credits

Extracted and adapted from [PolyBotConversation](https://github.com/IngoKl/PolyBotConversation/) by IngoKl.

## Contact

For questions or issues, see the main repository.

---

**Remember**: This is "Slack for bots" - simple, reliable, readable. Intelligence comes later.
