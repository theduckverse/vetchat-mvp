
import os
from .prompts import SYSTEM_BASE

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def chat_once(user: str, *, crisis: bool=False) -> str:
    system = SYSTEM_BASE
    if crisis:
        system += ("\nCRISIS MODE: Be extra direct about immediate help. Provide "
                   "Veterans Crisis Line: Dial 988 then press 1; text 838255.")
    # Example using OpenAI's Python SDK (async)
    if OPENAI_API_KEY:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":system},
                {"role":"user","content":user}
            ],
            temperature=0.4
        )
        return resp.choices[0].message.content.strip()
    # Fallback stub (for dev without key)
    return "Thanks for your message. (LLM not configured yet.) If you're in crisis: Dial 988 and press 1, or text 838255."
