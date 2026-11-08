import pytest
from fastapi.testclient import TestClient

from app.main import app, get_repo
from app.repository import TaskRepository


@pytest.fixture
def repo() -> TaskRepository:
    return TaskRepository()  # fresh, empty store per test


@pytest.fixture
def client(repo: TaskRepository):
    app.dependency_overrides[get_repo] = lambda: repo
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()  # teardown, like Dispose()


@pytest.fixture
def make_task(client):
    """Factory fixture: call it to POST a task and get the JSON back."""
    def _make(**overrides):
        body = {"title": "Sample task", **overrides}
        response = client.post("/tasks", json=body)
        assert response.status_code == 201, response.text
        return response.json()
    return _make