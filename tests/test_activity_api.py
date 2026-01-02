import copy
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


import pytest


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a deep copy of activities and restore after each test to keep tests isolated
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Tennis Club" in data
    assert "participants" in data["Tennis Club"]


def test_signup_success_and_normalization():
    activity_name = "Tennis Club"
    email = "  NewStudent@Mergington.EDU "

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Verify email stored normalized (lowercase, trimmed)
    assert "newstudent@mergington.edu" in [p.lower() for p in activities[activity_name]["participants"]]


def test_signup_duplicate():
    activity_name = "Tennis Club"
    email = "alex@mergington.edu"

    # First signup should already be present in initial data
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already signed up for this activity"


def test_signup_activity_not_found():
    activity_name = "Nonexistent Club"
    email = "someone@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_activity_full():
    activity_name = "Math Olympiad"
    email = "extra@mergington.edu"

    # Fill the activity to capacity
    activities[activity_name]["participants"] = [f"u{i}@mergington.edu" for i in range(activities[activity_name]["max_participants"])]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unsubscribe_activity_not_found():
    activity_name = "NoSuchActivity"
    email = "someone@mergington.edu"

    response = client.post(f"/activities/{activity_name}/unsubscribe?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
