import pytest
from fastapi.testclient import TestClient
from main import app, db


@pytest.fixture(autouse=True)
def clear_db():
    db.clear()
    yield
    db.clear()


client = TestClient(app)


def test_create_user():
    response = client.post("/users", json={"username": "alice", "age": 25})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["age"] == 25
    assert "id" in data


def test_get_existing_user():
    create_resp = client.post("/users", json={"username": "bob", "age": 30})
    user_id = create_resp.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "bob"


def test_get_nonexistent_user():
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_existing_user():
    create_resp = client.post("/users", json={"username": "charlie", "age": 22})
    user_id = create_resp.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204


def test_delete_nonexistent_user():
    response = client.delete("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_then_get_returns_404():
    create_resp = client.post("/users", json={"username": "dave", "age": 28})
    user_id = create_resp.json()["id"]
    client.delete(f"/users/{user_id}")
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_create_multiple_users_unique_ids():
    resp1 = client.post("/users", json={"username": "user1", "age": 20})
    resp2 = client.post("/users", json={"username": "user2", "age": 21})
    assert resp1.json()["id"] != resp2.json()["id"]
