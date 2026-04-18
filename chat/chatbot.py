from typing import Optional
import requests

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are an AI assistant inside a chat application. "
        "Help users to answer their questions"
        "Be clear, short, and practical."
    )
}

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5-coder:3b"


def get_chatbot_response(user_input: str, summary: Optional[str] = None):

    messages = [SYSTEM_PROMPT]

    if summary:
        messages.append({
            "role": "system",
            "content": f"This is the summary of previous questions asked by user replay based on it  : {summary}"
        })

    messages.append({
        "role": "user",
        "content": user_input
    })

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()["message"]["content"]