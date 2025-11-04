
import re

CRISIS_PATTERNS = [
    r"\bkill myself\b", r"\bsuicide\b", r"\bend my life\b", r"\bwant to die\b",
    r"\bno reason to live\b", r"\bhang myself\b", r"\bshoot myself\b"
]
IMMEDIACY = r"\b(right now|tonight|cant'? go on|immediate|now)\b"

def is_crisis(text: str) -> bool:
    t = text.lower()
    kw = any(re.search(p, t) for p in CRISIS_PATTERNS)
    return kw or bool(re.search(IMMEDIACY, t))
