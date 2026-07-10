import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(original_activities)


client = TestClient(app_module.app)


def test_unregister_participant_removes_the_email_from_activity():
    response = client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_404():
    response = client.delete("/activities/Chess%20Club/participants/unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
