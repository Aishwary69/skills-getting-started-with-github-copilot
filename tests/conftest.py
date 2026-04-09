"""Shared pytest fixtures and configuration for backend tests."""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


# Store the original activities data for reset between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test.
    
    This fixture ensures test isolation by resetting the in-memory
    activities dictionary to its original state before each test runs.
    """
    # Clear and restore activities to original state
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup after test
    activities.clear()


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the FastAPI app."""
    return TestClient(app)
