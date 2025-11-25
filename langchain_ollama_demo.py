import os

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from memori import Memori
from memori.core.providers import ProviderConfig

# Create Ollama provider configuration for Memori
# This enables Memori to track memory using Ollama
ollama_provider = ProviderConfig.from_custom(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't require an API key
    model=os.getenv("OLLAMA_MODEL", "gpt-oss:120b-cloud"),
)

print("Initializing Memori with Ollama for LangChain...")
ollama_memory = Memori(
    database_connect="sqlite:///langchain_ollama_demo.db",
    conscious_ingest=True,
    auto_ingest=True,
    verbose=True,
    provider_config=ollama_provider,
)

print("Enabling memory tracking...")
ollama_memory.enable()

# Create LangChain ChatOllama model
# LangChain will use this for conversations
model_name = os.getenv("OLLAMA_MODEL", "gpt-oss:120b-cloud")
llm = ChatOllama(
    model=model_name,
    base_url="http://localhost:11434",
    temperature=0.7,
)

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant with memory. You remember previous conversations and can reference them."),
    ("user", "{question}")
])

# Create the chain
chain = (
    {"question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(f"LangChain + Ollama + Memori Example - Chat with {model_name}")
print("Make sure Ollama is running locally (ollama serve)")
print("Type 'exit' or press Ctrl+C to quit")
print("-" * 50)

# Interactive chat loop
while True:
    try:
        user_input = input("\nYou: ")
        if not user_input.strip():
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("Processing with LangChain + Memori...")
        response = chain.invoke(user_input)
        print(f"AI: {response}")

    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        break
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running: 'ollama serve'")
        print(f"And that you have pulled the model: 'ollama pull {model_name}'")
        continue
