# app/llm.py
import os, asyncio
from openai import AsyncOpenAI
from openai import APIConnectionError, APIStatusError

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are Vetchat, a compassionate AI companion for U.S. veterans. "
    "Be supportive and practical. If the user may be in crisis, encourage contacting 988 (press 1) "
    "or texting 838255. Do not diagnose."
)

async def chat_once(message: str, crisis: bool = False) -> str:
    if not OPENAI_API_KEY:
        return "LLM not configured: set OPENAI_API_KEY in the server environment."

    # simple retry loop for transient network hiccups
    for attempt in range(3):
        try:
            prefix = "The user may be in crisis. Be extra gentle and brief.\n\n" if crisis else ""
            return await asyncio.wait_for(_call(prefix + message), timeout=25)
        except (APIConnectionError,) as e:
            # network/DNS/TLS hiccup, retry
            if attempt < 2:
                await asyncio.sleep(1.5 * (attempt + 1))
                continue
            print(f"[LLM APIConnectionError] {e!r}")
            return "I’m here with you. I’m having trouble connecting—can we try again in a moment?"
        except APIStatusError as e:
            # e.g., 401/429/5xx from API — log and return safe text
            print(f"[LLM APIStatusError] {e.status_code}: {e!r}")
            return "I ran into an upstream error. Please try again shortly."
        except asyncio.TimeoutError:
            return "I’m here with you. The assistant timed out—can we try again?"
        except Exception as e:
            print(f"[LLM ERROR] {type(e).__name__}: {e}")
            return "I hit an error reaching the assistant—please try again."

async def _call(text: str) -> str:
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.7,
    )
    return (resp.choices[0].message.content or "").strip()
