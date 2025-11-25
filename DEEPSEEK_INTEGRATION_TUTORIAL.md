# DeepSeek Integration with Memori - Complete Tutorial

This tutorial demonstrates how to integrate DeepSeek's AI models with Memori for persistent memory capabilities.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Configuration Overview](#configuration-overview)
4. [Code Walkthrough](#code-walkthrough)
5. [Running the Example](#running-the-example)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher
- `memorisdk` package installed
- A DeepSeek API key (obtain from [DeepSeek Platform](https://platform.deepseek.com/api_keys))

### Installation

```bash
# Install Memori SDK
pip install memorisdk

# Install additional dependencies if needed
pip install python-dotenv  # Optional: for managing environment variables
```

---

## Setup Instructions

### Step 1: Get Your DeepSeek API Key

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy and save your API key securely

### Step 2: Set Up Environment Variables

Create a `.env` file in your project directory:

```bash
# .env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat  # Optional: defaults to deepseek-chat
```

Or export the environment variable directly:

```bash
# On Linux/Mac
export DEEPSEEK_API_KEY="your_deepseek_api_key_here"

# On Windows (Command Prompt)
set DEEPSEEK_API_KEY=your_deepseek_api_key_here

# On Windows (PowerShell)
$env:DEEPSEEK_API_KEY="your_deepseek_api_key_here"
```

### Step 3: Create the Integration Script

Save the following code as `deepseek_example.py`:

```python
import os

from memori import Memori
from memori.core.providers import ProviderConfig

# Create DeepSeek provider configuration
# DeepSeek API is compatible with OpenAI's API format
deepseek_provider = ProviderConfig.from_custom(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # Get API key from environment variable
    model=os.getenv(
        "DEEPSEEK_MODEL", "deepseek-chat"
    ),  # Default to deepseek-chat, can be overridden
)

print("Initializing Memori with DeepSeek...")
deepseek_memory = Memori(
    database_connect="sqlite:///deepseek_demo.db",
    conscious_ingest=True,
    auto_ingest=True,
    verbose=True,
    provider_config=deepseek_provider,
)

# Create client using the provider config
client = deepseek_provider.create_client()

print("Enabling memory tracking...")
deepseek_memory.enable()

print(
    f"Memori DeepSeek Example - Chat with {deepseek_provider.model} while memory is being tracked"
)
print("Make sure you have set DEEPSEEK_API_KEY environment variable")
print("Type 'exit' or press Ctrl+C to quit")
print("-" * 50)

while 1:
    try:
        user_input = input("User: ")
        if not user_input.strip():
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("Processing your message with memory tracking...")
        response = client.chat.completions.create(
            model=deepseek_provider.model,
            messages=[{"role": "user", "content": user_input}],
        )
        print(f"AI: {response.choices[0].message.content}")
        print()  # Add blank line for readability
    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        break
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set DEEPSEEK_API_KEY environment variable")
        print("Get your API key from: https://platform.deepseek.com/api_keys")
        continue
```

---

## Configuration Overview

### Provider Configuration

The `ProviderConfig.from_custom()` method is used to configure DeepSeek:

```python
deepseek_provider = ProviderConfig.from_custom(
    base_url="https://api.deepseek.com/v1",  # DeepSeek API endpoint
    api_key=os.getenv("DEEPSEEK_API_KEY"),   # Your API key
    model="deepseek-chat"                     # Model name
)
```

**Key Parameters:**
- `base_url`: DeepSeek's API endpoint (OpenAI-compatible)
- `api_key`: Your DeepSeek API key from environment variable
- `model`: The DeepSeek model to use (default: `deepseek-chat`)

### Available DeepSeek Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `deepseek-chat` | General-purpose chat model | Conversational AI, Q&A |
| `deepseek-coder` | Specialized for code generation | Programming assistance |

### Memori Configuration

```python
deepseek_memory = Memori(
    database_connect="sqlite:///deepseek_demo.db",  # SQLite database for memory
    conscious_ingest=True,   # Enable background memory analysis
    auto_ingest=True,        # Enable real-time memory retrieval
    verbose=True,            # Show detailed logs
    provider_config=deepseek_provider  # Use DeepSeek provider
)
```

**Memory Modes:**
- `conscious_ingest=True`: Background AI agent analyzes and promotes important memories
- `auto_ingest=True`: Dynamically searches and injects relevant memories per query
- Both enabled: **Recommended** for best performance

---

## Code Walkthrough

### 1. Import Dependencies

```python
import os
from memori import Memori
from memori.core.providers import ProviderConfig
```

### 2. Configure DeepSeek Provider

```python
deepseek_provider = ProviderConfig.from_custom(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
)
```

This creates a custom provider configuration that tells Memori how to connect to DeepSeek's API.

### 3. Initialize Memori

```python
deepseek_memory = Memori(
    database_connect="sqlite:///deepseek_demo.db",
    conscious_ingest=True,
    auto_ingest=True,
    verbose=True,
    provider_config=deepseek_provider,
)
```

This initializes the Memori memory engine with:
- SQLite database for storing conversations
- Both memory modes enabled
- Verbose logging for debugging
- DeepSeek as the LLM provider

### 4. Create Client and Enable Memory

```python
client = deepseek_provider.create_client()
deepseek_memory.enable()
```

- `create_client()`: Creates an OpenAI-compatible client for DeepSeek
- `enable()`: Activates memory tracking for all subsequent API calls

### 5. Interactive Chat Loop

```python
while 1:
    user_input = input("User: ")
    
    response = client.chat.completions.create(
        model=deepseek_provider.model,
        messages=[{"role": "user", "content": user_input}],
    )
    
    print(f"AI: {response.choices[0].message.content}")
```

The chat loop:
- Accepts user input
- Sends to DeepSeek via the client
- **Automatically records and retrieves memories** (handled by Memori)
- Displays the response

---

## Running the Example

### Basic Usage

```bash
# Set your API key
export DEEPSEEK_API_KEY="your_api_key_here"

# Run the script
python deepseek_example.py
```

### Example Conversation

```
Initializing Memori with DeepSeek...
Enabling memory tracking...
Memori DeepSeek Example - Chat with deepseek-chat while memory is being tracked
Make sure you have set DEEPSEEK_API_KEY environment variable
Type 'exit' or press Ctrl+C to quit
--------------------------------------------------
User: My name is Alice and I love Python programming
Processing your message with memory tracking...
AI: Nice to meet you, Alice! Python is a wonderful language...

User: What's my name?
Processing your message with memory tracking...
AI: Your name is Alice! You mentioned that earlier.

User: exit
Goodbye!
```

**Notice:** The AI remembers your name from the previous conversation thanks to Memori!

---

## Advanced Usage

### Using DeepSeek Coder Model

For code-related tasks, use the `deepseek-coder` model:

```python
# Set environment variable
export DEEPSEEK_MODEL="deepseek-coder"

# Or modify the code directly
deepseek_provider = ProviderConfig.from_custom(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model="deepseek-coder"  # Use coder model
)
```

### Using PostgreSQL Instead of SQLite

For production use, switch to PostgreSQL:

```python
deepseek_memory = Memori(
    database_connect="postgresql://user:password@localhost:5432/memori_db",
    conscious_ingest=True,
    auto_ingest=True,
    provider_config=deepseek_provider,
)
```

### Multi-User Support with Namespaces

Isolate memories for different users:

```python
def create_user_memory(user_id: str):
    return Memori(
        database_connect="sqlite:///deepseek_demo.db",
        namespace=f"user_{user_id}",  # Separate namespace per user
        conscious_ingest=True,
        auto_ingest=True,
        provider_config=deepseek_provider,
    )

# Usage
alice_memory = create_user_memory("alice")
alice_memory.enable()

bob_memory = create_user_memory("bob")
bob_memory.enable()
```

### Custom System Prompts

Add system prompts to guide the AI's behavior:

```python
response = client.chat.completions.create(
    model=deepseek_provider.model,
    messages=[
        {"role": "system", "content": "You are a helpful Python programming assistant."},
        {"role": "user", "content": user_input}
    ],
)
```

### Using with dotenv

For better environment variable management:

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

deepseek_provider = ProviderConfig.from_custom(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
)
```

---

## Troubleshooting

### Common Issues

#### 1. Missing API Key Error

**Error:**
```
Error: API key not found
```

**Solution:**
```bash
# Make sure DEEPSEEK_API_KEY is set
echo $DEEPSEEK_API_KEY

# If empty, set it
export DEEPSEEK_API_KEY="your_api_key_here"
```

#### 2. Connection Error

**Error:**
```
Error: Connection refused or timeout
```

**Solution:**
- Check your internet connection
- Verify the API endpoint: `https://api.deepseek.com/v1`
- Ensure your API key is valid

#### 3. Authentication Error

**Error:**
```
Error: 401 Unauthorized
```

**Solution:**
- Verify your API key is correct
- Check if your API key has expired
- Generate a new API key from [DeepSeek Platform](https://platform.deepseek.com/api_keys)

#### 4. Model Not Found

**Error:**
```
Error: Model 'xxx' not found
```

**Solution:**
```python
# Use correct model names
model="deepseek-chat"  # For general chat
model="deepseek-coder"  # For code generation
```

#### 5. Database Lock Error (SQLite)

**Error:**
```
Error: database is locked
```

**Solution:**
- Close any other processes using the database
- Or switch to PostgreSQL for production use

### Enable Debugging

For more detailed error information:

```python
deepseek_memory = Memori(
    database_connect="sqlite:///deepseek_demo.db",
    conscious_ingest=True,
    auto_ingest=True,
    verbose=True,  # Enable verbose logging
    provider_config=deepseek_provider,
)
```

---

## Comparison: DeepSeek vs Ollama Integration

| Aspect | DeepSeek | Ollama |
|--------|----------|--------|
| **Hosting** | Cloud-based API | Local installation |
| **API Key** | Required | Not required |
| **Base URL** | `https://api.deepseek.com/v1` | `http://localhost:11434/v1` |
| **Setup** | Environment variable | Run `ollama serve` |
| **Internet** | Required | Not required |
| **Cost** | Pay per use | Free (local) |
| **Performance** | Depends on API | Depends on hardware |

**Key Difference:**
- **DeepSeek**: Cloud-based, requires API key, needs internet
- **Ollama**: Local, no API key needed, runs offline

Both use the same Memori integration pattern via `ProviderConfig.from_custom()`!

---

## Next Steps

1. **Explore Memory Features**: Check stored memories in `deepseek_demo.db`
2. **Build Applications**: Integrate into web apps, chatbots, or automation tools
3. **Customize Behavior**: Adjust memory modes and retention policies
4. **Scale Up**: Switch to PostgreSQL and add user namespaces
5. **Monitor Performance**: Use verbose mode to understand memory injection

## Resources

- **DeepSeek Documentation**: https://platform.deepseek.com/docs
- **Memori Documentation**: https://memorilabs.ai/docs
- **Memori GitHub**: https://github.com/GibsonAI/Memori
- **Get DeepSeek API Key**: https://platform.deepseek.com/api_keys

---

## Summary

You've learned how to:
- ✅ Configure DeepSeek with Memori using `ProviderConfig.from_custom()`
- ✅ Set up environment variables for API keys
- ✅ Enable dual memory modes (conscious + auto)
- ✅ Create an interactive chat application with persistent memory
- ✅ Troubleshoot common integration issues

The integration is simple: just 3 steps!
1. Configure provider
2. Initialize Memori
3. Enable memory tracking

Now your DeepSeek-powered AI has human-like memory! 🧠
