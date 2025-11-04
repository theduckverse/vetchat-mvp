import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def chat_once(message: str, crisis: bool = False):
    crisis_prompt = "The user may be in crisis. Be gentle, empathetic, and suggest professional help.\n\n" if crisis else ""
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Vetchat, a compassionate AI companion for veterans. Be supportive and non-judgmental."},
            {"role": "user", "content": crisis_prompt + message},
        ],
    )
    return response.choices[0].message.content.strip()
