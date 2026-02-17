import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_database_connection():
    mock_session = MagicMock()
    
    with patch("app.database.connection.engine") as mock_engine, \
         patch("app.database.connection.SessionLocal") as mock_session_local, \
         patch("app.main.engine") as mock_main_engine, \
         patch("app.main.SessionLocal") as mock_main_session_local, \
         patch("app.main.Base") as mock_base, \
         patch("app.main.seed_database"):
        
        mock_session_local.return_value = mock_session
        mock_main_session_local.return_value = mock_session
        yield


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    from app.database.connection import get_db
    from app.main import app
    
    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
