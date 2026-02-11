import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


SYSTEM_PROMPT = (
    "You are a professional workplace productivity advisor. "
    "Generate concise, executive-level recommendation emails. "
    "Keep the tone professional, constructive, and non-judgmental. "
    "Avoid emojis. Keep length under 200 words."
)


def generate_email(prompt: str, temperature: float = 0.3) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=250,
        )

        content = completion.choices[0].message.content.strip()

        if not content:
            return "Unable to generate recommendation at this time."

        return content

    except Exception:
        return "Unable to generate recommendation at this time."
