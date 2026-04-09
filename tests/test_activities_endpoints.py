"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern."""

import pytest
from src.app import activities


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities."""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_returns_dict_format(self, client):
        """Test that GET /activities returns a dictionary format."""
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_includes_all_required_fields(self, client):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity '{activity_name}' missing required fields"

    def test_get_activities_participants_is_list(self, client):
        """Test that participants field is a list."""
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Participants for '{activity_name}' should be a list"

    def test_get_activities_max_participants_is_integer(self, client):
        """Test that max_participants field is an integer."""
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"max_participants for '{activity_name}' should be an integer"

    def test_get_activities_reflects_current_participants(self, client):
        """Test that GET /activities shows current participant list."""
        # Arrange
        # The Chess Club should have 2 initial participants from conftest

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        chess_club_participants = data["Chess Club"]["participants"]
        assert len(chess_club_participants) == 2
        assert "michael@mergington.edu" in chess_club_participants
        assert "daniel@mergington.edu" in chess_club_participants
