import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from faker import Faker
from main import app, db

fake = Faker()


@pytest.fixture(autouse=True)
def clear_db():
    db.clear()
    yield
    db.clear()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_user_201(async_client):
    payload = {"username": fake.user_name(), "age": fake.random_int(min=1, max=99)}
    response = await async_client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_existing_user_200(async_client):
    payload = {"username": fake.user_name(), "age": fake.random_int(min=1, max=99)}
    create_resp = await async_client.post("/users", json=payload)
    user_id = create_resp.json()["id"]

    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]


@pytest.mark.asyncio
async def test_get_nonexistent_user_404(async_client):
    response = await async_client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_existing_user_204(async_client):
    payload = {"username": fake.user_name(), "age": fake.random_int(min=1, max=99)}
    create_resp = await async_client.post("/users", json=payload)
    user_id = create_resp.json()["id"]

    response = await async_client.delete(f"/users/{user_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_same_user_twice_404(async_client):
    payload = {"username": fake.user_name(), "age": fake.random_int(min=1, max=99)}
    create_resp = await async_client.post("/users", json=payload)
    user_id = create_resp.json()["id"]

    await async_client.delete(f"/users/{user_id}")
    response = await async_client.delete(f"/users/{user_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_state_isolation(async_client):
    assert len(db) == 0
    payload = {"username": fake.user_name(), "age": 25}
    await async_client.post("/users", json=payload)
    assert len(db) == 1


@pytest.mark.asyncio
async def test_create_boundary_age_1(async_client):
    payload = {"username": fake.user_name(), "age": 1}
    response = await async_client.post("/users", json=payload)
    assert response.status_code == 201
    assert response.json()["age"] == 1


@pytest.mark.asyncio
async def test_multiple_users_independent(async_client):
    payloads = [{"username": fake.user_name(), "age": fake.random_int(min=1, max=99)} for _ in range(3)]
    ids = []
    for p in payloads:
        resp = await async_client.post("/users", json=p)
        ids.append(resp.json()["id"])
    assert len(set(ids)) == 3
