import os
import time
import logging

from llama_index.core import Settings as LlamaSettings
from llama_index.core.llms import ChatMessage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def main() -> int:
    try:
        from dotenv import load_dotenv

        load_dotenv(".env")
        load_dotenv(".env.local", override=True)
    except Exception:
        pass

    api_key = os.getenv("OPENCODE_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENCODE_API_KEY in env")

    api_base = os.getenv("OPENCODE_BASE_URL", "https://opencode.ai/zen/go/v1")
    model = os.getenv("OPENCODE_MODEL", "deepseek-v4-flash")

    from llama_index.llms.openai_like import OpenAILike

    LlamaSettings.llm = OpenAILike(
        api_base=api_base,
        api_key=api_key,
        model=model,
        is_chat_model=True,
    )

    messages = [
        ChatMessage(role="system", content="You are a concise assistant."),
        ChatMessage(
            role="user",
            content="Tell me a joke about programming.",
        ),
    ]

    start = time.perf_counter()
    resp = LlamaSettings.llm.chat(messages)
    end = time.perf_counter()

    elapsed_ms = (end - start) * 1000.0
    logging.info("Model response time: %.2f ms", elapsed_ms)
    print(resp.message.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
