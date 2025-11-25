# Memori - AI Memory Engine

<p align="center">
  <strong>Open-Source SQL-Native Memory Engine for LLMs, AI Agents & Multi-Agent Systems</strong>
</p>

<p align="center">
  <em>Give your AI persistent, queryable memory with a single line of code</em>
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Memory Modes](#memory-modes)
- [AI Provider Integration](#ai-provider-integration)
- [Database Setup](#database-setup)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

---

## Overview

Memori enables any LLM to remember conversations, learn from interactions, and maintain context across sessions. Memory is stored in standard SQL databases (SQLite, PostgreSQL, MySQL) that you fully own and control.

### Why Memori?

- ✅ **One-line integration** - Works with OpenAI, Anthropic, LiteLLM, LangChain, and any LLM framework
- ✅ **SQL-native storage** - Portable, queryable, and auditable memory in databases you control
- ✅ **80-90% cost savings** - No expensive vector databases required
- ✅ **Zero vendor lock-in** - Export your memory as SQLite and move anywhere
- ✅ **Intelligent memory** - Automatic entity extraction, relationship mapping, and context prioritization

---

## Core Features

### 🧠 Dual Memory System

Memori provides two complementary memory modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Conscious Mode** | Background AI agent analyzes and promotes important memories | Stable context, faster responses |
| **Auto Mode** | Dynamic search per query for relevant memories | Real-time context, frequently changing scenarios |
| **Combined Mode** | Best of both worlds (Recommended) | Production applications |

### 🗄️ Database Support

| Database | Connection String | Use Case |
|----------|------------------|----------|
| SQLite | `sqlite:///my_memory.db` | Development, testing |
| PostgreSQL | `postgresql://user:pass@host/db` | Production |
| MySQL | `mysql://user:pass@host/db` | Production |
| Neon | `postgresql://user:pass@ep-*.neon.tech/db` | Serverless PostgreSQL |
| Supabase | `postgresql://postgres:pass@db.*.supabase.co/postgres` | PostgreSQL + Realtime |

### 🤖 LLM Framework Support

| Framework | Status | Usage |
|-----------|--------|-------|
| OpenAI | ✅ Native | `from openai import OpenAI` |
| Anthropic | ✅ Native | `from anthropic import Anthropic` |
| LiteLLM | ✅ Native | `from litellm import completion` |
| LangChain | ✅ Supported | Use with LiteLLM integration |
| Azure OpenAI | ✅ Supported | `ProviderConfig.from_azure()` |
| Custom APIs | ✅ Supported | `ProviderConfig.from_custom()` |

---

## Installation

### Basic Installation

```bash
pip install memorisdk
```

### With Optional Dependencies

```bash
# For environment variable management
pip install memorisdk python-dotenv

# For specific frameworks
pip install memorisdk langchain
pip install memorisdk crewai
```

### Requirements

- Python 3.8 or higher
- OpenAI API key (or other LLM provider credentials)

---

## Quick Start

### Minimal Example (3 lines!)

```python
from memori import Memori
from openai import OpenAI

# Initialize and enable Memori
memori = Memori(conscious_ingest=True)
memori.enable()

# Use OpenAI normally - memory is automatic!
client = OpenAI()

# First conversation
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "I'm building a FastAPI project"}]
)
print(response.choices[0].message.content)

# Later conversation - Memori automatically provides context
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Help me add authentication"}]
)
# AI automatically knows about your FastAPI project!
print(response.choices[0].message.content)
```

---

## Configuration

### Environment Variables

Set up environment variables for configuration:

```bash
# Core settings
export MEMORI_DATABASE__CONNECTION_STRING="postgresql://user:pass@localhost/memori"
export MEMORI_AGENTS__OPENAI_API_KEY="sk-..."
export MEMORI_MEMORY__NAMESPACE="production"

# Optional settings
export MEMORI_LOGGING__LEVEL="INFO"
export MEMORI_MEMORY__RETENTION_POLICY="30_days"
```

### Configuration File (memori.json)

Create a `memori.json` file in your project root:

```json
{
  "database": {
    "connection_string": "postgresql://user:pass@localhost/memori",
    "pool_size": 20
  },
  "agents": {
    "openai_api_key": "sk-...",
    "default_model": "gpt-4o-mini"
  },
  "memory": {
    "namespace": "production",
    "retention_policy": "30_days"
  }
}
```

### Using ConfigManager

```python
from memori import Memori, ConfigManager

# Auto-load from environment variables or config files
config = ConfigManager()
config.auto_load()

memori = Memori()
memori.enable()
```

### Direct Configuration

```python
from memori import Memori

memori = Memori(
    database_connect="sqlite:///my_memory.db",
    conscious_ingest=True,
    auto_ingest=True,
    openai_api_key="sk-...",
    namespace="my_app",
    verbose=True
)
memori.enable()
```

### Configuration Priority

Configuration is loaded in this order (highest to lowest):
1. Direct constructor parameters
2. Environment variables (`MEMORI_*`)
3. `MEMORI_CONFIG_PATH` environment variable
4. Configuration files (`memori.json`, `memori.yaml`)
5. Default Pydantic settings

---

## Memory Modes

### Conscious Mode

**One-shot working memory injection**

```python
memori = Memori(conscious_ingest=True)
```

**How it works:**
- Background AI agent analyzes conversations every 6 hours
- Promotes essential memories to short-term storage
- Injects promoted memories once per session
- Similar to human short-term working memory

**Best for:**
- Stable context scenarios
- Applications requiring fast response times
- Cost-sensitive deployments

### Auto Mode

**Dynamic memory search per query**

```python
memori = Memori(auto_ingest=True)
```

**How it works:**
- Searches entire database for each query
- Retrieves and injects 3-5 most relevant memories
- Real-time context matching

**Best for:**
- Frequently changing context
- Multi-user applications
- Maximum accuracy requirements

### Combined Mode (Recommended)

**Best of both worlds**

```python
memori = Memori(
    conscious_ingest=True,  # Core memories
    auto_ingest=True        # Dynamic supplement
)
```

**How it works:**
- Conscious mode provides stable core context
- Auto mode supplements with dynamic relevant memories
- Optimal balance of speed and accuracy

**Best for:**
- Production applications
- Complex AI systems
- Best user experience

---

## AI Provider Integration

### OpenAI

```python
from memori import Memori
from openai import OpenAI

memori = Memori(
    database_connect="sqlite:///openai_memory.db",
    conscious_ingest=True,
    openai_api_key="sk-..."
)
memori.enable()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Anthropic Claude

```python
from memori import Memori
import anthropic

memori = Memori(
    database_connect="sqlite:///claude_memory.db",
    conscious_ingest=True,
    openai_api_key="sk-..."  # For memory agent processing
)
memori.enable()

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Azure OpenAI

```python
from memori import Memori
from memori.core.providers import ProviderConfig
from openai import AzureOpenAI

# Configure Azure provider
azure_config = ProviderConfig.from_azure(
    api_key="your-azure-api-key",
    azure_endpoint="https://your-resource.openai.azure.com/",
    azure_deployment="your-deployment-name",
    api_version="2024-02-15-preview"
)

memori = Memori(
    database_connect="sqlite:///azure_memory.db",
    conscious_ingest=True,
    provider_config=azure_config
)
memori.enable()

client = AzureOpenAI(
    api_key=azure_config.api_key,
    azure_endpoint=azure_config.azure_endpoint,
    api_version=azure_config.api_version
)
```

### Ollama (Local Models)

```python
import os
from memori import Memori
from memori.core.providers import ProviderConfig

# Configure Ollama provider
ollama_provider = ProviderConfig.from_custom(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't require real API key
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b")
)

memori = Memori(
    database_connect="sqlite:///ollama_memory.db",
    conscious_ingest=True,
    auto_ingest=True,
    provider_config=ollama_provider
)

client = ollama_provider.create_client()
memori.enable()

# Chat with local model
response = client.chat.completions.create(
    model=ollama_provider.model,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Prerequisites:**
- Install Ollama: https://ollama.ai
- Run: `ollama serve`
- Pull model: `ollama pull llama3.2:3b`

### DeepSeek

```python
import os
from memori import Memori
from memori.core.providers import ProviderConfig

# Configure DeepSeek provider
deepseek_provider = ProviderConfig.from_custom(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
)

memori = Memori(
    database_connect="sqlite:///deepseek_memory.db",
    conscious_ingest=True,
    auto_ingest=True,
    provider_config=deepseek_provider
)

client = deepseek_provider.create_client()
memori.enable()

# Chat with DeepSeek
response = client.chat.completions.create(
    model=deepseek_provider.model,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Setup:**
```bash
# Get API key from: https://platform.deepseek.com/api_keys
export DEEPSEEK_API_KEY="your_api_key_here"
export DEEPSEEK_MODEL="deepseek-chat"  # or "deepseek-coder"
```

### LiteLLM (Universal)

```python
from memori import Memori
from litellm import completion

memori = Memori(
    database_connect="sqlite:///litellm_memory.db",
    conscious_ingest=True,
    openai_api_key="sk-..."
)
memori.enable()

# Works with any LiteLLM-supported model
response = completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Database Setup

### SQLite (Development)

**No setup required!** Just specify the file path:

```python
memori = Memori(
    database_connect="sqlite:///my_app_memory.db",
    conscious_ingest=True
)
```

**Pros:**
- Zero configuration
- Perfect for development and testing
- Portable single file

**Cons:**
- Not ideal for high concurrency
- Limited to single server

### PostgreSQL (Production)

**1. Install PostgreSQL:**
```bash
# macOS
brew install postgresql

# Ubuntu
sudo apt-get install postgresql

# Windows
# Download from: https://www.postgresql.org/download/
```

**2. Create database:**
```sql
CREATE DATABASE memori_db;
CREATE USER memori_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE memori_db TO memori_user;
```

**3. Configure Memori:**
```python
memori = Memori(
    database_connect="postgresql://memori_user:secure_password@localhost:5432/memori_db",
    conscious_ingest=True
)
```

### Neon (Serverless PostgreSQL)

**1. Sign up:** https://neon.tech

**2. Create project and get connection string**

**3. Configure Memori:**
```python
memori = Memori(
    database_connect="postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/memori",
    conscious_ingest=True
)
```

### Supabase

**1. Sign up:** https://supabase.com

**2. Create project and get connection string from Settings > Database**

**3. Configure Memori:**
```python
memori = Memori(
    database_connect="postgresql://postgres:password@db.projectref.supabase.co:5432/postgres",
    conscious_ingest=True
)
```

### MySQL

**1. Create database:**
```sql
CREATE DATABASE memori_db;
CREATE USER 'memori_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON memori_db.* TO 'memori_user'@'localhost';
```

**2. Configure Memori:**
```python
memori = Memori(
    database_connect="mysql://memori_user:secure_password@localhost:3306/memori_db",
    conscious_ingest=True
)
```

---

## Usage Examples

### Basic Personal Assistant

```python
from memori import Memori
from openai import OpenAI

# Initialize
memori = Memori(
    database_connect="sqlite:///assistant.db",
    conscious_ingest=True,
    auto_ingest=True,
    namespace="personal"
)
memori.enable()

client = OpenAI()

def chat(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful personal assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

# Usage
print(chat("My name is Alice and I love Python"))
print(chat("What's my name?"))  # AI remembers: "Your name is Alice!"
```

### Multi-User Application (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel
from memori import Memori
from openai import OpenAI
from typing import Dict

app = FastAPI()
user_memoris: Dict[str, Memori] = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

def get_user_memori(user_id: str) -> Memori:
    if user_id not in user_memoris:
        memori = Memori(
            database_connect="postgresql://user:pass@localhost/memori",
            namespace=f"user_{user_id}",  # Isolated per user
            conscious_ingest=True,
            auto_ingest=True
        )
        memori.enable()
        user_memoris[user_id] = memori
    return user_memoris[user_id]

@app.post("/chat")
async def chat(request: ChatRequest):
    memori = get_user_memori(request.user_id)
    client = OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": request.message}]
    )
    
    return {"response": response.choices[0].message.content}
```

### CrewAI Integration

```python
from memori import Memori
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Enable Memori
memori = Memori(
    database_connect="sqlite:///crewai_memory.db",
    conscious_ingest=True,
    namespace="crewai_project"
)
memori.enable()

llm = ChatOpenAI(model="gpt-4o-mini")

# Define agents
researcher = Agent(
    role="Researcher",
    goal="Research and gather information",
    backstory="You are an experienced researcher.",
    llm=llm
)

writer = Agent(
    role="Writer",
    goal="Write engaging content based on research",
    backstory="You are a talented writer.",
    llm=llm
)

# Define tasks
research_task = Task(
    description="Research FastAPI best practices",
    agent=researcher
)

write_task = Task(
    description="Write an article about FastAPI best practices",
    agent=writer
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task]
)

# Execute - all conversations automatically saved!
result = crew.kickoff()
```

### LangChain Integration

```python
from memori import Memori
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# Enable Memori
memori = Memori(
    database_connect="sqlite:///langchain_memory.db",
    conscious_ingest=True,
    namespace="langchain_app"
)
memori.enable()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{question}")
])

chain = prompt | llm | StrOutputParser()

# Use normally - memory automatic!
response = chain.invoke({"question": "I'm building a web app"})
print(response)

response = chain.invoke({"question": "What am I building?"})
print(response)  # AI remembers: "You're building a web app!"
```

### Interactive Chat Loop

```python
from memori import Memori
from openai import OpenAI

memori = Memori(
    database_connect="sqlite:///chat.db",
    conscious_ingest=True,
    auto_ingest=True
)
memori.enable()

client = OpenAI()

print("Chat with AI (type 'exit' to quit)")
print("-" * 50)

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}]
    )
    
    print(f"AI: {response.choices[0].message.content}\n")
```

---

## Troubleshooting

### Common Issues

#### Issue: "No module named 'memori'"

**Solution:**
```bash
pip install memorisdk
```

#### Issue: "API key not found"

**Solution:**
```bash
# Set environment variable
export OPENAI_API_KEY="sk-..."

# Or pass directly
memori = Memori(
    openai_api_key="sk-...",
    conscious_ingest=True
)
```

#### Issue: "Database locked" (SQLite)

**Solution:**
- Close other processes using the database
- Or switch to PostgreSQL for production:
```python
memori = Memori(
    database_connect="postgresql://user:pass@localhost/memori",
    conscious_ingest=True
)
```

#### Issue: "Connection timeout"

**Solution:**
- Check database connection string
- Verify database is running
- Test connection:
```python
import sqlalchemy
engine = sqlalchemy.create_engine("postgresql://user:pass@host/db")
engine.connect()
```

#### Issue: "Memory not persisting"

**Solution:**
- Ensure `memori.enable()` is called
- Check database connection
- Verify namespace matches:
```python
# Same namespace required
memori = Memori(namespace="my_app", ...)
```

#### Issue: "Ollama connection refused"

**Solution:**
```bash
# Start Ollama server
ollama serve

# Pull the model
ollama pull llama3.2:3b

# Verify it's running
curl http://localhost:11434/api/tags
```

#### Issue: "DeepSeek authentication error"

**Solution:**
```bash
# Check API key is set
echo $DEEPSEEK_API_KEY

# Get new key from: https://platform.deepseek.com/api_keys
export DEEPSEEK_API_KEY="your_key_here"
```

### Enable Debugging

```python
memori = Memori(
    database_connect="sqlite:///debug.db",
    conscious_ingest=True,
    verbose=True,  # Enable detailed logs
    log_level="DEBUG"
)
```

### Check Database Contents

```python
import sqlite3

conn = sqlite3.connect("my_memory.db")
cursor = conn.cursor()

# View all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

# View conversations
cursor.execute("SELECT * FROM chat_history LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()
```

---

## Resources

### Official Documentation

- **Memori Docs**: https://memorilabs.ai/docs
- **GitHub Repository**: https://github.com/GibsonAI/Memori
- **Architecture Guide**: https://memorilabs.ai/docs/open-source/architecture

### Community

- **Discord**: https://discord.gg/abD4eGym6v
- **Issues**: https://github.com/GibsonAI/Memori/issues
- **Discussions**: https://github.com/GibsonAI/Memori/discussions

### AI Provider Documentation

- **OpenAI**: https://platform.openai.com/docs
- **Anthropic**: https://docs.anthropic.com/
- **LiteLLM**: https://docs.litellm.ai/
- **Ollama**: https://ollama.ai/
- **DeepSeek**: https://platform.deepseek.com/docs

### Database Resources

- **PostgreSQL**: https://www.postgresql.org/docs/
- **SQLite**: https://www.sqlite.org/docs.html
- **Neon**: https://neon.tech/docs/introduction
- **Supabase**: https://supabase.com/docs

### Framework Integrations

- **LangChain**: https://python.langchain.com/docs/
- **CrewAI**: https://docs.crewai.com/
- **AutoGen**: https://microsoft.github.io/autogen/

---

## How It Works

Memori transparently intercepts LLM API calls using LiteLLM's native callback system:

**Pre-Call (Context Injection):**
1. Your app calls LLM API
2. Memori intercepts the call
3. Retrieval/Conscious Agent fetches relevant memories
4. Context injected into messages
5. Enhanced request sent to LLM

**Post-Call (Recording):**
6. LLM returns response
7. Memory Agent extracts entities and categorizes information
8. Conversation stored in SQL database with full-text search indexes
9. Original response returned to your app

**Background (every 6 hours - Conscious Mode):**
- Conscious Agent analyzes memory patterns
- Promotes essential memories from long-term to short-term storage
- Optimizes context injection for future queries

---

## License

Apache 2.0 - see [LICENSE](https://github.com/GibsonAI/Memori/blob/main/LICENSE)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](https://github.com/GibsonAI/Memori/blob/main/CONTRIBUTING.md)

---

## Support

- 📖 **Documentation**: https://memorilabs.ai/docs
- 💬 **Discord**: https://discord.gg/abD4eGym6v
- 🐛 **Issues**: https://github.com/GibsonAI/Memori/issues
- ⭐ **Star us on GitHub**: https://github.com/GibsonAI/Memori

---

<p align="center">
  <strong>Made with ❤️ by the Memori team</strong>
</p>

<p align="center">
  Give your AI the gift of memory 🧠
</p>
