from unittest.mock import MagicMock, Mock
from fastapi.testclient import TestClient
import pytest
import sys

# Mocking della dipendenza del database per i test
# scope session dice che la fixture viene eseguita una volta per sessione di test
@pytest.fixture(scope="session", autouse=True)
def mock_database():
    mock_db_module = Mock()
    mock_db_module.engine = MagicMock()
    mock_db_module.SessionLocal = MagicMock()
    mock_db_module.get_db = MagicMock()
    sys.modules['config.database'] = mock_db_module
    
    yield mock_db_module
    
    # Pulizia del mock dopo i test
    if 'config.database' in sys.modules:
        del sys.modules['config.database']

@pytest.fixture
# pytest inietta automaticamente mock_database 
# che trova nei sys.modules
def client(mock_database):
    # importando qui l'app Fastapi dopo aver 
    # mockato il database quando chiamerà get_db
    # dai sys.modules prenderà il mock anziché il vero db
    from main import app
    return TestClient(app)

def test_smoke():
    assert True

def test_index_route(client):
    resp = client.get("/")
    assert resp.status_code == 200