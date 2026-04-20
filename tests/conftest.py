from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def app_module(tmp_path_factory: pytest.TempPathFactory):
    test_db_path = tmp_path_factory.mktemp("db") / "test_app.db"
    os.environ["READLEX_DB_PATH"] = str(test_db_path)
    os.environ["APP_BASE_URL"] = "http://127.0.0.1:8046"
    os.environ.pop("DATABASE_URL", None)
    os.environ.pop("POSTGRES_URL", None)
    sys.modules.pop("backend.main", None)
    import backend.main as main

    main = importlib.reload(main)
    return main


@pytest.fixture()
def isolated_db(app_module):
    app_module.db_execute("DELETE FROM sessions")
    app_module.db_execute("DELETE FROM email_verifications")
    app_module.db_execute("DELETE FROM saved_words")
    app_module.db_execute("DELETE FROM reading_history")
    app_module.db_execute("DELETE FROM user_progress")
    app_module.db_execute("DELETE FROM users")
    app_module.WORD_DETAIL_CACHE.clear()
    app_module.GENERATE_CACHE.clear()
    yield


@pytest.fixture()
def client(app_module, isolated_db):
    with TestClient(app_module.app) as test_client:
        yield test_client
