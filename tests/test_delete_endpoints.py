"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using AAA pattern."""

import pytest
from src.app import activities


class TestDeleteParticipantEndpoint:
    """Test suite for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_delete_existing_participant_success(self, client):
        """Test successful removal of an existing participant."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_delete_participant_removes_from_list(self, client):
        """Test that delete removes only the specified participant."""
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        other_email = "daniel@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )

        # Assert
        assert response.status_code == 200
        current_participants = activities[activity_name]["participants"]
        assert email_to_remove not in current_participants
        assert other_email in current_participants

    def test_delete_nonexistent_participant_fails(self, client):
        """Test that deleting a nonexistent participant returns 404."""
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_delete_from_nonexistent_activity_fails(self, client):
        """Test that deleting from a nonexistent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_delete_then_signup_allowed(self, client):
        """Test that a participant can sign up again after being deleted."""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act - First delete the participant
        delete_response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Then try to sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert delete_response.status_code == 200
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_delete_preserves_other_participants(self, client):
        """Test that deleting one participant preserves others."""
        # Arrange
        activity_name = "Programming Class"
        participants_before = activities[activity_name]["participants"].copy()
        email_to_remove = "emma@mergington.edu"
        other_emails = [p for p in participants_before if p != email_to_remove]

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )

        # Assert
        assert response.status_code == 200
        current_participants = activities[activity_name]["participants"]
        for email in other_emails:
            assert email in current_participants

    def test_delete_response_format(self, client):
        """Test that delete response has correct format."""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert isinstance(response_data["message"], str)

    def test_delete_same_participant_twice_fails_second_time(self, client):
        """Test that deleting the same participant twice fails on the second attempt."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act - First delete succeeds
        first_response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Second delete should fail
        second_response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert first_response.status_code == 200
        assert second_response.status_code == 404
