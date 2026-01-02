from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_unsubscribe_existing_participant():
    activity_name = "Tennis Club"
    email = "alex@mergington.edu"

    # Ensure alex is initially signed up
    assert email.lower() in [p.lower() for p in activities[activity_name]["participants"]]

    response = client.post(f"/activities/{activity_name}/unsubscribe?email={email}")
    assert response.status_code == 200
    assert "Unsubscribed" in response.json()["message"]

    # Verify participant removed
    assert email.lower() not in [p.lower() for p in activities[activity_name]["participants"]]


def test_unsubscribe_not_signed_up():
    activity_name = "Tennis Club"
    email = "not-signed-up@mergington.edu"

    response = client.post(f"/activities/{activity_name}/unsubscribe?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Email not signed up for this activity"
