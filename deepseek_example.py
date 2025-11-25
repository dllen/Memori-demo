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
