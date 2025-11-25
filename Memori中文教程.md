# Memori 中文教程

![Memori Banner](https://s3.us-east-1.amazonaws.com/images.memorilabs.ai/banner.png)

## 📚 目录

1. [项目简介](#项目简介)
2. [核心特性](#核心特性)
3. [工作原理](#工作原理)
4. [快速开始](#快速开始)
5. [记忆模式详解](#记忆模式详解)
6. [数据库支持](#数据库支持)
7. [LLM框架支持](#llm框架支持)
8. [配置详解](#配置详解)
9. [系统架构](#系统架架构)
10. [实战示例](#实战示例)
11. [框架集成](#框架集成)
12. [常见问题](#常见问题)

---

## 项目简介

### 什么是 Memori？

Memori 是一个开源的 SQL 原生记忆引擎，专为 LLM（大语言模型）、AI Agent 和多 Agent 系统设计。只需一行代码 `memori.enable()`，就能让任何 LLM 拥有持久化、可查询的记忆能力。

### 为什么选择 Memori？

- **🚀 一行代码集成** - 无缝集成 OpenAI、Anthropic、LiteLLM、LangChain 等主流框架
- **💾 SQL 原生存储** - 使用标准 SQL 数据库（SQLite、PostgreSQL、MySQL）存储记忆，完全可控
- **💰 节省 80-90% 成本** - 无需昂贵的向量数据库
- **🔓 零供应商锁定** - 支持导出为 SQLite，随时迁移
- **🧠 智能记忆** - 自动实体提取、关系映射和上下文优先级排序

**官方资源：**
- 📖 文档：https://memorilabs.ai/docs
- 💻 GitHub：https://github.com/GibsonAI/Memori
- 💬 Discord：https://discord.gg/abD4eGym6v

---

## 核心特性

### 1. 通用集成能力

Memori 通过 LiteLLM 的原生回调系统实现通用集成，支持：

- ✅ OpenAI（原生支持）
- ✅ Anthropic Claude（原生支持）
- ✅ Azure OpenAI（支持）
- ✅ LiteLLM（原生支持）
- ✅ LangChain（支持）
- ✅ 100+ 模型（通过 LiteLLM）

### 2. 多种记忆类型

| 类型 | 用途 | 保留时间 | 使用场景 |
|------|------|---------|---------|
| **短期记忆** | 最近对话 | 7-30 天 | 当前会话上下文 |
| **长期记忆** | 重要见解 | 永久 | 用户偏好、关键事实 |
| **规则记忆** | 用户偏好/约束 | 永久 | "我喜欢 Python"、"使用 pytest" |
| **实体记忆** | 人物、项目、技术 | 跟踪 | 关系映射 |

### 3. 双记忆模式

- **Conscious Mode（意识模式）** - 后台分析，智能提升重要记忆到短期存储
- **Auto Mode（自动模式）** - 每次查询动态搜索相关记忆
- **Combined Mode（组合模式）** - 两种模式结合使用，效果最佳

### 4. 多数据库支持

支持所有主流 SQL 数据库和云数据库：

- SQLite（本地开发）
- PostgreSQL（生产环境）
- MySQL（生产环境）
- Neon（Serverless PostgreSQL）
- Supabase（PostgreSQL）
- GibsonAI Platform（免费 Serverless 数据库）

---

## 工作原理

### 整体流程图

```
┌─────────────┐
│   你的应用   │
└─────┬───────┘
      │ 1. 调用 LLM API
      ▼
┌─────────────────┐
│ Memori 拦截器  │
└────┬────────┬───┘
     │        │
     │ 2. 获取上下文
     ▼        │
┌────────────┐│
│ SQL 数据库 ││
└────┬───────┘│
     │        │
     │ 3. 返回相关记忆
     └────────┘
     │
     │ 4. 注入上下文 + 调用 LLM
     ▼
┌─────────────────┐
│ OpenAI/Claude   │
│    等 LLM       │
└────┬────────────┘
     │ 5. 返回响应
     ▼
┌─────────────────┐
│ Memori 拦截器  │
└────┬────────────┘
     │ 6. 提取实体并存储
     ▼
┌────────────┐
│ SQL 数据库 │
└────────────┘
     │ 7. 返回响应给应用
     ▼
┌─────────────┐
│   你的应用   │
└─────────────┘

后台任务（每 6 小时）：
┌─────────────────┐
│  Conscious      │
│  Agent          │──► 分析模式，提升重要记忆
└─────────────────┘
```

### 三个阶段

#### 📥 调用前（上下文注入）

1. 应用调用 `client.chat.completions.create(messages=[...])`
2. Memori 透明拦截调用
3. **检索 Agent**（auto 模式）或 **Conscious Agent**（conscious 模式）检索相关记忆
4. 将上下文注入到消息中，然后发送给 LLM

#### 📤 调用后（记录存储）

5. LLM 提供商返回响应
6. **记忆 Agent** 提取实体，分类（事实、偏好、技能、规则、上下文）
7. 对话存储到 SQL 数据库，建立全文搜索索引
8. 将原始响应返回给应用

#### 🔄 后台任务（每 6 小时）

- **Conscious Agent** 分析记忆模式
- 将重要记忆从长期记忆提升到短期记忆
- 持续优化上下文注入效率

---

## 快速开始

### 安装

```bash
pip install memorisdk
```

### 基础用法

```python
from memori import Memori
from openai import OpenAI

# 初始化 Memori
memori = Memori(conscious_ingest=True)
memori.enable()

# 创建 OpenAI 客户端
client = OpenAI()

# 第一次对话 - 建立上下文
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "我正在开发一个 FastAPI 项目"}]
)
print(response.choices[0].message.content)

# 稍后对话 - Memori 自动提供上下文
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "帮我添加身份验证功能"}]
)
# LLM 自动知道你的 FastAPI 项目信息！
print(response.choices[0].message.content)
```

### 完整示例

```python
"""
Memori 基础使用示例
演示意识注入和上下文自动注入
"""
from dotenv import load_dotenv
from litellm import completion
from memori import Memori

load_dotenv()

def main():
    print("🧠 Memori - 带意识注入的 AI 记忆系统")
    print("=" * 55)

    # 使用意识注入初始化工作区记忆
    office_work = Memori(
        database_connect="sqlite:///office_memory.db",
        conscious_ingest=True,  # 🔥 启用 AI 驱动的后台分析
        verbose=True,  # 显示幕后发生的事情
        openai_api_key=None,  # 使用环境变量中的 OPENAI_API_KEY
    )

    # 启用记忆记录
    office_work.enable()
    print("✅ 记忆已启用 - 所有对话都将被记录！")

    # 第一次对话 - 建立上下文
    print("\n--- 第一次对话 ---")
    response1 = completion(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "我正在开发一个使用 PostgreSQL 数据库的 FastAPI 项目",
            }
        ],
    )
    print(f"助手: {response1.choices[0].message.content}")

    # 第二次对话 - 记忆自动提供上下文
    print("\n--- 第二次对话（带记忆上下文）---")
    response2 = completion(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "帮我写数据库连接代码"}
        ],
    )
    print(f"助手: {response2.choices[0].message.content}")

    # 第三次对话 - 展示偏好记忆
    print("\n--- 第三次对话（记住偏好）---")
    response3 = completion(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "我喜欢简洁、有详细文档和类型提示的代码",
            }
        ],
    )
    print(f"助手: {response3.choices[0].message.content}")

    # 第四次对话 - 记忆知道你的偏好
    print("\n--- 第四次对话（应用偏好）---")
    response4 = completion(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "告诉我如何创建用户模型"}
        ],
    )
    print(f"助手: {response4.choices[0].message.content}")

    print("\n🎉 完成！你的 AI 现在记住了：")
    print("  • 技术栈（FastAPI、PostgreSQL）")
    print("  • 编码偏好（简洁代码、类型提示）")
    print("  • 项目上下文（用户模型、数据库连接）")
    print("\n🧠 使用 conscious_ingest=True：")
    print("  • 后台分析会识别重要信息")
    print("  • 关键事实自动提升以便即时访问")
    print("  • 上下文注入随时间变得更智能")
    print("\n不再需要重复上下文 - 只需自然对话！")


if __name__ == "__main__":
    main()
```

---

## 记忆模式详解

### 1. Conscious Mode（意识模式）

**工作原理：**
- 一次性工作记忆注入
- 后台 Conscious Agent 每 6 小时分析记忆模式
- 自动将重要记忆提升到短期存储
- 类似人类的短期工作记忆

**使用场景：**
- 需要快速响应的应用
- 上下文相对稳定的场景
- 希望减少每次查询的数据库开销

**配置方式：**

```python
from memori import Memori

memori = Memori(
    database_connect="sqlite:///my_memory.db",
    conscious_ingest=True,  # 启用意识模式
    auto_ingest=False
)
memori.enable()
```

**优点：**
- ⚡ 快速 - 一次性注入，无需每次查询
- 🎯 精准 - 只提升最重要的记忆
- 💡 智能 - AI 自动分析重要性

**缺点：**
- 🕐 延迟 - 需要等待后台分析（最长 6 小时）
- 📊 可能遗漏 - 动态信息可能不会立即提升

### 2. Auto Mode（自动模式）

**工作原理：**
- 每次查询动态搜索相关记忆
- 检索 Agent 实时搜索整个数据库
- 注入 3-5 条最相关的记忆

**使用场景：**
- 需要实时上下文的应用
- 上下文频繁变化的场景
- 多用户系统，每个用户有独立记忆

**配置方式：**

```python
from memori import Memori

memori = Memori(
    database_connect="sqlite:///my_memory.db",
    conscious_ingest=False,
    auto_ingest=True  # 启用自动模式
)
memori.enable()
```

**优点：**
- 🔄 实时 - 立即获取最新相关记忆
- 🎯 准确 - 基于当前查询动态匹配
- 📈 全面 - 搜索整个数据库

**缺点：**
- 🐌 较慢 - 每次查询都需要数据库搜索
- 💰 成本 - 更多的数据库查询

### 3. Combined Mode（组合模式）⭐ 推荐

**工作原理：**
- 结合两种模式的优点
- Conscious Mode 提供稳定的核心上下文
- Auto Mode 补充动态相关记忆

**配置方式：**

```python
from memori import Memori

memori = Memori(
    database_connect="sqlite:///my_memory.db",
    conscious_ingest=True,  # 启用意识模式
    auto_ingest=True        # 同时启用自动模式
)
memori.enable()
```

**优点：**
- ✨ 最佳效果 - 兼顾速度和准确性
- 🧠 最智能 - 核心记忆 + 动态补充
- 🚀 生产就绪 - 适合大多数生产场景

**推荐用于：**
- 生产环境
- 复杂的 AI 应用
- 需要最佳用户体验的场景

---

## 数据库支持

### 支持的数据库

| 数据库 | 连接字符串示例 | 适用场景 |
|--------|---------------|---------|
| **SQLite** | `sqlite:///my_memory.db` | 本地开发、测试 |
| **PostgreSQL** | `postgresql://user:pass@localhost/memori` | 生产环境 |
| **MySQL** | `mysql://user:pass@localhost/memori` | 生产环境 |
| **Neon** | `postgresql://user:pass@ep-*.neon.tech/memori` | Serverless PostgreSQL |
| **Supabase** | `postgresql://postgres:pass@db.*.supabase.co/postgres` | PostgreSQL + 实时功能 |
| **GibsonAI** | 通过平台获取 | 免费 Serverless 数据库 |

### 数据库配置示例

#### SQLite（本地开发）

```python
from memori import Memori

memori = Memori(
    database_connect="sqlite:///my_app_memory.db",
    conscious_ingest=True
)
memori.enable()
```

#### PostgreSQL（生产环境）

```python
from memori import Memori

memori = Memori(
    database_connect="postgresql://username:password@localhost:5432/memori_db",
    conscious_ingest=True,
    auto_ingest=True
)
memori.enable()
```

#### Neon（Serverless）

```python
from memori import Memori

memori = Memori(
    database_connect="postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/memori",
    conscious_ingest=True
)
memori.enable()
```

#### 使用环境变量

```python
# .env 文件
MEMORI_DATABASE__CONNECTION_STRING=postgresql://user:pass@localhost/memori
MEMORI_AGENTS__OPENAI_API_KEY=sk-...
MEMORI_MEMORY__NAMESPACE=production

# Python 代码
from memori import Memori, ConfigManager

config = ConfigManager()
config.auto_load()  # 自动从环境变量加载

memori = Memori()
memori.enable()
```

### 数据库架构

Memori 使用以下核心表结构：

```sql
-- 所有对话历史
CREATE TABLE chat_history (
    id TEXT PRIMARY KEY,
    user_input TEXT,
    ai_output TEXT,
    model TEXT,
    timestamp DATETIME,
    session_id TEXT,
    namespace TEXT,
    metadata JSON
);

-- 短期记忆（提升的重要记忆）
CREATE TABLE short_term_memory (
    id TEXT PRIMARY KEY,
    conversation_id TEXT,
    category TEXT,
    importance_score REAL,
    frequency_score REAL,
    recency_score REAL,
    summary TEXT,
    searchable_content TEXT,
    expires_at DATETIME,
    FOREIGN KEY (conversation_id) REFERENCES chat_history(id)
);

-- 长期记忆（所有处理过的记忆）
CREATE TABLE long_term_memory (
    id TEXT PRIMARY KEY,
    conversation_id TEXT,
    category TEXT,
    subcategory TEXT,
    retention_type TEXT,
    importance_score REAL,
    summary TEXT,
    searchable_content TEXT,
    reasoning TEXT,
    timestamp DATETIME,
    namespace TEXT,
    FOREIGN KEY (conversation_id) REFERENCES chat_history(id)
);

-- 提取的实体
CREATE TABLE memory_entities (
    id TEXT PRIMARY KEY,
    memory_id TEXT,
    entity_type TEXT,
    entity_value TEXT,
    confidence REAL,
    FOREIGN KEY (memory_id) REFERENCES long_term_memory(id)
);

-- 实体关系
CREATE TABLE memory_relationships (
    id TEXT PRIMARY KEY,
    from_entity_id TEXT,
    to_entity_id TEXT,
    relationship_type TEXT,
    strength REAL,
    FOREIGN KEY (from_entity_id) REFERENCES memory_entities(id),
    FOREIGN KEY (to_entity_id) REFERENCES memory_entities(id)
);
```

---

## LLM框架支持

### 支持的框架

| 框架 | 状态 | 使用方式 |
|------|------|---------|
| **OpenAI** | ✅ 原生支持 | `from openai import OpenAI` |
| **Anthropic** | ✅ 原生支持 | `from anthropic import Anthropic` |
| **LiteLLM** | ✅ 原生支持 | `from litellm import completion` |
| **LangChain** | ✅ 支持 | 通过 LiteLLM 集成 |
| **Azure OpenAI** | ✅ 支持 | `ProviderConfig.from_azure()` |
| **100+ 模型** | ✅ 支持 | 任何 LiteLLM 兼容的提供商 |

### 使用 OpenAI

```python
from memori import Memori
from openai import OpenAI

memori = Memori(conscious_ingest=True)
memori.enable()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好"}]
)
# 自动记录并注入上下文
```

### 使用 Anthropic Claude

```python
from memori import Memori
import anthropic

memori = Memori(conscious_ingest=True)
memori.enable()

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好"}]
)
# 自动记录并注入上下文
```

### 使用 LiteLLM

```python
from memori import Memori
from litellm import completion

memori = Memori(conscious_ingest=True)
memori.enable()

response = completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好"}]
)
# 自动记录并注入上下文
```

### 使用 Azure OpenAI

```python
from memori import Memori
from memori.core.providers import ProviderConfig

# 配置 Azure OpenAI
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

# 使用 Azure OpenAI 客户端
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=azure_config.api_key,
    azure_endpoint=azure_config.azure_endpoint,
    api_version=azure_config.api_version
)

response = client.chat.completions.create(
    model="your-deployment-name",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 使用自定义端点（如 Ollama）

```python
from memori import Memori
from memori.core.providers import ProviderConfig

# 配置自定义端点
custom_config = ProviderConfig.from_custom(
    base_url="http://localhost:11434/v1",  # Ollama 端点
    api_key="ollama",  # Ollama 不需要真实 API 密钥
    model="llama2"
)

memori = Memori(
    database_connect="sqlite:///ollama_memory.db",
    conscious_ingest=True,
    provider_config=custom_config
)
memori.enable()
```

---

## 配置详解

### 配置优先级

Memori 使用分层配置系统，优先级从高到低：

1. **直接构造参数** - `Memori(database_connect="...")`
2. **环境变量** - `MEMORI_DATABASE__CONNECTION_STRING`
3. **配置文件路径** - `MEMORI_CONFIG_PATH` 环境变量
4. **配置文件** - `memori.json` 或 `memori.yaml`
5. **默认设置** - Pydantic 模型的默认值

### 使用 ConfigManager（推荐）

```python
from memori import Memori, ConfigManager

# 自动加载配置
config = ConfigManager()
config.auto_load()  # 从所有源自动加载

memori = Memori()  # 使用已加载的配置
memori.enable()
```

### 环境变量配置

```bash
# 数据库配置
export MEMORI_DATABASE__CONNECTION_STRING="postgresql://user:pass@localhost/memori"
export MEMORI_DATABASE__POOL_SIZE=20

# Agent 配置
export MEMORI_AGENTS__OPENAI_API_KEY="sk-..."
export MEMORI_AGENTS__DEFAULT_MODEL="gpt-4o-mini"

# 记忆配置
export MEMORI_MEMORY__NAMESPACE="production"
export MEMORI_MEMORY__RETENTION_POLICY="30_days"

# 日志配置
export MEMORI_LOGGING__LEVEL="INFO"
export MEMORI_LOGGING__FILE_PATH="/var/log/memori.log"
```

### 配置文件（memori.json）

```json
{
  "database": {
    "connection_string": "postgresql://user:pass@localhost/memori",
    "pool_size": 20,
    "echo": false
  },
  "agents": {
    "openai_api_key": "sk-...",
    "default_model": "gpt-4o-mini",
    "temperature": 0.7
  },
  "memory": {
    "namespace": "production",
    "retention_policy": "30_days",
    "max_context_length": 4000
  },
  "logging": {
    "level": "INFO",
    "file_path": "/var/log/memori.log",
    "format": "json"
  },
  "integrations": {
    "agentops_api_key": null,
    "langsmith_api_key": null
  }
}
```

### 配置文件（memori.yaml）

```yaml
database:
  connection_string: postgresql://user:pass@localhost/memori
  pool_size: 20
  echo: false

agents:
  openai_api_key: sk-...
  default_model: gpt-4o-mini
  temperature: 0.7

memory:
  namespace: production
  retention_policy: 30_days
  max_context_length: 4000

logging:
  level: INFO
  file_path: /var/log/memori.log
  format: json

integrations:
  agentops_api_key: null
  langsmith_api_key: null
```

### 完整配置示例

```python
from memori import Memori
from memori.core.providers import ProviderConfig

# 方式 1：直接参数配置
memori = Memori(
    # 数据库配置
    database_connect="postgresql://user:pass@localhost/memori",
    
    # 记忆模式
    conscious_ingest=True,  # 启用意识模式
    auto_ingest=True,       # 启用自动模式
    
    # Agent 配置
    openai_api_key="sk-...",
    default_model="gpt-4o-mini",
    temperature=0.7,
    
    # 记忆配置
    namespace="my_app",  # 命名空间隔离
    retention_days=30,   # 保留天数
    
    # 日志配置
    verbose=True,  # 详细日志
    log_level="INFO",
    
    # 提供商配置
    provider_config=ProviderConfig.from_openai(
        api_key="sk-...",
        organization="org-..."
    )
)

memori.enable()

# 方式 2：使用 ConfigManager
from memori import ConfigManager

config = ConfigManager()
config.auto_load()

memori = Memori()
memori.enable()
```

### 命名空间（Namespace）

命名空间用于隔离不同应用或用户的记忆：

```python
# 应用 A 的记忆
memori_app_a = Memori(
    database_connect="sqlite:///shared_memory.db",
    namespace="app_a",
    conscious_ingest=True
)
memori_app_a.enable()

# 应用 B 的记忆
memori_app_b = Memori(
    database_connect="sqlite:///shared_memory.db",
    namespace="app_b",
    conscious_ingest=True
)
memori_app_b.enable()

# 多用户隔离
def get_user_memori(user_id: str):
    return Memori(
        database_connect="postgresql://user:pass@localhost/memori",
        namespace=f"user_{user_id}",
        conscious_ingest=True
    )
```

---

## 系统架构

### 核心组件

Memori 由以下核心组件组成：

#### 1. Memori 类（入口点）

用户交互的主要接口：

```python
class Memori:
    def __init__(self,
                 database_connect,
                 conscious_ingest=True,
                 auto_ingest=False,
                 provider_config=None,
                 ...):
        # 初始化所有子系统

    def enable(self):
        # 使用 LiteLLM 回调启动通用记录

    def disable(self):
        # 停止记录并清理

    def trigger_conscious_analysis(self):
        # 手动触发后台分析
```

**职责：**
- 通过 ConfigManager 管理配置
- 使用提供商支持初始化组件
- 两种记忆模式的生命周期管理
- 公共 API 接口和记忆工具

#### 2. 记忆管理器 & LiteLLM 集成

与 LiteLLM 回调系统的原生集成：

```python
class MemoryManager:
    def enable(self, interceptors=None):
        # 使用 LiteLLM 原生回调进行通用记录

    def record_conversation(self, user_input, ai_output, model):
        # 自动处理和存储对话
```

**工作方式：**
- 使用 LiteLLM 的原生回调系统进行通用记录
- 支持 OpenAI、Anthropic、Azure OpenAI 和 100+ 提供商
- 无需 monkey-patching 的自动对话提取
- 支持 Azure 和自定义端点的提供商配置

#### 3. 双记忆系统

两种互补的记忆模式：

**Conscious Ingest Mode（意识注入模式）：**

```python
class ConsciouscMode:
    def __init__(self, conscious_ingest=True):
        # 一次性工作记忆注入

    def inject_context(self, messages):
        # 每个会话注入一次重要记忆
        # 类似人类的短期记忆
```

**Auto Ingest Mode（自动注入模式）：**

```python
class AutoIngestMode:
    def __init__(self, auto_ingest=True):
        # 每次查询动态记忆搜索

    def get_context(self, user_input):
        # 搜索整个数据库寻找相关记忆
        # 每次调用注入 3-5 条最相关的记忆
```

#### 4. Agent 系统

三个专门的 AI Agent 用于智能记忆处理：

**Memory Agent（记忆 Agent）：**

```python
class MemoryAgent:
    def process_conversation(self, user_input, ai_output):
        # 使用 OpenAI 结构化输出和 Pydantic
        return ProcessedMemory(
            category=...,
            entities=...,
            importance=...,
            summary=...
        )
```

**Conscious Agent（意识 Agent）：**

```python
class ConsciouscAgent:
    def analyze_patterns(self):
        # 每 6 小时分析记忆模式
        # 将重要对话提升到工作记忆
        return EssentialMemoriesAnalysis(
            essential_memories=[...],
            analysis_reasoning="..."
        )

    def run_conscious_ingest(self, db_manager, namespace):
        # 后台分析进行记忆提升
```

**Retrieval Agent（检索 Agent）：**

```python
class RetrievalAgent:
    def execute_search(self, query, db_manager, namespace, limit=5):
        # 智能数据库搜索（自动注入模式）
        # 理解查询意图并找到相关记忆
        return RelevantMemories(
            memories=[...],
            search_strategy="semantic",
            relevance_scores=[...]
        )
```

#### 5. 提供商配置系统

支持多个 LLM 提供商的统一配置：

```python
class ProviderConfig:
    @classmethod
    def from_azure(cls, api_key, azure_endpoint, azure_deployment, ...):
        # Azure OpenAI 配置

    @classmethod
    def from_openai(cls, api_key, organization=None, ...):
        # 标准 OpenAI 配置

    @classmethod
    def from_custom(cls, base_url, api_key, model):
        # 自定义端点配置（Ollama 等）

    def create_client(self):
        # 创建配置的 OpenAI 兼容客户端
```

#### 6. 记忆工具系统

用于 AI Agent 的函数调用集成：

```python
from memori import create_memory_tool

def setup_memory_tools(memori_instance):
    # 为函数调用创建记忆搜索工具
    memory_tool = create_memory_tool(memori_instance)

    return {
        "type": "function",
        "function": {
            "name": "search_memory",
            "description": "搜索记忆中相关的过去对话",
            "parameters": {...}
        }
    }
```

#### 7. 数据库层

支持多数据库和智能查询：

```python
class DatabaseManager:
    def __init__(self, connection_string):
        # 支持 SQLite、PostgreSQL、MySQL
        # 云数据库：Neon、Supabase、GibsonAI

    def initialize_schema(self):
        # 创建表、索引、全文搜索

    def store_memory(self, processed_memory):
        # 存储关系和全文索引

    def search_memories(self, query, namespace, limit=5):
        # 带排名和命名空间隔离的全文搜索
```

### 数据流程

#### 对话捕获（LiteLLM 原生）

```
你的应用
   │
   ├─→ LLM API 调用
   │
   ▼
LiteLLM/OpenAI
   │
   ├─→ 原生回调触发
   │
   ▼
LiteLLM 回调
   │
   ├─→ 处理对话
   │
   ▼
Memory Agent
   │
   ├─→ 提取实体 & 分类
   │
   ▼
数据库
   │
   ├─→ 存储处理后的记忆
   │
   ▼
返回原始响应给应用
```

#### Conscious Mode：后台分析 & 提升

```
6小时定时器
   │
   ├─→ 触发分析
   │
   ▼
Conscious Agent
   │
   ├─→ 获取所有记忆
   │
   ▼
分析模式 & 重要性
   │
   ├─→ 选择重要记忆
   │
   ▼
提升到工作记忆（短期存储）
   │
   ├─→ 更新分析时间戳
   │
   ▼
完成
```

#### Auto Mode：动态上下文检索

```
你的应用
   │
   ├─→ 新查询
   │
   ▼
Retrieval Agent
   │
   ├─→ 智能搜索
   │
   ▼
数据库
   │
   ├─→ 返回结果
   │
   ▼
排名 & 选择前 5 条
   │
   ├─→ 注入上下文
   │
   ▼
LLM API
   │
   ├─→ 上下文化响应
   │
   ▼
返回给应用
```

---

## 实战示例

### 示例 1：个人助手

```python
"""
个人助手示例
演示如何构建带记忆的个人 AI 助手
"""
from memori import Memori
from openai import OpenAI
from datetime import datetime

# 初始化个人助手记忆
personal_assistant = Memori(
    database_connect="sqlite:///personal_assistant.db",
    conscious_ingest=True,
    auto_ingest=True,  # 组合模式
    namespace="personal",
    verbose=True
)
personal_assistant.enable()

client = OpenAI()

def chat(message: str):
    """与助手聊天"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "你是一个有用的个人助手，能记住用户的偏好和之前的对话。"
            },
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

# 使用示例
if __name__ == "__main__":
    # 第一天
    print("第一天：")
    print(chat("我喜欢喝咖啡，每天早上 8 点起床"))
    print(chat("我正在学习 Python 和机器学习"))
    
    # 第二天
    print("\n第二天：")
    print(chat("早上好！今天有什么建议吗？"))
    # 助手会记得你喜欢咖啡和早上 8 点起床
    
    print(chat("推荐一些 Python 学习资源"))
    # 助手会记得你正在学习 Python
```

### 示例 2：多用户应用（FastAPI）

```python
"""
多用户 FastAPI 应用示例
演示如何为每个用户隔离记忆
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from memori import Memori
from openai import OpenAI
from typing import Dict

app = FastAPI()

# 用户记忆缓存
user_memoris: Dict[str, Memori] = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    user_id: str

def get_user_memori(user_id: str) -> Memori:
    """获取或创建用户的 Memori 实例"""
    if user_id not in user_memoris:
        memori = Memori(
            database_connect="postgresql://user:pass@localhost/memori",
            namespace=f"user_{user_id}",  # 每个用户独立的命名空间
            conscious_ingest=True,
            auto_ingest=True
        )
        memori.enable()
        user_memoris[user_id] = memori
    
    return user_memoris[user_id]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天端点"""
    try:
        # 确保用户有自己的记忆
        memori = get_user_memori(request.user_id)
        
        # 创建 OpenAI 客户端
        client = OpenAI()
        
        # 发送消息
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request.message}]
        )
        
        return ChatResponse(
            response=response.choices[0].message.content,
            user_id=request.user_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/memories")
async def get_user_memories(user_id: str):
    """获取用户的记忆摘要"""
    memori = get_user_memori(user_id)
    
    # 这里可以添加自定义逻辑来获取和格式化记忆
    return {
        "user_id": user_id,
        "namespace": f"user_{user_id}",
        "status": "active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 示例 3：记忆检索（函数调用）

```python
"""
记忆检索示例
演示如何使用函数调用进行记忆检索
"""
from memori import Memori, create_memory_tool
from openai import OpenAI
import json

# 初始化 Memori
memori = Memori(
    database_connect="sqlite:///memory_retrieval.db",
    conscious_ingest=True,
    verbose=True
)
memori.enable()

client = OpenAI()

# 创建记忆搜索工具
memory_tool = create_memory_tool(memori)

# 首先存储一些信息
print("存储信息...")
conversations = [
    "我的名字是张三，我是一名软件工程师",
    "我喜欢用 Python 和 JavaScript 编程",
    "我最喜欢的框架是 FastAPI 和 React",
    "我正在开发一个电商平台项目"
]

for conv in conversations:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": conv}]
    )
    print(f"✓ 已存储: {conv}")

print("\n使用函数调用检索记忆...")

# 使用函数调用
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "我使用什么编程语言？"}
    ],
    tools=[memory_tool],
    tool_choice="auto"
)

# 处理工具调用
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"\n🔍 调用工具: {tool_call.function.name}")
    print(f"参数: {tool_call.function.arguments}")
    
    # 执行搜索
    args = json.loads(tool_call.function.arguments)
    # 这里可以调用实际的搜索逻辑
    
print(f"\n💬 最终响应: {response.choices[0].message.content}")
```

### 示例 4：CrewAI 集成

```python
"""
CrewAI 集成示例
演示 Memori 与 CrewAI 多 Agent 系统的集成
"""
from memori import Memori
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# 初始化 Memori
memori = Memori(
    database_connect="sqlite:///crewai_memory.db",
    conscious_ingest=True,
    auto_ingest=True,
    namespace="crewai_project"
)
memori.enable()

# 创建 LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# 定义 Agent
researcher = Agent(
    role="研究员",
    goal="研究和收集关于主题的信息",
    backstory="你是一个经验丰富的研究员，擅长查找和分析信息。",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="作家",
    goal="基于研究撰写引人入胜的内容",
    backstory="你是一个有才华的作家，能够将复杂的信息转化为易懂的内容。",
    llm=llm,
    verbose=True
)

# 定义任务
research_task = Task(
    description="研究 FastAPI 框架的最佳实践",
    agent=researcher,
    expected_output="FastAPI 最佳实践的详细研究报告"
)

write_task = Task(
    description="根据研究撰写一篇关于 FastAPI 最佳实践的文章",
    agent=writer,
    expected_output="一篇结构良好的 FastAPI 最佳实践文章"
)

# 创建 Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

# 执行
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "="*50)
    print("最终结果：")
    print(result)
    print("="*50)
    print("\n✅ 所有对话和结果都已自动存储到 Memori！")
```

### 示例 5：LangChain 集成

```python
"""
LangChain 集成示例
演示 Memori 与 LangChain 的集成
"""
from memori import Memori
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

# 初始化 Memori
memori = Memori(
    database_connect="sqlite:///langchain_memory.db",
    conscious_ingest=True,
    auto_ingest=True,
    namespace="langchain_app"
)
memori.enable()

# 创建 LangChain 组件
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手，记住之前的对话。"),
    ("user", "{question}")
])

# 创建链
chain = (
    {"question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 使用示例
if __name__ == "__main__":
    questions = [
        "我正在开发一个 Web 应用，使用 Python",
        "我应该用什么框架？",
        "如何连接数据库？",
        "提醒我，我在开发什么？"
    ]
    
    for q in questions:
        print(f"\n❓ 问题: {q}")
        response = chain.invoke(q)
        print(f"💬 回答: {response}")
    
    print("\n✅ 所有对话都已自动记录到 Memori！")
```

---

## 框架集成

Memori 提供了与主流 AI 框架的集成示例：

### 支持的框架

| 框架 | 描述 | 示例代码 |
|------|------|---------|
| **AgentOps** | 带可观测性的记忆操作跟踪 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/agentops_example.py) |
| **Agno** | 带持久对话的 Agent 框架 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/agno_example.py) |
| **AWS Strands** | 带持久记忆的 Strands SDK | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/aws_strands_example.py) |
| **Azure AI Foundry** | Azure 企业 AI Agent | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/azure_ai_foundry_example.py) |
| **AutoGen** | 多 Agent 群聊记忆 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/autogen_example.py) |
| **CamelAI** | 多 Agent 通信框架 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/camelai_example.py) |
| **CrewAI** | 多 Agent 共享记忆 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/crewai_example.py) |
| **Digital Ocean AI** | 带历史的客户支持 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/digital_ocean_example.py) |
| **LangChain** | 企业 Agent 框架 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/langchain_example.py) |
| **OpenAI Agent** | 带偏好的函数调用 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/openai_agent_example.py) |
| **Swarms** | 多 Agent 持久记忆 | [示例](https://github.com/GibsonAI/Memori/blob/main/examples/integrations/swarms_example.py) |

### 集成模式

所有框架集成都遵循相同的简单模式：

```python
# 1. 导入 Memori
from memori import Memori

# 2. 初始化 Memori
memori = Memori(
    database_connect="sqlite:///framework_memory.db",
    conscious_ingest=True,
    namespace="my_framework"
)

# 3. 启用记忆
memori.enable()

# 4. 正常使用你的框架
# 所有 LLM 调用都会自动记录和注入上下文
```

---

## 常见问题

### Q1: Memori 如何工作？

**A:** Memori 通过 LiteLLM 的原生回调系统拦截 LLM API 调用。在调用前注入相关上下文，在调用后提取和存储记忆。完全透明，无需修改现有代码。

### Q2: 是否需要修改现有代码？

**A:** 不需要！只需添加 3 行代码：

```python
from memori import Memori
memori = Memori(conscious_ingest=True)
memori.enable()
```

然后正常使用你的 LLM 框架，Memori 会自动处理其余部分。

### Q3: 数据存储在哪里？

**A:** 数据存储在你选择的 SQL 数据库中（SQLite、PostgreSQL、MySQL 等）。你完全拥有和控制数据，可以随时导出或迁移。

### Q4: 是否支持多用户？

**A:** 是的！使用命名空间（namespace）来隔离不同用户的记忆：

```python
memori = Memori(
    database_connect="postgresql://...",
    namespace=f"user_{user_id}",
    conscious_ingest=True
)
```

### Q5: Conscious 和 Auto 模式哪个更好？

**A:** 建议同时使用两种模式（组合模式）：

```python
memori = Memori(
    conscious_ingest=True,  # 核心记忆
    auto_ingest=True        # 动态补充
)
```

这样可以获得最佳性能和准确性。

### Q6: 如何处理隐私和安全？

**A:** 
- 所有数据存储在你自己的数据库中
- 支持命名空间隔离
- 可以使用加密的数据库连接
- 支持自定义保留策略
- 可以随时删除或导出数据

### Q7: 成本如何？

**A:** 
- Memori 本身是开源免费的
- 只需支付 LLM API 调用费用（与正常使用相同）
- 由于智能上下文注入，实际上可以减少不必要的 API 调用
- 无需昂贵的向量数据库，节省 80-90% 存储成本

### Q8: 支持哪些 LLM？

**A:** 支持所有 LiteLLM 兼容的 LLM：
- OpenAI（GPT-3.5、GPT-4、GPT-4o 等）
- Anthropic（Claude 系列）
- Azure OpenAI
- Google PaLM
- Cohere
- Ollama（本地模型）
- 100+ 其他模型

### Q9: 如何监控和调试？

**A:** 启用详细日志：

```python
memori = Memori(
    database_connect="sqlite:///my_memory.db",
    conscious_ingest=True,
    verbose=True,  # 启用详细日志
    log_level="DEBUG"
)
```

### Q10: 可以自定义记忆处理吗？

**A:** 是的！Memori 提供了灵活的配置选项：

```python
memori = Memori(
    database_connect="postgresql://...",
    conscious_ingest=True,
    
    # 自定义 Agent 模型
    default_model="gpt-4o-mini",
    temperature=0.7,
    
    # 自定义保留策略
    retention_days=30,
    
    # 自定义命名空间
    namespace="custom_app",
    
    # 自定义提供商
    provider_config=ProviderConfig.from_custom(...)
)
```

### Q11: 如何迁移现有数据？

**A:** Memori 使用标准 SQL 数据库，可以轻松迁移：

```python
# 从 SQLite 迁移到 PostgreSQL
# 1. 导出 SQLite 数据
# 2. 导入到 PostgreSQL
# 3. 更新连接字符串

memori = Memori(
    database_connect="postgresql://new-db/memori",  # 新数据库
    conscious_ingest=True
)
```

### Q12: 性能如何优化？

**A:** 性能优化建议：

1. **使用 PostgreSQL** - 比 SQLite 更快（生产环境）
2. **启用组合模式** - 平衡速度和准确性
3. **合理设置保留期** - 避免数据库过大
4. **使用命名空间** - 减少搜索范围
5. **定期清理过期数据** - 保持数据库性能

```python
memori = Memori(
    database_connect="postgresql://...",  # 使用 PostgreSQL
    conscious_ingest=True,
    auto_ingest=True,
    retention_days=30,  # 30 天保留期
    namespace="optimized_app"
)
```

---

## 总结

Memori 是一个强大而灵活的 AI 记忆引擎，具有以下优势：

✅ **简单易用** - 一行代码即可集成  
✅ **通用兼容** - 支持所有主流 LLM 和框架  
✅ **完全可控** - 数据存储在你自己的数据库中  
✅ **智能高效** - 双记忆模式，自动分析和提升  
✅ **生产就绪** - 完善的错误处理和配置系统  
✅ **开源免费** - Apache 2.0 许可证  

### 快速开始步骤

1. **安装**：`pip install memorisdk`
2. **初始化**：`memori = Memori(conscious_ingest=True)`
3. **启用**：`memori.enable()`
4. **使用**：正常使用你的 LLM 框架

就这么简单！Memori 会自动处理记忆的存储、检索和注入。

### 获取帮助

- 📖 **文档**：https://memorilabs.ai/docs
- 💻 **GitHub**：https://github.com/GibsonAI/Memori
- 💬 **Discord**：https://discord.gg/abD4eGym6v
- 🐛 **问题反馈**：https://github.com/GibsonAI/Memori/issues

### 参与贡献

Memori 是开源项目，欢迎社区贡献！查看 [贡献指南](https://github.com/GibsonAI/Memori/blob/main/CONTRIBUTING.md) 了解如何参与。

### 许可证

Apache 2.0 - 详见 [LICENSE](https://github.com/GibsonAI/Memori/blob/main/LICENSE)

---

**⭐ 如果觉得 Memori 有用，请在 GitHub 上给我们一个 Star！**

[![Star History](https://api.star-history.com/svg?repos=GibsonAI/memori&type=date)](https://star-history.com/#GibsonAI/memori)
