"""
Tests for the GET /activities endpoint (list all activities).
"""

import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """
    Test that GET /activities returns all activities with correct structure.
    
    ARRANGE: Client is set up via fixture
    ACT: Make GET request to /activities
    ASSERT: Verify response contains all activities with required fields
    """
    # ARRANGE
    # (client and reset_activities fixtures handle setup)
    expected_activity_names = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball",
        "Soccer",
        "Art Club",
        "Music Ensemble",
        "Debate Team",
        "Science Club",
    ]
    
    # ACT
    response = client.get("/activities")
    activities = response.json()
    
    # ASSERT
    assert response.status_code == 200
    assert len(activities) == len(expected_activity_names)
    
    for activity_name in expected_activity_names:
        assert activity_name in activities
    
    # Verify required fields in each activity
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_response_contains_chess_club(client, reset_activities):
    """
    Test that the Chess Club activity exists with expected data.
    
    ARRANGE: Client is set up via fixture
    ACT: Make GET request to /activities
    ASSERT: Verify Chess Club has correct details
    """
    # ARRANGE
    expected_chess_club_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # ACT
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities.get("Chess Club")
    
    # ASSERT
    assert chess_club is not None
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess_club["max_participants"] == 12
    assert chess_club["participants"] == expected_chess_club_participants
