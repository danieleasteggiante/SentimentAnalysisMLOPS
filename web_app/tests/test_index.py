import pytest

def test_smoke():
    assert True

def test_index_route(app):
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"ok" in resp.data