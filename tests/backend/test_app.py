from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Test activity",
                "schedule": "Fridays",
                "max_participants": 10,
                "participants": ["alice@example.com"],
            }
        }
    )


def test_unregister_participant_removes_them_from_activity():
    # Arrange
    reset_activities()

    # Act
    response = client.delete("/activities/Chess Club/participants/alice@example.com")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered alice@example.com from Chess Club"
    }
    assert activities["Chess Club"]["participants"] == []


def test_activities_endpoint_disables_caching():
    # Arrange
    # No setup required for this endpoint test.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers["cache-control"].lower().startswith("no-store")
