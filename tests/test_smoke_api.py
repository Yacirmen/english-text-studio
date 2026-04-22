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


def test_pwa_assets_are_served(client):
    manifest_response = client.get("/manifest.webmanifest")
    assert manifest_response.status_code == 200
    assert manifest_response.headers["content-type"].startswith("application/manifest+json")
    assert manifest_response.json()["short_name"] == "ReadLex"

    service_worker_response = client.get("/sw.js")
    assert service_worker_response.status_code == 200
    assert "READLEX_CACHE" in service_worker_response.text


def test_mobile_origins_are_allowed(app_module):
    assert "capacitor://localhost" in app_module.ALLOWED_ORIGINS
    assert "ionic://localhost" in app_module.ALLOWED_ORIGINS


def test_register_me_and_logout_flow(client):
    response = register_user(client, username="FlowUser")
    body = response.json()

    assert body["user"]["username"] == "flowuser"
    assert body["user"]["email_verified"] is True
    assert body["stats"]["login_streak"] == 1
    assert body["stats"]["fire_level"] == 1
    assert "readlex_session" in client.cookies

    me_response = client.get("/api/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["user"]["username"] == "flowuser"
    assert me_response.json()["stats"]["login_streak"] == 1

    logout_response = client.post("/api/auth/logout")
    assert logout_response.status_code == 200
    assert logout_response.json()["ok"] is True

    me_after_logout = client.get("/api/auth/me")
    assert me_after_logout.status_code == 200
    assert me_after_logout.json()["user"] is None


def test_daily_login_streak_grows_once_per_day(client, app_module):
    register_user(client, username="streaker")
    client.post("/api/auth/logout")

    user = app_module.db_fetchone("SELECT id FROM users WHERE username = ?", ("streaker",))
    yesterday = (app_module.datetime.now().astimezone().date() - app_module.timedelta(days=1)).isoformat()
    app_module.db_execute(
        "UPDATE user_progress SET streak_count = ?, last_streak_date = ?, updated_at = ? WHERE user_id = ?",
        (2, yesterday, app_module.now_iso(), int(user["id"])),
    )

    login_response = login_user(client, username="streaker")
    stats = login_response.json()["stats"]
    assert stats["login_streak"] == 3
    assert stats["fire_level"] == 2
    assert stats["fire_label"] == "Spark"

    me_response = client.get("/api/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["stats"]["login_streak"] == 3


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


def test_ai_generate_falls_back_to_local_text(client, app_module, monkeypatch):
    register_user(client, username="aiuser")

    def fail_model(*args, **kwargs):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(app_module, "request_model", fail_model)
    response = client.post(
        "/api/generate",
        json={
            "level": "B1",
            "topic": "Work Life",
            "length_target": 150,
            "keywords": ["meeting", "project"],
            "source": "ai",
        },
    )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["content_source"] == "ai"
    assert "meeting" in payload["text"].lower()
    assert "project" in payload["text"].lower()


def test_postgres_insert_accepts_non_id_returning_column(app_module, monkeypatch):
    class FakeCursor:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def execute(self, query, params):
            self.query = query
            self.params = params

        def fetchone(self):
            return {"user_id": 42}

    class FakeConnection:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def cursor(self):
            return FakeCursor()

        def commit(self):
            self.committed = True

    class FakePsycopg:
        @staticmethod
        def connect(*args, **kwargs):
            return FakeConnection()

    monkeypatch.setattr(app_module, "USE_POSTGRES", True)
    monkeypatch.setattr(app_module, "psycopg", FakePsycopg)
    monkeypatch.setattr(app_module, "DATABASE_URL", "postgresql://example")

    inserted_id = app_module.db_insert("INSERT INTO user_progress VALUES (?) RETURNING user_id", (42,))

    assert inserted_id == 42


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
    assert question["question_type"] == "meaning"
    assert "sentence" not in question

    saved_word = next(item for item in words if int(item["id"]) == int(question["word_id"]))

    check_response = client.post(
        "/api/quiz/check",
        json={
            "word_id": question["word_id"],
            "answer": saved_word["turkish"],
            "question_type": question["question_type"],
        },
    )
    assert check_response.status_code == 200, check_response.text
    result = check_response.json()
    assert result["correct"] is True
    assert result["word"] == question["word"]


def test_lexical_engine_prefers_phrases_over_split_words(app_module):
    text = (
        "After two weeks, the routine turned out to work well. "
        "Instead of eating fast food, people chose home-cooked meals. "
        "The pilot said take off before the storm arrived."
    )

    glossary = app_module.build_library_glossary(text)

    assert glossary["turned out"]["turkish"] == "sonuçlanmak / ortaya çıkmak"
    assert glossary["turned out"]["kind"] == "phrase"
    assert glossary["turn out"]["surface"] == "turned out"
    assert glossary["home-cooked"]["turkish"] == "ev yapımı"
    assert glossary["take off"]["turkish"] == "havalanmak / hızla yükselmek"
    assert "turned" not in glossary
    assert "out" not in glossary


def test_core_academic_terms_are_stable(app_module):
    text = (
        "Regardless of their employment status, workers need flexibility. "
        "Many employees are deeply concerned about burnout."
    )

    glossary = app_module.build_library_glossary(text)

    assert glossary["regardless of"]["turkish"] == "...den bağımsız olarak / ...e bakılmaksızın"
    assert glossary["regardless of"]["kind"] == "phrase"
    assert "regardless" not in glossary
    assert "of" not in glossary
    assert glossary["flexibility"]["turkish"] == "esneklik"
    assert glossary["deeply"]["turkish"] == "derinden / son derece"


def test_library_word_lookup_skips_suspicious_identity_values(app_module):
    text = (
        "Modern society is often shaped not only by objective realities, "
        "but also by the ways in which those realities are perceived and interpreted."
    )

    assert app_module.build_library_word_detail(text, "Modern")["turkish"] == "çağdaş"
    assert app_module.build_library_word_detail(text, "objective")["turkish"] == "nesnel"
    assert app_module.build_library_word_detail(text, "interpreted")["turkish"] == "yorumlanmış / yorumlanan"


def test_word_detail_resolves_inflected_phrase(client):
    text = "After two weeks, the routine turned out to work well."
    response = client.post(
        "/api/word-detail",
        json={
            "text": text,
            "word": "turned out",
            "content_source": "library",
        },
    )

    assert response.status_code == 200, response.text
    detail = response.json()
    assert detail["turkish"] == "sonuçlanmak / ortaya çıkmak"
    assert "Kalıp kökü: turn out" in detail["context"]
    assert "turned out" in detail["example"]


def test_fallback_translation_is_queued_not_written_to_static_map(app_module, monkeypatch):
    app_module.db_execute("DELETE FROM lexical_review_queue")
    monkeypatch.setattr(app_module, "GOOGLE_TRANSLATE_API_KEY", "")
    monkeypatch.setattr(app_module, "request_model", lambda *args, **kwargs: "özenli düzen")

    def fail_static_write(*args, **kwargs):
        raise AssertionError("fallback translations must not be written into library_word_map.json")

    monkeypatch.setattr(app_module, "save_json_map", fail_static_write)

    translated = app_module.translate_library_word_with_fallback("careful-system", "careful system")
    row = app_module.db_fetchone(
        "SELECT term, canonical, meaning, kind, source, status, occurrence_count FROM lexical_review_queue WHERE term = ?",
        ("careful-system",),
    )

    assert translated == "özenli düzen"
    assert row is not None
    assert row["canonical"] == "careful system"
    assert row["meaning"] == "özenli düzen"
    assert row["kind"] == "phrase"
    assert row["source"] == "ai_fallback"
    assert row["status"] == "pending"
    assert int(row["occurrence_count"]) == 1


def test_approved_lexical_entries_join_runtime_phrase_map(app_module):
    timestamp = app_module.now_iso()
    app_module.db_execute(
        """
        INSERT INTO lexical_entries (term, meaning, kind, source, confidence, created_at, updated_at)
        VALUES (?, ?, 'phrase', 'curated', 1.0, ?, ?)
        """,
        ("micro habit", "mikro alışkanlık", timestamp, timestamp),
    )
    app_module.get_approved_lexical_map(force=True)

    glossary = app_module.build_library_glossary("A micro habit can make practice easier.")

    assert glossary["micro habit"]["turkish"] == "mikro alışkanlık"
    assert glossary["micro habit"]["kind"] == "phrase"


def test_social_friend_request_accept_and_cheer(client):
    register_user(client, username="socialone")
    client.post("/api/auth/logout")
    register_user(client, username="socialtwo")
    client.post("/api/auth/logout")

    login_user(client, username="socialone")
    request_response = client.post("/api/social/request", json={"username": "socialtwo"})
    assert request_response.status_code == 200, request_response.text
    assert len(request_response.json()["outgoing"]) == 1
    client.post("/api/auth/logout")

    login_user(client, username="socialtwo")
    overview_response = client.get("/api/social")
    assert overview_response.status_code == 200, overview_response.text
    incoming = overview_response.json()["incoming"]
    assert len(incoming) == 1

    accept_response = client.post(
        f"/api/social/requests/{incoming[0]['request_id']}",
        json={"action": "accept"},
    )
    assert accept_response.status_code == 200, accept_response.text
    friends = accept_response.json()["friends"]
    assert len(friends) == 1
    assert friends[0]["username"] == "socialone"

    cheer_response = client.post(f"/api/social/friends/{friends[0]['friendship_id']}/cheer")
    assert cheer_response.status_code == 200, cheer_response.text


def test_social_search_and_suggestions_are_actionable(client):
    register_user(client, username="alphauser")
    client.post("/api/auth/logout")
    register_user(client, username="betabuddy")
    client.post("/api/auth/logout")

    login_user(client, username="alphauser")
    search_response = client.get("/api/social/search?q=beta")
    assert search_response.status_code == 200, search_response.text
    results = search_response.json()["results"]
    assert len(results) == 1
    assert results[0]["username"] == "betabuddy"
    assert results[0]["relationship"] == "none"

    request_response = client.post("/api/social/request", json={"username": "betabuddy"})
    assert request_response.status_code == 200, request_response.text
    assert request_response.json()["outgoing"][0]["user"]["username"] == "betabuddy"

    search_after_request = client.get("/api/social/search?q=beta")
    assert search_after_request.status_code == 200, search_after_request.text
    assert search_after_request.json()["results"][0]["relationship"] == "pending_outgoing"
