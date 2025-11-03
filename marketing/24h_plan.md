
# 24‑Hour Build & Launch Plan (inspired by Sam Thompson’s public build approach)

**Goal:** ship an SMS‑first MVP in 24 hours, capture real usage, and validate willingness to pay within 7–14 days.

## Hour‑by‑hour (suggested)

**H1–2: Scope + repo**
- Define the one job to be done (non‑clinical SMS companion for Veterans).
- Clone the provided FastAPI SMS scaffold; configure `.env` and Twilio webhook.

**H3–4: Crisis guardrails + prompt**
- Keep the included risk heuristic and system prompt.
- Add footer with 988 (press 1) / text 838255 on crisis triggers.

**H5–6: Landing page + waitlist**
- Deploy `landing/index.html` to Vercel/Netlify.
- CTA: “Text HELLO to +1 (xxx) xxx‑xxxx” and waitlist form that posts to `/waitlist`.

**H7–10: Polish + logs**
- Add Sentry + basic request logging (PII‑free). 
- Create a public “build log” thread (X/LinkedIn), posting progress screenshots.

**H11–14: Organic marketing**
- 3 posts: why this exists; demo GIF; call for early veterans’ feedback.
- DM outreach to 20 community orgs (no PHI).

**H15–18: Paid test (optional)**
- $50–$100 on Meta/Google keywords: “veteran support resources”, “va benefits help” (ensure compliant copy).

**H19–22: Iterate**
- Answer first 20 SMS threads; refine prompt; add quick‑reply macros (copy/paste).

**H23–24: Pricing smoke test**
- Soft paywall after 3 days: $5/mo supporter plan; always free for crisis links.

## Measurement
- Waitlist CTR, SMS starts, % sessions with crisis footer, helpfulness rating.
- Qualitative insights > vanity metrics.

## Ethics
- Non‑clinical; clear disclaimers; never gate crisis resources.
