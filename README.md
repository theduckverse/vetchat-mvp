
# AI for Veterans — Python SMS MVP (FastAPI)

This is a **HIPAA-aligned, crisis-aware** MVP skeleton for an SMS-based assistant that chats with U.S. Veterans.  
Channels: **SMS (Twilio)** and optional **web chat**.

> ⚠️ Important: This assistant is **non-clinical** and **not medical advice**. Always provide crisis resources:
> Veterans Crisis Line — **Dial 988, then press 1**, or **text 838255**.

---

## Quick start

### 1) Prerequisites
- Python 3.10+
- (Optional) Postgres; dev uses SQLite by default.
- (Optional) ngrok for tunneling during local SMS testing.
- A Twilio phone number or Messaging Service (SMS enabled).

### 2) Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # then edit values
```

### 3) Run the API
```bash
uvicorn app.main:app --reload
```
- Local health check: http://127.0.0.1:8000/healthz

### 4) Expose locally (for Twilio)
```bash
ngrok http 8000
```
Copy the HTTPS URL and set it as your **Twilio Inbound Webhook** for SMS (e.g., `https://XYZ.ngrok.io/twilio/inbound`).

### 5) Send a test SMS
Text your Twilio number. The bot replies.  
Try a crisis phrase (e.g., “I want to die”) to see the **crisis footer**.

---

## Project layout

```
ai-vets-mvp-python-sms/
├─ app/
│  ├─ main.py              # FastAPI app entry
│  ├─ chat_routes.py       # /chat web endpoint (optional)
│  ├─ sms_routes.py        # Twilio inbound SMS webhook
│  ├─ llm.py               # LLM wrapper
│  ├─ prompts.py           # System prompt(s)
│  ├─ risk.py              # Simple crisis heuristic
│  ├─ db.py                # DB session/engine
│  ├─ models.py            # SQLAlchemy models
│  ├─ store.py             # Persistence helpers
│  ├─ security.py          # Hashing, phone redaction, etc.
│  └─ deps.py              # Shared dependencies (if needed)
├─ migrations/             # Alembic (optional)
├─ tests/
│  └─ test_smoke.py
├─ requirements.txt
├─ Dockerfile
├─ .env.example
└─ README.md
```

---

## Environment variables

See `.env.example` for a complete list.

- `OPENAI_API_KEY` (or alternative provider keys)
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_MESSAGING_SERVICE_SID`
- `DATABASE_URL` (defaults to SQLite for dev if missing)
- `SECRET_KEY` for hashing IDs (do not commit)

---

## Database

- Default dev DB: `sqlite+aiosqlite:///./local.db`
- Production: Postgres (RDS/Supabase). Run Alembic migrations as needed.

### Schema (minimal)
- `conversations`: channel (`sms`/`web`), `user_ref` (hashed phone or anonymized ID).
- `messages`: `role` (`user|assistant|system`), `content`, `crisis_flag`.
- `feedback`: simple 1–5 rating + comment.

> **Privacy:** Avoid storing raw phone numbers. Use `security.hash_user_ref()` to store a hash instead.

---

## HIPAA-aligned guardrails (pragmatic)
- **Data minimization**: do not request diagnosis/medical histories, SSN, full DOB.
- **Encryption**: TLS in transit; at-rest encryption (DB/volumes). Use field-level encryption for anything sensitive.
- **Access control**: least privilege, MFA for admin endpoints (not in this MVP).
- **Vendor BAAs**: if PHI may be present, execute BAAs (e.g., Twilio, cloud DB). Avoid PHI in SMS if possible.
- **Crisis SOP**: when self-harm risk is detected, provide VCL resources and encourage immediate contact.

---

## Notes on Twilio request validation
We include a lightweight signature validator. For production, prefer Twilio's official helper.
Make sure your webhook URL is **HTTPS** and keep a secret path (e.g. `/twilio/inbound?sig=...`) if desired.

---

## License
For demonstration and evaluation purposes only; no warranty. You are responsible for any regulatory and safety compliance in your deployment.

---

## Deploying the API (Render/Fly/Cloud Run)

- **Render:** Create a new Web Service → Python → set `Start Command`: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **Fly.io:** `fly launch` → expose 8000 → set env from `.env`.
- **Cloud Run:** Build container with the included Dockerfile and deploy.

Expose `/twilio/inbound` via HTTPS and paste that URL into Twilio Messaging webhook.

## Deploying the landing page (Vercel or Netlify)

### Vercel
```bash
cd landing
vercel
```
Accept defaults; the included `vercel.json` makes it static.

### Netlify
Connect repo → set publish directory to `landing/`. The included `netlify.toml` routes SPA to index.html.

---

## Supabase Postgres + Alembic

1. Create a Supabase project → copy the **Connection string (psql)**.
2. Set `DATABASE_URL=postgresql+asyncpg://...` in `.env` (use the **password** variant).
3. Run Alembic:
```bash
alembic upgrade head
```
This creates the `conversations`, `messages`, and `feedback` tables.

---

## Sentry

- Set `SENTRY_DSN` in `.env` (and optional `SENTRY_TRACES`, default 0.1).
- Errors and traces will appear in Sentry automatically.

---

## Metrics endpoint

- `GET /metrics` returns JSON: conversations, messages, and messages flagged crisis.
- Do not expose this publicly in production; protect it behind auth or allowlist.
