"""
Shared pytest fixtures and configuration for API tests.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture to reset the global activities dictionary to its original state
    before and after each test to ensure test isolation.
    """
    # Store original activities
    original_activities = deepcopy(activities)
    
    yield
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)
