import argparse
import os
import sys
import json

from dotenv import load_dotenv
from openai import OpenAI

import prompts
from functions.call_functions import available_functions, call_function


def main() -> None:
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

    messages = [
        {
            "role": "system",
            "content": prompts.system_prompt,
        },
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]

    max_iterations = 20

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=available_functions,
            tool_choice="auto",
            temperature=0,
        )

        choice = response.choices[0]
        message = choice.message

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            usage = getattr(response, "usage", None)
            if usage is None:
                print("Token usage information not available from this backend.")
            else:
                prompt_tokens = getattr(usage, "prompt_tokens", None)
                completion_tokens = getattr(usage, "completion_tokens", None)
                if prompt_tokens is not None and completion_tokens is not None:
                    print(f"Prompt tokens: {prompt_tokens}")
                    print(f"Response tokens: {completion_tokens}")

        # Preserve the full message object so tool_calls stay attached
        messages.append(message)

        tool_calls = getattr(message, "tool_calls", None)

        if not tool_calls:
            print("Final response:")
            print(message.content)
            return

        for tool_call in tool_calls:
            func = tool_call.function
            function_name = func.name or ""
            arguments = func.arguments

            if isinstance(arguments, str):
                raw_args = json.loads(arguments)
            else:
                raw_args = arguments

            function_response = call_function(
                function_name=function_name,
                raw_args=raw_args,
                verbose=args.verbose,
            )

            if "error" in function_response:
                print(function_response["error"])
            else:
                print(function_name)
                if isinstance(raw_args, dict):
                    for value in raw_args.values():
                        print(value)
                print(function_response["result"])

            # One tool message per call with matching tool_call_id
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(function_response),
                }
            )

    print("Error: Reached maximum number of iterations without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()