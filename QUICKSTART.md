# GauntletFuse - Phase 0 (Lite) Quick Start

This repository now contains **GauntletFuse Lite** - a simple, hackable multi-bot conversation framework extracted from PolyBotConversation.

## What's New?

The `gauntlet_lite/` directory contains a standalone framework for orchestrating conversations between multiple LLM-powered bots.

## Quick Start

### 1. Run the Demo

```bash
cd gauntlet_lite
python main.py
```

This shows 4 different demo conversations with multiple bots.

### 2. Run the Simple Example

```bash
cd gauntlet_lite
python example.py
```

This is a minimal example showing how to create a 2-bot conversation.

### 3. Create Your Own Bot

```python
from gauntlet_lite import BotAgent, ConversationController

# Create a bot
my_bot = BotAgent(
    id="my-bot-1",
    name="MyBot",
    prompt="You are a helpful assistant who loves explaining things clearly.",
    use_llm=False  # Set to True to use real OpenAI API
)

# Create controller and register bot
controller = ConversationController()
controller.register_bot(my_bot)

# Add more bots...
# controller.register_bot(another_bot)

# Start conversation
controller.run_conversation(
    initial_message="Tell me about your expertise.",
    max_turns=5,
    verbose=True
)
```

## Features

✅ **Multiple bot agents** with unique personalities  
✅ **Bot-to-bot communication** with maintained context  
✅ **Simple orchestration** via ConversationController  
✅ **Mock mode** (no API costs) and **LLM mode** (real AI)  
✅ **Extensible design** - easy to customize and extend  

## Documentation

See the full documentation in [`gauntlet_lite/README.md`](gauntlet_lite/README.md)

## Original Project

This framework is extracted from the original Django-based web application in this repository. To use the original PolyBotConversation web app, see the main [README.md](README.md).

## Architecture

```
gauntlet_lite/
├── agents/           # Bot agent implementations
├── controller/       # Conversation orchestration
├── models/          # Message and context models
├── main.py          # Full demo with multiple scenarios
├── example.py       # Minimal quick-start example
└── README.md        # Comprehensive documentation
```

## Requirements

- Python 3.8+
- (Optional) OpenAI API key for real LLM responses
- (Optional) `openai` package for LLM mode

No requirements for mock mode - works out of the box!

## Design Philosophy

> **"Slack for bots"** - Simple, reliable, readable.

This is **Phase 0** - deliberately minimal to make it easy to understand and extend. Future phases will add more advanced features.

---

**For detailed usage, API reference, and examples, see [`gauntlet_lite/README.md`](gauntlet_lite/README.md)**
