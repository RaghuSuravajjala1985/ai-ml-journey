import pytest


def test_create_task_returns_201_and_server_fields(client):
    response = client.post("/tasks", json={"title": "  Learn FastAPI  ", "tags": ["week01"]})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Learn FastAPI"  # whitespace stripped
    assert body["priority"] == "medium"       # default applied
    assert body["done"] is False
    assert "created_at" in body


@pytest.mark.parametrize(
    "payload, error_type",
    [
        ({"title": ""}, "string_too_short"),
        ({"title": "x" * 121}, "string_too_long"),
        ({"title": "ok", "priority": "urgent"}, "enum"),
        ({"title": "ok", "colour": "red"}, "extra_forbidden"),
        ({}, "missing"),
    ],
)
def test_create_task_rejects_invalid_body(client, payload, error_type):
    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    types = [err["type"] for err in response.json()["detail"]]
    assert error_type in types


def test_client_cannot_set_id(client):
    response = client.post("/tasks", json={"title": "sneaky", "id": 42})
    assert response.status_code == 422


def test_get_task_by_id(client, make_task):
    created = make_task(title="Find me")

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_task_returns_404(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task 999 not found"}


def test_get_task_with_non_int_id_returns_422(client):
    assert client.get("/tasks/abc").status_code == 422


def test_list_filters_by_priority(client, make_task):
    make_task(title="a", priority="high")
    make_task(title="b", priority="low")
    make_task(title="c", priority="high")

    response = client.get("/tasks", params={"priority": "high"})

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["a", "c"]


def test_list_respects_limit_bounds(client, make_task):
    for i in range(3):
        make_task(title=f"t{i}")

    assert len(client.get("/tasks", params={"limit": 2}).json()) == 2
    assert client.get("/tasks", params={"limit": 0}).status_code == 422
    assert client.get("/tasks", params={"limit": 101}).status_code == 422


def test_each_test_starts_empty(client):
    assert client.get("/tasks").json() == []