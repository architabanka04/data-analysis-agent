import os

import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-120b"
URL = "https://api.groq.com/openai/v1/chat/completions"


def send_request(prompt):
    reply = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )

    if reply.status_code != 200:
        raise RuntimeError(f"Groq error {reply.status_code}: {reply.text[:200]}")

    text = reply.json()["choices"][0]["message"]["content"] or ""

    if "</think>" in text:
        text = text.split("</think>", 1)[1]

    return text.strip()


if __name__ == "__main__":
    print(send_request("Say hello in one short sentence."))
