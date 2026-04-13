# English Text Studio

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
- Hugging Face Router or Gemini
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
DATABASE_URL=
APP_BASE_URL=http://127.0.0.1:8041
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_USE_TLS=true
```

- Leave `DATABASE_URL` empty for local SQLite
- Set `DATABASE_URL` in staging/production for PostgreSQL
- Set SMTP variables to enable email verification links

## Live Test Environment

This repo includes a Render blueprint in [render.yaml](C:\Users\PC\Desktop\proje\render.yaml).

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
