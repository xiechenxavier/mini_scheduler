from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "mini_scheduler running"}


def test_schedule_greedy():
    response = client.post(
        "/schedule",
        json={
            "jobs": [3, 5, 2, 7],
            "machines": 2,
            "solver": "greedy",
            "use_lpt": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["makespan"] == 12
    assert sum(data["loads"]) == 17


def test_schedule_ortools():
    response = client.post(
        "/schedule",
        json={
            "jobs": [3, 5, 2, 7],
            "machines": 2,
            "solver": "ortools",
            "use_lpt": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["makespan"] == 9
    assert sum(data["loads"]) == 17


def test_schedule_invalid_solver():
    response = client.post(
        "/schedule",
        json={
            "jobs": [3, 5, 2, 7],
            "machines": 2,
            "solver": "abc",
            "use_lpt": False,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported solver: abc"


def test_schedule_invalid_machines():
    response = client.post(
        "/schedule",
        json={
            "jobs": [3, 5, 2, 7],
            "machines": 0,
            "solver": "greedy",
            "use_lpt": False,
        },
    )

    assert response.status_code == 422