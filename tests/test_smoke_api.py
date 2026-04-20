from __future__ import annotations


def register_user(client, username: str = "smoketest", password: str = "secret123"):
    response = client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response


def login_user(client, username: str = "smoketest", password: str = "secret123"):
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response


def test_register_me_and_logout_flow(client):
    response = register_user(client, username="FlowUser")
    body = response.json()

    assert body["user"]["username"] == "flowuser"
    assert body["user"]["email_verified"] is True
    assert "readlex_session" in client.cookies

    me_response = client.get("/api/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["user"]["username"] == "flowuser"

    logout_response = client.post("/api/auth/logout")
    assert logout_response.status_code == 200
    assert logout_response.json()["ok"] is True

    me_after_logout = client.get("/api/auth/me")
    assert me_after_logout.status_code == 200
    assert me_after_logout.json()["user"] is None


def test_legacy_password_login_upgrades_hash(client, app_module):
    legacy_hash = app_module.hash_password_legacy("legacy123")
    app_module.db_insert(
        "INSERT INTO users (username, password_hash, is_active, verified_at, created_at) VALUES (?, ?, ?, ?, ?)",
        ("legacyuser", legacy_hash, 1, app_module.now_iso(), app_module.now_iso()),
    )

    login_response = client.post(
        "/api/auth/login",
        json={"username": "legacyuser", "password": "legacy123"},
    )
    assert login_response.status_code == 200, login_response.text

    row = app_module.db_fetchone(
        "SELECT password_hash FROM users WHERE username = ?",
        ("legacyuser",),
    )
    assert row is not None
    assert str(row["password_hash"]).startswith("$2")
    assert not app_module.is_legacy_password_hash(str(row["password_hash"]))


def test_protected_endpoint_requires_auth(client):
    response = client.get("/api/saved-words")
    assert response.status_code == 401
    assert "giriş" in response.json()["detail"].lower()


def test_library_generate_records_history_for_logged_in_user(client):
    register_user(client, username="readerone")

    generate_response = client.post(
        "/api/generate",
        json={
            "level": "B1",
            "topic": "Random",
            "length_target": 150,
            "keywords": [],
            "source": "library",
        },
    )
    assert generate_response.status_code == 200, generate_response.text
    payload = generate_response.json()
    assert payload["content_source"] == "library"
    assert payload["title"]
    assert payload["text"]

    me_response = client.get("/api/auth/me")
    assert me_response.status_code == 200
    history = me_response.json()["history"]
    assert len(history) == 1

    history_response = client.get(f"/api/history/{history[0]['id']}")
    assert history_response.status_code == 200
    reading = history_response.json()["reading"]
    assert reading["title"] == payload["title"]
    assert reading["content_source"] == "library"


def test_word_detail_saved_words_and_quiz_roundtrip(client):
    register_user(client, username="quizuser")

    generate_response = client.post(
        "/api/generate",
        json={
            "level": "B1",
            "topic": "Random",
            "length_target": 150,
            "keywords": [],
            "source": "library",
        },
    )
    assert generate_response.status_code == 200, generate_response.text
    reading = generate_response.json()
    glossary = reading["glossary"]
    assert glossary

    selected_words = list(glossary.keys())[:4]
    assert len(selected_words) == 4

    for word in selected_words:
        detail_response = client.post(
            "/api/word-detail",
            json={
                "text": reading["text"],
                "word": word,
                "content_source": "library",
            },
        )
        assert detail_response.status_code == 200, detail_response.text
        detail = detail_response.json()
        assert detail["turkish"]
        assert detail["context"]
        assert detail["example"]

    saved_response = client.get("/api/saved-words")
    assert saved_response.status_code == 200
    words = saved_response.json()["words"]
    assert len(words) >= 4

    quiz_response = client.get("/api/quiz/next")
    assert quiz_response.status_code == 200, quiz_response.text
    question = quiz_response.json()["question"]
    assert question is not None

    saved_word = next(item for item in words if int(item["id"]) == int(question["word_id"]))
    expected_answer = question["word"] if question["question_type"] == "blank" else saved_word["turkish"]

    check_response = client.post(
        "/api/quiz/check",
        json={
            "word_id": question["word_id"],
            "answer": expected_answer,
            "question_type": question["question_type"],
        },
    )
    assert check_response.status_code == 200, check_response.text
    result = check_response.json()
    assert result["correct"] is True
    assert result["word"] == question["word"]
