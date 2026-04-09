"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern."""

import pytest
from src.app import activities


class TestSignupEndpoint:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_success(self, client):
        """Test successful signup of a new student to an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert email in activities[activity_name]["participants"]

    def test_signup_adds_email_to_participants_list(self, client):
        """Test that signup adds the email to the participants list."""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert len(activities[activity_name]["participants"]) == initial_count + 1
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_student_fails(self, client):
        """Test that duplicate signup returns an error."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_fails(self, client):
        """Test that signup to a nonexistent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_multiple_different_students(self, client):
        """Test that multiple different students can sign up for the same activity."""
        # Arrange
        activity_name = "Gym Class"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert len(activities[activity_name]["participants"]) == initial_count + 2
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]

    def test_signup_preserves_existing_participants(self, client):
        """Test that signup doesn't remove existing participants."""
        # Arrange
        activity_name = "Chess Club"
        existing_participants = activities[activity_name]["participants"].copy()
        new_email = "newperson@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        current_participants = activities[activity_name]["participants"]
        for existing_email in existing_participants:
            assert existing_email in current_participants

    def test_signup_response_format(self, client):
        """Test that signup response has correct format."""
        # Arrange
        activity_name = "Programming Class"
        email = "testuser@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert isinstance(response_data["message"], str)
