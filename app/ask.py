
"""Lecture 1: Ask Gemini questions with optional conversation history."""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def print_tokens(response):
    """Display token usage for an API response."""
    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[tokens] input: {usage.prompt_token_count}, "
            f"output: {usage.candidates_token_count}"
        )


def ask(question: str) -> str:
    """Ask a single independent question."""
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
    )
    print_tokens(response)
    return response.text or ""


def chat() -> None:
    """Maintain conversation history across multiple questions."""
    client = genai.Client(api_key=get_api_key())
    session = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    print("Conversation mode. Type 'exit' to finish.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Conversation ended.")
            break

        if not question:
            continue

        response = session.send_message(question)
        print_tokens(response)
        print(f"\nGemini: {response.text}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask Gemini questions"
    )
    parser.add_argument(
        "question",
        nargs="?",
        default=DEFAULT_QUESTION,
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Enable multi-turn conversation",
    )
    args = parser.parse_args()

    try:
        if args.chat:
            chat()
        else:
            print(f"[model] {MODEL}")
            print(f"[質問] {args.question}\n")
            print(ask(args.question))

    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
