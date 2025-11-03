
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .db import get_session

router = APIRouter()

@router.post("/waitlist")
async def waitlist(request: Request, session: AsyncSession = Depends(get_session)):
    form = await request.form()
    email = (form.get("email") or "").strip().lower()
    if not email:
        return {"ok": False}
    # create table if not exists (simple)
    await session.execute(text("""
CREATE TABLE IF NOT EXISTS waitlist (
  email TEXT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  utm_source TEXT,
  utm_medium TEXT,
  utm_campaign TEXT,
  utm_term TEXT,
  utm_content TEXT
)
"""))
    try:
        await session.execute(text("INSERT OR IGNORE INTO waitlist(email, utm_source, utm_medium, utm_campaign, utm_term, utm_content) VALUES (:email,:utm_source,:utm_medium,:utm_campaign,:utm_term,:utm_content)"), {
  "email": email,
  "utm_source": (form.get('utm_source') or '').strip(),
  "utm_medium": (form.get('utm_medium') or '').strip(),
  "utm_campaign": (form.get('utm_campaign') or '').strip(),
  "utm_term": (form.get('utm_term') or '').strip(),
  "utm_content": (form.get('utm_content') or '').strip(),
})
        await session.commit()
    except Exception:
        pass
    # Simple success page
    return {"ok": True, "message": "Thanks! We'll email you when your invite is ready."}
