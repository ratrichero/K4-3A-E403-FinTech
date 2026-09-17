"""
Example Usage of LLM Provider Module
Demonstrates sync, async, and streaming calls with automatic fallback protection.
"""

import asyncio
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from langchain_core.messages import HumanMessage, SystemMessage

try:
    from .llm import get_llm
    from .config import get_settings
except ImportError:
    from llm import get_llm
    from config import get_settings


def demo_sync():
    print("\n--- 1. Synchronous Invocation ---")
    settings = get_settings()
    print(f"Primary Model: {settings.model_name}")
    print(f"Base URL: {settings.openai_base_url or 'Official OpenAI'}")

    llm = get_llm()
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Say 'Hello, LLMExtract is working!' in Vietnamese and English."),
    ]

    try:
        response = llm.invoke(messages)
        print(f"\nResponse:\n{response.content}\n")
    except Exception as exc:
        print(f"\nFailed to invoke model: {exc}")
        print("Tip: Ensure your OPENAI_API_KEY in .env is valid or configure OPENAI_BASE_URL (Groq, DeepSeek, Ollama).")


async def demo_async():
    print("\n--- 2. Asynchronous Invocation ---")
    llm = get_llm()
    prompt = "Give 3 tips for writing good prompts for LLMs. Answer in bullet points."

    try:
        response = await llm.ainvoke(prompt)
        print(f"\nResponse:\n{response.content}\n")
    except Exception as exc:
        print(f"\nAsync invocation error: {exc}")


async def demo_streaming():
    print("\n--- 3. Streaming Invocation ---")
    llm = get_llm()
    prompt = "Count from 1 to 5 with an emoji for each."

    try:
        print("Streaming: ", end="", flush=True)
        async for chunk in llm.astream(prompt):
            print(chunk.content, end="", flush=True)
        print("\n")
    except Exception as exc:
        print(f"\nStreaming error: {exc}")


if __name__ == "__main__":
    print("=" * 60)
    print("LLMExtract Demo — Multi-Provider & Fallback Runner")
    print("=" * 60)

    # 1. Sync
    demo_sync()

    # 2. Async & Streaming
    asyncio.run(demo_async())
    asyncio.run(demo_streaming())
