def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    payload = response.json()
    activities_response = client.get("/activities")
    activities_payload = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities_payload[activity_name]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/participants", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_not_found_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "notregistered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": missing_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"
