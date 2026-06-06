import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    # 1. Parse CLI prompt
    parser = argparse.ArgumentParser(
        description="Local coding agent using Ollama + gemma4:e4b"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable extra output (prompt and token usage)",
    )
    parser.add_argument(
        "user_prompt",
        type=str,
        help="User prompt for the coding agent",
    )
    args = parser.parse_args()

    # 2. Load env config
    load_dotenv()

    api_base = os.environ.get("LLM_API_BASE", "http://localhost:11434/v1")
    api_key = os.environ.get("LLM_API_KEY", "ollama")
    model = os.environ.get("LLM_MODEL", "gemma4:e4b")

    if api_base is None or api_key is None or model is None:
        raise RuntimeError(
            "Missing LLM configuration. "
            "Ensure LLM_API_BASE, LLM_API_KEY, and LLM_MODEL are set in your .env file."
        )

    client = OpenAI(
        base_url=api_base,
        api_key=api_key,
    )

    # 3. Build messages list (equivalent of list[types.Content])
    messages: list[dict[str, str]] = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    # 4. Call the model with the messages list
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    # 5. Verbose output: prompt + token usage (if available)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

        usage = getattr(response, "usage", None)
        if usage is None:
            raise Exception("need to include a user prompt")
            pass
        else:
            prompt_tokens = getattr(usage, "prompt_tokens", None)
            completion_tokens = getattr(usage, "completion_tokens", None)

            if prompt_tokens is not None and completion_tokens is not None:
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {completion_tokens}")

    # 6. Always print the model’s answer
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()