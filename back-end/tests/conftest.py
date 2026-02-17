import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(scope="session", autouse=True)
def mock_db_before_imports():
    with patch("app.database.connection.engine"), \
         patch("app.database.connection.SessionLocal"), \
         patch("app.main.engine"), \
         patch("app.main.SessionLocal"), \
         patch("app.main.Base"), \
         patch("app.main.seed_database"):
        yield
