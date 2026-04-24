# ReadLex

Interactive English reading practice app with:

- account-based sign up / log in
- saved words per user
- quiz questions built from saved words
- topic and level based text generation
- clickable reading text with Turkish meaning cards
- FastAPI backend + custom frontend

## Stack

- FastAPI
- Vanilla HTML/CSS/JS
- Hugging Face Router or Gemini for reading generation
- Google Cloud Translation API for word detail / quick word translation
- SQLite locally
- PostgreSQL in live/staging deploys
- SMTP mail delivery for email verification

## Local Run

1. Create a `.env` file from `.env.example`
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8041
```

4. Open:

```text
http://localhost:8041
```

## Environment Variables

```env
MODEL_PROVIDER=hf
HF_MODEL=Qwen/Qwen2.5-72B-Instruct
HF_TOKEN=your_huggingface_token
GEMINI_MODEL=gemini-2.5-flash
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key
DATABASE_URL=
APP_BASE_URL=http://127.0.0.1:8041
CORS_ALLOWED_ORIGINS=http://127.0.0.1:8041,http://localhost:8041,http://127.0.0.1:8046,http://localhost:8046
COOKIE_SECURE=auto
RESEND_API_KEY=
RESEND_FROM_EMAIL=
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_USE_TLS=true
```

- Leave `DATABASE_URL` empty for local SQLite
- Set `DATABASE_URL` in staging/production for PostgreSQL
- Set `CORS_ALLOWED_ORIGINS` to your exact frontend domains in staging/production
- Leave `COOKIE_SECURE=auto` locally, use `true` in HTTPS production
- Set `GOOGLE_TRANSLATE_API_KEY` to power `word-detail`, quick word help, and translation cards
- Set `RESEND_API_KEY` + `RESEND_FROM_EMAIL` for the easiest email verification setup
- Or set SMTP variables if you want to keep SMTP delivery

## Live Test Environment

This repo includes a Render blueprint in [render.yaml](C:\Users\PC\Desktop\proje\render.yaml).

## Release / Rollback Safety

The 2026-04-25 social panel and recovery UI release is documented in [RELEASE_ROLLBACK_NOTES.md](RELEASE_ROLLBACK_NOTES.md).

- Previous stable main is preserved at commit `d813c85d368423288e72d3253cadaba35e39669c`
- Backup branch: `backup/main-before-social-release-20260425`
- Backup tag: `main-before-social-release-20260425`
- Current release asset version: `20260425social3`
- Current service worker cache: `readlex-shell-v65`

Do not delete the backup branch or tag until this release has been stable in production. If a rollback is needed, follow the notes in `RELEASE_ROLLBACK_NOTES.md` and avoid force-pushing unless it is explicitly approved.

### Render staging flow

1. Push this project to GitHub
2. In Render, create a new Blueprint deploy from the repo
3. Render will create:
   - one web service
   - one PostgreSQL database
4. Add your `HF_TOKEN` in Render environment variables
5. Deploy

After deploy, the app will:

- serve the frontend from the FastAPI backend
- use PostgreSQL through `DATABASE_URL`
- keep saved words and quiz progress in the live environment

## Project Structure

```text
backend/
  main.py
  app.db
frontend/
  index.html
  assets/
    app.js
    styles.css
```

## Notes

- Do not commit your real `.env`
- `.env.example` is safe to share
- Local development uses SQLite automatically
- Live staging uses PostgreSQL automatically when `DATABASE_URL` is set
