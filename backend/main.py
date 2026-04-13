import hashlib
import json
import os
import random
import re
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from fastapi import Cookie, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field
from backend.reading_library import READING_SEEDS, normalize_topic

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # pragma: no cover
    psycopg = None
    dict_row = None


ROOT_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT_DIR / "frontend"
ENV_PATH = ROOT_DIR / ".env"
DB_PATH = ROOT_DIR / "backend" / "app.db"
SESSION_COOKIE = "ets_session"
WORD_DETAIL_CACHE: dict[str, dict[str, str]] = {}
GENERATE_CACHE: dict[str, str] = {}
QUIZ_DISTRACTOR_BANK = {
    "verb": ["kaydetmek", "yorumlamak", "ta??mak", "dengelemek", "kar??la?t?rmak", "geli?tirmek"],
    "adjective": ["d?zenli", "kar???k", "dar", "geni?", "yo?un", "sakin", "net", "karma??k", "yava?", "h?zl?", "g??l?", "zay?f"],
    "noun": ["ama?", "denge", "al??kanl?k", "kan?t", "yolculuk", "odak", "fikir", "yorum", "kavram", "??z?m"],
}
LEVEL_CONFIG = {
    "A1": {"min_words": 60, "max_words": 100, "label": "Ã‡ok temel ve gÃ¼nlÃ¼k"},
    "A2": {"min_words": 90, "max_words": 130, "label": "Basit ve gÃ¼nlÃ¼k"},
    "B1": {"min_words": 120, "max_words": 170, "label": "DoÄŸal ve akÄ±cÄ±"},
    "B2": {"min_words": 150, "max_words": 220, "label": "Daha zengin ama rahat okunur"},
    "C1": {"min_words": 180, "max_words": 260, "label": "Ä°leri, doÄŸal ve detaylÄ±"},
    "Academic": {"min_words": 190, "max_words": 280, "label": "Akademik ve daha analitik"},
}
LOCAL_WORD_MAP = {
    "academic": "akademik",
    "airport": "havaalanÄ±",
    "analysis": "analiz",
    "balance": "denge",
    "busy": "yoÄŸun",
    "bus": "otobÃ¼s",
    "calm": "sakin",
    "challenge": "zorluk",
    "city": "ÅŸehir",
    "coffee": "kahve",
    "collaboration": "iÅŸ birliÄŸi",
    "concept": "kavram",
    "data": "veri",
    "different": "farklÄ±",
    "difficult": "zor",
    "early": "erken",
    "education": "eÄŸitim",
    "email": "e-posta",
    "exam": "sÄ±nav",
    "evidence": "kanÄ±t",
    "flexible": "esnek",
    "friend": "arkadaÅŸ",
    "goal": "hedef",
    "happy": "mutlu",
    "hotel": "otel",
    "important": "Ã¶nemli",
    "late": "geÃ§",
    "library": "kÃ¼tÃ¼phane",
    "life": "hayat",
    "meaningful": "anlamlÄ±",
    "meeting": "toplantÄ±",
    "method": "yÃ¶ntem",
    "morning": "sabah",
    "office": "ofis",
    "plan": "plan",
    "project": "proje",
    "purpose": "amaÃ§",
    "quiet": "sessiz",
    "research": "araÅŸtÄ±rma",
    "result": "sonuÃ§",
    "rewarding": "tatmin edici",
    "school": "okul",
    "simple": "basit",
    "student": "Ã¶ÄŸrenci",
    "study": "Ã§alÄ±ÅŸma",
    "task": "gÃ¶rev",
    "teacher": "Ã¶ÄŸretmen",
    "team": "ekip",
    "theory": "kuram",
    "ticket": "bilet",
    "travel": "seyahat etmek",
    "work": "iÅŸ",
    "workday": "iÅŸ gÃ¼nÃ¼",
}
TOPIC_SENTENCE_BANK = {
    "Serbest": [
        "The day starts quietly, but it soon becomes full of small decisions and new plans.",
        "There is always a balance between routine, personal goals, and unexpected moments.",
        "People often move through the day by solving simple problems and adjusting their plans.",
        "By the evening, even an ordinary day can feel meaningful when it includes progress and connection.",
    ],
    "GÃ¼nlÃ¼k Hayat": [
        "Most days begin with simple habits like breakfast, getting ready, and checking the time.",
        "Daily life feels smoother when familiar routines create a sense of comfort and rhythm.",
        "Small moments, such as talking to someone or taking a short walk, can change the mood of the day.",
        "Even when nothing dramatic happens, ordinary life can still feel full and satisfying.",
    ],
    "Okul": [
        "School life often mixes responsibility, curiosity, and the pressure to stay organized.",
        "Students move between lessons, assignments, and conversations with classmates throughout the day.",
        "A good class can make difficult ideas feel more manageable and interesting.",
        "By the end of the day, school is not only about grades but also about growth and routine.",
    ],
    "Seyahat": [
        "Travel usually brings a mix of excitement, planning, and small surprises.",
        "Moving through a new place makes people notice different sounds, habits, and rhythms.",
        "Even a short trip can create strong memories through simple details and unexpected encounters.",
        "The best part of travel is often the feeling of discovery that stays with you afterwards.",
    ],
    "Ä°ÅŸ HayatÄ±": [
        "Work life is often shaped by planning, communication, and the need to stay flexible.",
        "A normal day can include meetings, messages, and moments that require quick decisions.",
        "Professional life becomes easier when people know how to organize their time and energy.",
        "Even busy schedules feel more manageable when there is a clear goal and steady teamwork.",
    ],
    "Akademik": [
        "Academic work often begins with a question, a method, and a clear reason for exploring the topic.",
        "A careful reading process helps students connect evidence, ideas, and interpretation.",
        "Strong academic writing balances clarity with detail, so each sentence supports the central claim.",
        "In the end, the value of academic practice comes from thoughtful analysis and precise communication.",
    ],
}
TOPIC_SCENARIOS = {
    "Serbest": ["a personal routine", "a small decision", "an ordinary day with meaningful details"],
    "GÃ¼nlÃ¼k Hayat": ["a simple day at home", "a walk through the neighborhood", "a relaxed plan with a friend"],
    "Okul": ["preparing for class", "finishing an assignment", "talking with classmates after a lesson"],
    "Seyahat": ["arriving in a new city", "preparing for a short trip", "moving through an airport or station"],
    "Ä°ÅŸ HayatÄ±": ["handling a busy workday", "preparing for an important meeting", "balancing deadlines and communication"],
    "Akademik": ["preparing a research summary", "analyzing an article for class", "connecting evidence to an academic argument"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_env_file() -> None:
    if not ENV_PATH.exists():
        return
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        cleaned = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), cleaned)


load_env_file()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "hf").strip().lower()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_BASE_URL = os.getenv("HF_BASE_URL", "https://router.huggingface.co/v1").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
USE_POSTGRES = DATABASE_URL.startswith("postgres")


class GenerateRequest(BaseModel):
    level: str
    topic: str
    length_target: int = Field(ge=60, le=320)
    keywords: list[str] = Field(default_factory=list)
    source: str = "library"
    exclude_title: str | None = None


class ExplainRequest(BaseModel):
    text: str
    word: str


class AuthRequest(BaseModel):
    username: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=72)


class QuizAnswerRequest(BaseModel):
    word_id: int
    answer: str
    question_type: str = "meaning"


def build_http_client() -> httpx.Client:
    return httpx.Client(timeout=90.0, trust_env=False)


def build_openai_compatible_client(base_url: str, api_key: str) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=api_key, http_client=build_http_client())


def _pg_query(query: str) -> str:
    return query.replace("?", "%s")


def _row_to_dict(row: Any) -> dict[str, Any] | None:
    if row is None:
        return None
    if isinstance(row, sqlite3.Row):
        return dict(row)
    if isinstance(row, dict):
        return row
    return dict(row)


def _rows_to_dicts(rows: list[Any]) -> list[dict[str, Any]]:
    return [_row_to_dict(row) or {} for row in rows]


def db_fetchone(query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
                return _row_to_dict(cur.fetchone())
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        return _row_to_dict(connection.execute(query, params).fetchone())
    finally:
        connection.close()


def db_fetchall(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
                return _rows_to_dicts(cur.fetchall())
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        return _rows_to_dicts(connection.execute(query, params).fetchall())
    finally:
        connection.close()


def db_execute(query: str, params: tuple[Any, ...] = ()) -> None:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
            conn.commit()
        return
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute(query, params)
        connection.commit()
    finally:
        connection.close()


def db_insert(query: str, params: tuple[Any, ...] = ()) -> int:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
                row = cur.fetchone()
            conn.commit()
        return int(row["id"])
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.execute(query, params)
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()


def seed_readings() -> None:
    existing_rows = db_fetchall("SELECT id, title, source FROM readings")
    existing_by_title = {str(row["title"]): row for row in existing_rows}
    seed_titles = {item["title"] for item in READING_SEEDS}

    for row in existing_rows:
        if str(row.get("source")) == "manual" and str(row["title"]) not in seed_titles:
            db_execute("DELETE FROM readings WHERE id = ?", (row["id"],))

    for item in READING_SEEDS:
        payload = (
            item["title"],
            item["text"],
            item["level"],
            item["topic"],
            json.dumps(item["keywords"], ensure_ascii=False),
            len(item["text"].split()),
            "manual",
            1,
        )
        existing = existing_by_title.get(item["title"])
        if existing:
            db_execute(
                """
                UPDATE readings
                SET title = ?, text = ?, level = ?, topic = ?, keywords = ?,
                    word_count = ?, source = ?, is_published = ?
                WHERE id = ?
                """,
                payload + (existing["id"],),
            )
            continue

        insert_query = (
            "INSERT INTO readings (title, text, level, topic, keywords, word_count, source, is_published) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        if USE_POSTGRES:
            insert_query += " RETURNING id"
        db_insert(insert_query, payload)


def init_db() -> None:
    schema_sqlite = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS saved_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            source_text TEXT NOT NULL,
            turkish TEXT NOT NULL,
            context TEXT NOT NULL,
            example TEXT NOT NULL,
            click_count INTEGER NOT NULL DEFAULT 1,
            last_result TEXT NOT NULL DEFAULT 'new',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, word),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            level TEXT NOT NULL,
            topic TEXT NOT NULL,
            keywords TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            source TEXT NOT NULL DEFAULT 'manual',
            is_published INTEGER NOT NULL DEFAULT 1
        );
    """
    schema_postgres = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS saved_words (
            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            word TEXT NOT NULL,
            source_text TEXT NOT NULL,
            turkish TEXT NOT NULL,
            context TEXT NOT NULL,
            example TEXT NOT NULL,
            click_count INTEGER NOT NULL DEFAULT 1,
            last_result TEXT NOT NULL DEFAULT 'new',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, word)
        );
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            level TEXT NOT NULL,
            topic TEXT NOT NULL,
            keywords TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            source TEXT NOT NULL DEFAULT 'manual',
            is_published INTEGER NOT NULL DEFAULT 1
        );
    """
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(schema_postgres)
            conn.commit()
        return
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.executescript(schema_sqlite)
        connection.commit()
    finally:
        connection.close()


init_db()
seed_readings()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def clean_username(username: str) -> str:
    cleaned = username.strip().lower()
    if not re.fullmatch(r"^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$", cleaned):
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")
    return cleaned


def user_payload(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if not row:
        return None
    return {"id": row["id"], "username": row["username"], "created_at": row["created_at"]}


def require_user(session_token: str | None) -> dict[str, Any]:
    if not session_token:
        raise HTTPException(status_code=401, detail="Ã–nce giriÅŸ yapmalÄ±sÄ±n.")
    row = db_fetchone(
        """
        SELECT users.id, users.username, users.created_at
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.token = ?
        """,
        (session_token,),
    )
    if not row:
        raise HTTPException(status_code=401, detail="Oturum bulunamadÄ±. Tekrar giriÅŸ yap.")
    return user_payload(row) or {}


def optional_user(session_token: str | None) -> dict[str, Any] | None:
    if not session_token:
        return None
    try:
        return require_user(session_token)
    except HTTPException:
        return None


def create_session(response: Response, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    db_execute(
        "INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)",
        (token, user_id, now_iso()),
    )
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24 * 30,
    )
    return token


def clear_session(response: Response, session_token: str | None) -> None:
    if session_token:
        db_execute("DELETE FROM sessions WHERE token = ?", (session_token,))
    response.delete_cookie(SESSION_COOKIE)


def build_user_stats(user_id: int) -> dict[str, int]:
    row = db_fetchone(
        """
        SELECT COUNT(*) AS saved_words,
               SUM(CASE WHEN last_result = 'correct' THEN 1 ELSE 0 END) AS mastered_words
        FROM saved_words
        WHERE user_id = ?
        """,
        (user_id,),
    ) or {"saved_words": 0, "mastered_words": 0}
    return {
        "saved_words": int(row["saved_words"] or 0),
        "mastered_words": int(row["mastered_words"] or 0),
    }


def save_word_for_user(user_id: int, word: str, text: str, detail: dict[str, str]) -> None:
    timestamp = now_iso()
    existing = db_fetchone(
        "SELECT id, click_count FROM saved_words WHERE user_id = ? AND word = ?",
        (user_id, word.lower()),
    )
    if existing:
        db_execute(
            """
            UPDATE saved_words
            SET source_text = ?, turkish = ?, context = ?, example = ?,
                click_count = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                text,
                detail["turkish"],
                detail["context"],
                detail["example"],
                int(existing["click_count"]) + 1,
                timestamp,
                existing["id"],
            ),
        )
    else:
        db_execute(
            """
            INSERT INTO saved_words (
                user_id, word, source_text, turkish, context, example,
                click_count, last_result, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 1, 'new', ?, ?)
            """,
            (
                user_id,
                word.lower(),
                text,
                detail["turkish"],
                detail["context"],
                detail["example"],
                timestamp,
                timestamp,
            ),
          )


def detail_is_saveable(word: str, detail: dict[str, str]) -> bool:
    turkish = (detail.get("turkish") or "").strip()
    if not turkish:
        return False
    lowered = turkish.lower()
    if "alÄ±namadÄ±" in lowered or "bulunamadÄ±" in lowered:
        return False
    if lowered == word.strip().lower():
        return False
    return True


def classify_turkish_meaning(value: str) -> str:
    lowered = value.strip().lower()
    if lowered.endswith(("mek", "mak")):
        return "verb"
    if lowered.endswith(("yor", "?yor", "iyor", "uyor", "?yor", "ilir", "?l?r", "ulur", "?l?r", "lan?r", "lenir")):
        return "verb"
    if lowered.endswith(("li", "l?", "lu", "l?", "siz", "s?z", "suz", "s?z", "sel", "sal")):
        return "adjective"
    if lowered.endswith(("ik", "?k", "uk", "?k")):
        return "adjective"
    return "noun"


def quiz_candidate_meanings(words: list[dict[str, Any]], target_id: int, target_turkish: str) -> list[str]:
    values: list[str] = []
    target_kind = classify_turkish_meaning(target_turkish)
    for row in words:
        if int(row["id"]) == int(target_id):
            continue
        candidate = str(row.get("turkish") or "").strip().lower()
        if not candidate:
            continue
        if any(mark in candidate for mark in ["al?namad?", "bulunamad?", "not available"]):
            continue
        if len(candidate) < 2:
            continue
        if classify_turkish_meaning(candidate) != target_kind:
            continue
        if candidate not in values:
            values.append(candidate)
    for fallback in QUIZ_DISTRACTOR_BANK[target_kind]:
        if fallback != target_turkish.strip().lower() and fallback not in values:
            values.append(fallback)
    return values


def get_recent_words(user_id: int, limit: int = 6) -> list[dict[str, Any]]:
    return db_fetchall(
        """
        SELECT id, word, turkish, click_count, last_result, updated_at
        FROM saved_words
        WHERE user_id = ?
        ORDER BY updated_at DESC
        LIMIT ?
        """,
        (user_id, limit),
    )


def build_quiz_question(user_id: int, exclude_word_id: int | None = None) -> dict[str, Any] | None:
    words = db_fetchall(
        """
        SELECT id, word, turkish, context, example, click_count, last_result
        FROM saved_words
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,),
    )
    if len(words) < 4:
        return None
    if exclude_word_id is not None:
        alternate_words = [row for row in words if int(row["id"]) != int(exclude_word_id)]
        if len(alternate_words) >= 4:
            words = alternate_words
    target = sorted(
        words,
        key=lambda row: (row["last_result"] == "correct", row["click_count"], row["id"]),
    )[0]
    translation_distractors = quiz_candidate_meanings(words, int(target["id"]), str(target["turkish"]))[:3]
    translation_options = list(dict.fromkeys(translation_distractors + [str(target["turkish"]).strip().lower()]))
    while len(translation_options) < 4:
        for fallback in quiz_candidate_meanings(words, int(target["id"]), str(target["turkish"])):
            if fallback not in translation_options:
                translation_options.append(fallback)
            if len(translation_options) == 4:
                break

    example_text = str(target["example"] or "").strip()
    can_make_blank = bool(example_text) and re.search(rf"\b{re.escape(str(target['word']))}\b", example_text, flags=re.IGNORECASE)
    if can_make_blank and random.random() < 0.5:
        blank_sentence = re.sub(
            rf"\b{re.escape(str(target['word']))}\b",
            "_____",
            example_text,
            count=1,
            flags=re.IGNORECASE,
        )
        word_distractors = [row["word"] for row in words if row["id"] != target["id"]][:3]
        word_options = list(dict.fromkeys(word_distractors + [target["word"]]))
        while len(word_options) < 4:
            for fallback in ["result", "habit", "travel", "focus"]:
                if fallback not in word_options:
                    word_options.append(fallback)
                if len(word_options) == 4:
                    break
        random.shuffle(word_options)
        return {
            "word_id": target["id"],
            "question_type": "blank",
            "question": "Which word best completes the sentence?",
            "sentence": blank_sentence,
            "word": target["word"],
            "options": word_options[:4],
            "answer": target["word"],
            "context": target["context"],
            "example": target["example"],
        }

    random.shuffle(translation_options)
    return {
        "word_id": target["id"],
        "question_type": "meaning",
        "question": f'What is the best Turkish meaning of "{target["word"]}"?',
        "word": target["word"],
        "options": translation_options[:4],
        "answer": target["turkish"],
        "context": target["context"],
        "example": target["example"],
    }


def sanitize_keywords(raw_keywords: list[str]) -> list[str]:
    seen, result = set(), []
    for item in raw_keywords:
        cleaned = item.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered not in seen:
            seen.add(lowered)
            result.append(cleaned)
    return result


def sanitize_word(word: str) -> str:
    return re.sub(r"[^A-Za-z -]", "", word).strip()


def parse_keywords_field(value: str) -> list[str]:
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in value.split(",") if item.strip()]


def pick_library_reading(
    level: str,
    topic: str,
    keywords: list[str],
    length_target: int,
    exclude_title: str | None = None,
) -> dict[str, Any] | None:
    normalized_topic = normalize_topic(topic)
    rows = db_fetchall(
        """
        SELECT id, title, text, level, topic, keywords, word_count, source
        FROM readings
        WHERE is_published = 1 AND level = ?
        ORDER BY id
        """,
        (level,),
    )
    if not rows:
        return None
    if exclude_title:
        alternate_rows = [row for row in rows if str(row["title"]) != exclude_title]
        if alternate_rows:
            rows = alternate_rows
    if normalized_topic != "Serbest":
        exact_topic_rows = [row for row in rows if row["topic"] == normalized_topic]
        if exact_topic_rows:
            rows = exact_topic_rows
    scored: list[tuple[int, int, dict[str, Any]]] = []
    for row in rows:
        row_keywords = parse_keywords_field(row["keywords"])
        keyword_hits = sum(1 for keyword in keywords if keyword.lower() in {item.lower() for item in row_keywords})
        topic_score = 2 if row["topic"] == normalized_topic else 0
        length_score = abs(int(row["word_count"]) - int(length_target))
        scored.append((-(keyword_hits + topic_score), length_score, row))
    scored.sort(key=lambda item: (item[0], item[1], item[2]["id"]))
    top_score = scored[0][0]
    candidate_rows = [row for score, _length, row in scored if score == top_score]
    best = random.choice(candidate_rows)
    return {
        "id": best["id"],
        "title": best["title"],
        "text": best["text"],
        "level": best["level"],
        "topic": best["topic"],
        "keywords": parse_keywords_field(best["keywords"]),
        "word_count": best["word_count"],
        "source": best["source"],
    }


def build_text_prompt(level: str, topic: str, keywords: list[str], length_target: int) -> str:
    cfg = LEVEL_CONFIG[level]
    return f"""
Write a natural English reading text for a {level} learner.

Topic:
{topic}

Use these keywords naturally:
{", ".join(keywords)}

Rules:
- Write only one paragraph
- Keep the text clear, natural, and realistic
- Do not force the keywords
- Target length: around {length_target} words
- Stay between {cfg["min_words"]} and {cfg["max_words"]} words
- Aim for at least {cfg["min_words"]} words before stopping
- Do not use markdown, bullet points, bold markers, or headings
- Do not wrap any word with symbols such as ** or quotes for emphasis
- Give only the reading text
""".strip()


def build_plan_prompt(level: str, topic: str, keywords: list[str], length_target: int) -> str:
    cfg = LEVEL_CONFIG[level]
    return f"""
Create a short writing plan for an English reading text.

Topic: {topic}
Level: {level}
Keywords: {", ".join(keywords)}
Target length: {length_target} words

Return valid JSON only:
{{
  "scenario": "one short realistic scenario",
  "voice": "short style note",
  "beats": ["beat 1", "beat 2", "beat 3", "beat 4"]
}}

Rules:
- Scenario must be realistic and simple
- Beats should describe the paragraph flow
- Keep everything short
- No markdown
- No extra text
- The final writing should fit between {cfg["min_words"]} and {cfg["max_words"]} words
""".strip()


def build_text_from_plan_prompt(level: str, topic: str, keywords: list[str], length_target: int, plan: dict[str, Any]) -> str:
    cfg = LEVEL_CONFIG[level]
    beats = "\n".join(f"- {beat}" for beat in plan.get("beats", [])[:4])
    return f"""
Write a natural English reading text for a {level} learner.

Topic:
{topic}

Scenario:
{plan.get("scenario", topic)}

Voice:
{plan.get("voice", "clear and natural")}

Flow:
{beats}

Use these keywords naturally:
{", ".join(keywords)}

Rules:
- Write only one paragraph
- Keep the text clear, natural, and realistic
- Do not force the keywords
- Target length: around {length_target} words
- Stay between {cfg["min_words"]} and {cfg["max_words"]} words
- Do not use markdown, bullet points, bold markers, or headings
- Give only the reading text
""".strip()


def build_word_prompt(text: str, word: str) -> str:
    return f"""
The learner is reading this English text:

\"\"\"{text}\"\"\"

Explain this word in Turkish: "{word}"

Rules:
- First line: Turkish meaning
- Second line: meaning in the context of the text
- Third line: one short and simple English example sentence
- Keep it short and clear
""".strip()


def build_word_strict_prompt(text: str, word: str) -> str:
    return f"""
The learner is reading this English text:

\"\"\"{text}\"\"\"

Target word: "{word}"

Return valid JSON only:
{{
  "turkish": "...",
  "context": "...",
  "example": "..."
}}

Rules:
- The "turkish" value must be a natural Turkish meaning for this English word
- The "context" value must explain the meaning inside this text in Turkish
- The "example" value must be one short English sentence using the same word naturally
- Never leave any field empty
- No markdown
- No extra text
""".strip()


def extract_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        texts = [part.get("text", "") for part in parts if part.get("text")]
        if texts:
            return "\n".join(texts).strip()
    return ""


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", text))


def clean_generated_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"[*_#`]+", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def parse_json_response(raw_text: str) -> dict[str, Any]:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = cleaned[start : end + 1]
            candidate = re.sub(r",(\s*[}\]])", r"\1", candidate)
            try:
                data = json.loads(candidate)
                return data if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}


def infer_turkish_meaning(word: str) -> str:
    lowered = word.lower().strip()
    if lowered in LOCAL_WORD_MAP:
        return LOCAL_WORD_MAP[lowered]
    if lowered.endswith("ing") and len(lowered) > 4:
        return f"{lowered[:-3]} yapmak"
    if lowered.endswith("ed") and len(lowered) > 3:
        return lowered[:-2]
    return lowered


def choose_local_scenario(topic: str, keywords: list[str]) -> dict[str, Any]:
    topic_key = topic if topic in TOPIC_SCENARIOS else "Serbest"
    scenario_seed = TOPIC_SCENARIOS[topic_key][len(keywords) % len(TOPIC_SCENARIOS[topic_key])]
    return {
        "scenario": scenario_seed,
        "voice": "clear, natural, and realistic",
        "beats": [
            "open with a clear everyday situation",
            "introduce a practical action or responsibility",
            "connect the keywords through a natural flow",
            "end with a small reflection or outcome",
        ],
    }


def build_local_word_detail(text: str, word: str) -> dict[str, str]:
    meaning = infer_turkish_meaning(word)
    context = f'"{word}" bu metinde "{meaning}" anlamÄ±na yakÄ±n ÅŸekilde kullanÄ±lÄ±yor.'
    example = f"I use the word {word} in a simple sentence."
    if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE):
        example = f"The word {word} appears in this reading text."
    return {"turkish": meaning, "context": context, "example": example}


def should_use_local_meaning(word: str, candidate: str) -> bool:
    cleaned = candidate.strip().lower()
    lowered_word = word.strip().lower()
    return not cleaned or cleaned == lowered_word or cleaned.startswith(lowered_word + " ")


def build_local_reading(level: str, topic: str, keywords: list[str], length_target: int) -> str:
    topic_key = topic if topic in TOPIC_SENTENCE_BANK else "Serbest"
    base_sentences = TOPIC_SENTENCE_BANK[topic_key][:]
    keyword_sentences = []
    for index, keyword in enumerate(keywords):
        if index == 0:
            keyword_sentences.append(f"In this text, {keyword} becomes one of the key details that shapes the situation.")
        elif index == 1:
            keyword_sentences.append(f"As the paragraph develops, {keyword} fits naturally into the flow of the day.")
        elif index == 2:
            keyword_sentences.append(f"Later, {keyword} helps the reader understand the goal or challenge more clearly.")
        else:
            keyword_sentences.append(f"In a realistic way, {keyword} supports the main idea without feeling forced.")
    level_sentences = {
        "A1": [
            "The ideas stay short, direct, and very easy to follow.",
            "Each sentence gives one clear piece of information.",
        ],
        "A2": [
            "The situation is simple, clear, and easy to follow.",
            "Each step connects to the next part of the day in a natural way.",
        ],
        "B1": [
            "The situation develops gradually, and each detail supports the main idea.",
            "As the day moves forward, the person becomes more aware of what matters most.",
        ],
        "B2": [
            "Because of this, the person has to think carefully, stay calm, and adapt to changing priorities.",
            "This creates a realistic picture of how everyday choices, communication, and timing shape the final outcome.",
        ],
        "C1": [
            "As the situation grows more complex, the text highlights subtle motivations, decisions, and consequences.",
            "This makes the reading feel more layered while still staying coherent and accessible.",
        ],
        "Academic": [
            "From an academic perspective, the paragraph also draws attention to evidence, structure, and interpretation.",
            "The tone remains analytical, so the reader can follow both the example and the broader idea behind it.",
        ],
    }
    sentences = base_sentences + keyword_sentences + level_sentences[level]
    paragraph = " ".join(sentences)
    filler_pool = base_sentences + level_sentences[level]
    filler_index = 0
    target_ceiling = min(length_target, LEVEL_CONFIG[level]["max_words"])
    while count_words(paragraph) < target_ceiling:
        paragraph += " " + filler_pool[filler_index % len(filler_pool)]
        filler_index += 1
        if count_words(paragraph) >= target_ceiling:
            break
    trimmed = " ".join(paragraph.split()[:target_ceiling])
    return clean_generated_text(trimmed)


def validate_text_quality(text: str, level: str, keywords: list[str]) -> tuple[bool, dict[str, Any]]:
    word_count = count_words(text)
    cfg = LEVEL_CONFIG[level]
    keyword_hits = [keyword.lower() in text.lower() for keyword in keywords]
    metrics = {
        "word_count": word_count,
        "length_ok": cfg["min_words"] <= word_count <= cfg["max_words"],
        "keyword_ok": all(keyword_hits),
        "has_markdown": bool(re.search(r"[*_#`]", text)),
    }
    is_valid = bool(metrics["length_ok"] and metrics["keyword_ok"] and not metrics["has_markdown"])
    return is_valid, metrics


def ensure_provider_ready() -> None:
    if MODEL_PROVIDER == "gemini":
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY bulunamadÄ±.")
        return
    if MODEL_PROVIDER == "hf":
        if not HF_TOKEN:
            raise HTTPException(status_code=500, detail="HF_TOKEN bulunamadÄ±.")
        return
    raise HTTPException(status_code=500, detail=f"Desteklenmeyen provider: {MODEL_PROVIDER}")


def request_gemini(prompt: str, system_instruction: str, *, temperature: float, max_output_tokens: int, json_mode: bool = False) -> str:
    payload: dict[str, Any] = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }
    if json_mode:
        payload["generationConfig"]["responseMimeType"] = "application/json"
    with build_http_client() as client:
        response = client.post(
            GEMINI_API_URL,
            headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
    text = extract_text(data)
    if not text:
        raise RuntimeError("Gemini boÅŸ yanÄ±t dÃ¶ndÃ¼.")
    return text


def request_hf(prompt: str, system_instruction: str, *, temperature: float, max_output_tokens: int) -> str:
    client = build_openai_compatible_client(HF_BASE_URL, HF_TOKEN)
    response = client.chat.completions.create(
        model=HF_MODEL,
        messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_output_tokens,
    )
    text = response.choices[0].message.content or ""
    cleaned = text.strip()
    if not cleaned:
        raise RuntimeError("HF Router boÅŸ yanÄ±t dÃ¶ndÃ¼.")
    return cleaned


def request_model(prompt: str, system_instruction: str, *, temperature: float, max_output_tokens: int, json_mode: bool = False) -> str:
    ensure_provider_ready()
    if MODEL_PROVIDER == "hf":
        return request_hf(prompt, system_instruction, temperature=temperature, max_output_tokens=max_output_tokens)
    return request_gemini(
        prompt,
        system_instruction,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        json_mode=json_mode,
    )


def request_text(prompt: str, level: str, topic: str, keywords: list[str]) -> str:
    cache_key = hashlib.sha1(
        json.dumps(
            {"level": level, "topic": topic, "keywords": keywords, "prompt": prompt, "provider": MODEL_PROVIDER},
            ensure_ascii=True,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    cached = GENERATE_CACHE.get(cache_key)
    if cached:
        return cached
    system_instruction = (
        "You are a premium English learning assistant. "
        "Write concise, natural reading passages and follow the requested format exactly."
    )
    min_words = LEVEL_CONFIG[level]["min_words"]
    plan = choose_local_scenario(topic, keywords)
    try:
        raw_plan = request_model(
            build_plan_prompt(level, topic, keywords, LEVEL_CONFIG[level]["max_words"]),
            "You are an expert educational content planner. Return compact JSON only.",
            temperature=0.25,
            max_output_tokens=220,
            json_mode=True,
        )
        parsed_plan = parse_json_response(raw_plan)
        if parsed_plan:
            plan = {
                "scenario": parsed_plan.get("scenario") or plan["scenario"],
                "voice": parsed_plan.get("voice") or plan["voice"],
                "beats": parsed_plan.get("beats") or plan["beats"],
            }
    except Exception:
        pass
    try:
        text = request_model(
            build_text_from_plan_prompt(level, topic, keywords, LEVEL_CONFIG[level]["max_words"], plan),
            system_instruction,
            temperature=0.6,
            max_output_tokens=min(620, LEVEL_CONFIG[level]["max_words"] * 3),
        )
        text = clean_generated_text(text)
    except Exception:
        text = ""
    is_valid, _ = validate_text_quality(text, level, keywords) if text else (False, {})
    if not is_valid and text:
        repaired = clean_generated_text(f"{text} {' '.join(keywords)}")
        repaired_ok, _ = validate_text_quality(repaired, level, keywords)
        text = repaired if repaired_ok else text
    if count_words(text) < max(60, min_words // 2):
        text = build_local_reading(level, topic, keywords, LEVEL_CONFIG[level]["max_words"])
    GENERATE_CACHE[cache_key] = text
    return text


def request_manual_explanation(text: str, word: str) -> str:
    return request_model(
        build_word_prompt(text, word),
        "You are a concise English vocabulary tutor.",
        temperature=0.25,
        max_output_tokens=140,
    )


def request_word_detail(text: str, word: str) -> dict[str, str]:
    cache_key = f"{hashlib.sha1(text.encode('utf-8')).hexdigest()}::{word.lower()}::{MODEL_PROVIDER}"
    cached = WORD_DETAIL_CACHE.get(cache_key)
    if cached:
        return cached
    try:
        raw = request_model(
            build_word_strict_prompt(text, word),
            "You are a bilingual vocabulary tutor. Return compact and correct JSON.",
            temperature=0.2,
            max_output_tokens=180,
            json_mode=True,
        )
        parsed = parse_json_response(raw)
    except Exception:
        parsed = {}
    local_fallback = build_local_word_detail(text, word)
    parsed_meaning = str(parsed.get("turkish", "")).strip()
    result = {
        "turkish": local_fallback["turkish"] if should_use_local_meaning(word, parsed_meaning) else parsed_meaning,
        "context": str(parsed.get("context", "")).strip() or local_fallback["context"],
        "example": str(parsed.get("example", "")).strip() or local_fallback["example"],
    }
    WORD_DETAIL_CACHE[cache_key] = result
    return result


def normalize_api_error(exc: Exception) -> HTTPException:
    if isinstance(exc, HTTPException):
        return exc
    raw = str(exc).strip() or "Unknown API error"
    lowered = raw.lower()
    if "api key" in lowered or "permission" in lowered or "unauthorized" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=401, detail="HF token geÃ§ersiz veya yetkisiz.")
        return HTTPException(status_code=401, detail="Gemini API key geÃ§ersiz veya yetkisiz.")
    if "429" in lowered or "quota" in lowered or "rate limit" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=429, detail="HF Ã¼cretsiz limitine ulaÅŸÄ±ldÄ±.")
        return HTTPException(status_code=429, detail="Gemini free tier limiti aÅŸÄ±ldÄ±.")
    if "403" in lowered:
        return HTTPException(status_code=403, detail="SeÃ§ili saÄŸlayÄ±cÄ± bu isteÄŸe izin vermedi.")
    if "404" in lowered:
        return HTTPException(status_code=404, detail="SeÃ§ili model bulunamadÄ±.")
    if "503" in lowered or "connection" in lowered or "timed out" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=503, detail="HF Router servisine ÅŸu anda ulaÅŸÄ±lamÄ±yor.")
        return HTTPException(status_code=503, detail="Gemini servisine ÅŸu anda ulaÅŸÄ±lamÄ±yor.")
    return HTTPException(status_code=500, detail=raw)


app = FastAPI(title="English Text Studio")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health(session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    active_model = HF_MODEL if MODEL_PROVIDER == "hf" else GEMINI_MODEL
    configured = bool(HF_TOKEN) if MODEL_PROVIDER == "hf" else bool(GEMINI_API_KEY)
    user = optional_user(session_token)
    return {
        "status": "ok",
        "provider": MODEL_PROVIDER,
        "model": active_model,
        "configured": configured,
        "levels": list(LEVEL_CONFIG.keys()),
        "user": user,
    }


@app.post("/api/auth/register")
def register(payload: AuthRequest, response: Response) -> dict[str, Any]:
    username = clean_username(payload.username)
    password_hash = hash_password(payload.password)
    timestamp = now_iso()
    try:
        insert_query = "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)"
        if USE_POSTGRES:
            insert_query += " RETURNING id"
        user_id = db_insert(insert_query, (username, password_hash, timestamp))
    except Exception as exc:
        if "unique" not in str(exc).lower() and "duplicate" not in str(exc).lower():
            raise
        raise HTTPException(status_code=409, detail="This email is already in use.")
    create_session(response, user_id)
    return {"user": {"id": user_id, "username": username, "created_at": timestamp}, "stats": build_user_stats(user_id)}


@app.post("/api/auth/login")
def login(payload: AuthRequest, response: Response) -> dict[str, Any]:
    username = clean_username(payload.username)
    password_hash = hash_password(payload.password)
    row = db_fetchone(
        "SELECT id, username, created_at FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash),
    )
    if not row:
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    create_session(response, int(row["id"]))
    return {"user": user_payload(row), "stats": build_user_stats(int(row["id"]))}


@app.post("/api/auth/logout")
def logout(response: Response, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, bool]:
    clear_session(response, session_token)
    return {"ok": True}


@app.get("/api/auth/me")
def me(session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    user = optional_user(session_token)
    if not user:
        return {"user": None, "stats": {"saved_words": 0, "mastered_words": 0}, "recent_words": []}
    return {
        "user": user,
        "stats": build_user_stats(int(user["id"])),
        "recent_words": get_recent_words(int(user["id"])),
    }


@app.get("/api/quiz/next")
def quiz_next(
    exclude_word_id: int | None = Query(default=None),
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    question = build_quiz_question(int(user["id"]), exclude_word_id)
    if not question:
        return {"question": None, "min_words_needed": 4}
    return {"question": {key: value for key, value in question.items() if key != "answer"}}


@app.post("/api/saved-words/clear")
def clear_saved_words(session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    user = require_user(session_token)
    db_execute("DELETE FROM saved_words WHERE user_id = ?", (int(user["id"]),))
    return {"ok": True, "stats": build_user_stats(int(user["id"]))}


@app.post("/api/quiz/check")
def quiz_check(payload: QuizAnswerRequest, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    user = require_user(session_token)
    row = db_fetchone(
        "SELECT id, word, turkish, context, example FROM saved_words WHERE id = ? AND user_id = ?",
        (payload.word_id, int(user["id"])),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Quiz kelimesi bulunamadÄ±.")
    expected_answer = row["word"] if payload.question_type == "blank" else row["turkish"]
    is_correct = payload.answer.strip().lower() == expected_answer.strip().lower()
    db_execute(
        "UPDATE saved_words SET last_result = ?, updated_at = ? WHERE id = ?",
        ("correct" if is_correct else "wrong", now_iso(), row["id"]),
    )
    return {
        "correct": is_correct,
        "answer": expected_answer,
        "word": row["word"],
        "question_type": payload.question_type,
        "context": row["context"],
        "example": row["example"],
        "stats": build_user_stats(int(user["id"])),
    }


@app.post("/api/generate")
def generate(payload: GenerateRequest) -> dict[str, str]:
    keywords = sanitize_keywords(payload.keywords)
    if payload.level not in LEVEL_CONFIG:
        raise HTTPException(status_code=400, detail="GeÃ§ersiz seviye.")
    if payload.source not in {"library", "ai"}:
        raise HTTPException(status_code=400, detail="GeÃ§ersiz iÃ§erik kaynaÄŸÄ±.")
    if payload.source == "ai" and (len(keywords) < 2 or len(keywords) > 12):
        raise HTTPException(status_code=400, detail="2 ile 12 arasÄ±nda anahtar kelime gerekli.")
    if payload.source == "library":
        library_match = pick_library_reading(
            payload.level,
            payload.topic,
            keywords,
            payload.length_target,
            payload.exclude_title,
        )
        if library_match:
            return {
                "text": library_match["text"],
                "title": library_match["title"],
                "content_source": "library",
            }
        raise HTTPException(status_code=404, detail="Bu filtreler iÃ§in library iÃ§inde uygun bir metin bulunamadÄ±.")
    prompt = build_text_prompt(payload.level, payload.topic, keywords, payload.length_target)
    try:
        return {
            "text": request_text(prompt, payload.level, payload.topic, keywords),
            "title": "",
            "content_source": "ai",
        }
    except Exception as exc:
        raise normalize_api_error(exc)


@app.get("/api/library/readings")
def list_library_readings(level: str | None = None, topic: str | None = None) -> dict[str, Any]:
    query = """
        SELECT id, title, level, topic, keywords, word_count, source
        FROM readings
        WHERE is_published = 1
    """
    params: list[Any] = []
    if level:
        query += " AND level = ?"
        params.append(level)
    if topic:
        query += " AND topic = ?"
        params.append(normalize_topic(topic))
    query += " ORDER BY level, topic, id"
    rows = db_fetchall(query, tuple(params))
    for row in rows:
        row["keywords"] = parse_keywords_field(row["keywords"])
    return {"readings": rows}


@app.get("/api/library/stats")
def library_stats() -> dict[str, Any]:
    total_row = db_fetchone("SELECT COUNT(*) AS total FROM readings WHERE is_published = 1")
    level_rows = db_fetchall(
        """
        SELECT level, COUNT(*) AS total
        FROM readings
        WHERE is_published = 1
        GROUP BY level
        ORDER BY level
        """
    )
    topic_rows = db_fetchall(
        """
        SELECT topic, COUNT(*) AS total
        FROM readings
        WHERE is_published = 1
        GROUP BY topic
        ORDER BY topic
        """
    )
    return {
        "total": int((total_row or {}).get("total", 0)),
        "by_level": level_rows,
        "by_topic": topic_rows,
    }


@app.post("/api/explain")
def explain(payload: ExplainRequest) -> dict[str, str]:
    safe_word = sanitize_word(payload.word)
    if not safe_word:
        raise HTTPException(status_code=400, detail="GeÃ§erli bir kelime gerekli.")
    try:
        return {"explanation": request_manual_explanation(payload.text, safe_word)}
    except Exception as exc:
        raise normalize_api_error(exc)


@app.post("/api/word-detail")
def word_detail(payload: ExplainRequest, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, str]:
    safe_word = sanitize_word(payload.word)
    if not safe_word:
        raise HTTPException(status_code=400, detail="GeÃ§erli bir kelime gerekli.")
    try:
        detail = request_word_detail(payload.text, safe_word)
        user = optional_user(session_token)
        if user and detail_is_saveable(safe_word, detail):
            save_word_for_user(int(user["id"]), safe_word, payload.text, detail)
        return detail
    except Exception as exc:
        raise normalize_api_error(exc)

