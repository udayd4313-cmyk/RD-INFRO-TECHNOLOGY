import pytest
from app import create_app
from app.config import Config


@pytest.fixture
def client(tmp_path):
    class TestConfig(Config):
        TESTING = True
        DATABASE_PATH = str(tmp_path / "test.db")

    return create_app(TestConfig).test_client()


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_student_crud(client):
    payload = {"name": "Ada", "age": 22, "gender": "Female", "marks": 95}
    created = client.post("/api/v1/students", json=payload)
    assert created.status_code == 201
    student_id = created.json["id"]
    assert client.get(f"/api/v1/students/{student_id}").status_code == 200
    assert client.put(f"/api/v1/students/{student_id}", json={**payload, "marks": 99}).status_code == 200
    assert client.delete(f"/api/v1/students/{student_id}").status_code == 204


def test_validation(client):
    assert client.post("/api/v1/students", json={}).status_code == 400
