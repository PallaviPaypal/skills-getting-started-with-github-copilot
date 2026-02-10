import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    # Get an activity name
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "testuser@mergington.edu"

    # Sign up
    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200
    assert "message" in signup.json()

    # Unregister
    unregister = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister.status_code == 200
    assert "message" in unregister.json()

    # Unregister again (should fail or give a message)
    unregister2 = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister2.status_code in (400, 200)

def test_signup_invalid_email():
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "notanemail"
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code in (400, 422)
