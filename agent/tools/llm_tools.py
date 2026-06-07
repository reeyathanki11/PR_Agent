from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

MODEL = os.getenv("GITHUB_MODEL", "gpt-4o-mini")


def ask_llm(prompt: str) -> str:
    """Call LLM and return raw string response."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content


def call_llm(prompt: str) -> dict:
    """
    Call LLM and return a parsed JSON dict.
    All nodes use this function.
    Falls back to empty dict if JSON parsing fails.
    """
    raw = ask_llm(prompt)

    # Strip markdown fences if LLM wraps response in ```json ... ```
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"[LLM] Warning: response was not valid JSON. Raw: {raw[:200]}")
        return {}