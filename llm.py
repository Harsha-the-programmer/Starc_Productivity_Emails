"""
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def generate_email(prompt: str, temperature: float = 0.4) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "Ollama server not running. Please start Ollama."

    except requests.exceptions.Timeout:
        return "LLM request timed out."

    except Exception as e:
        return f"LLM error: {str(e)}"
"""


import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def generate_email(prompt: str, temperature: float = 0.4) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=250,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Groq LLM error: {str(e)}"
