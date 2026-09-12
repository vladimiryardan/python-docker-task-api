from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test task",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data


def test_update_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated title"
    assert data["completed"] is True


def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete me",
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

    get_response = client.get("/tasks")

    assert get_response.status_code == 200
    assert get_response.json() == []