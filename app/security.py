
import hashlib
import hmac
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

def hash_user_ref(raw: str) -> str:
    return hmac.new(SECRET_KEY.encode(), raw.encode(), hashlib.sha256).hexdigest()
