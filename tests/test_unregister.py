"""
Tests for the POST /unregister endpoint (student unregistration).
"""

import pytest


def test_unregister_student_success(client, reset_activities):
    """
    Test that a student can successfully unregister from an activity.
    
    ARRANGE: Use existing participant in an activity
    ACT: POST to unregister endpoint
    ASSERT: Verify status 200 and student removed from participants
    """
    # ARRANGE
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"  # Already in Chess Club
    
    # ACT
    response = client.post(
        "/unregister",
        params={"activity": activity_name, "email": student_email}
    )
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {student_email} from {activity_name}"
    
    # Verify student was removed by checking via GET
    get_response = client.get("/activities")
    activities = get_response.json()
    assert student_email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client, reset_activities):
    """
    Test that unregister fails with 404 when activity does not exist.
    
    ARRANGE: Set up client and invalid activity name
    ACT: POST to unregister with non-existent activity
    ASSERT: Verify status 404 and error message
    """
    # ARRANGE
    invalid_activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # ACT
    response = client.post(
        "/unregister",
        params={"activity": invalid_activity, "email": email}
    )
    
    # ASSERT
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_signed_up(client, reset_activities):
    """
    Test that unregister fails with 400 when student is not signed up.
    
    ARRANGE: Use a student not enrolled in the activity
    ACT: Attempt to unregister them
    ASSERT: Verify status 400 and error message
    """
    # ARRANGE
    activity_name = "Chess Club"
    # Create an email that's not in Chess Club (from a different activity)
    student_email = "emma@mergington.edu"  # In Programming Class, not Chess Club
    
    # ACT
    response = client.post(
        "/unregister",
        params={"activity": activity_name, "email": student_email}
    )
    
    # ASSERT
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up"


def test_unregister_then_signup_again_succeeds(client, reset_activities):
    """
    Test that a student can unregister and then sign up again for same activity.
    
    ARRANGE: Use existing participant
    ACT: Unregister, then sign up again
    ASSERT: Verify both operations succeed
    """
    # ARRANGE
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"
    
    # ACT: First unregister
    unregister_response = client.post(
        "/unregister",
        params={"activity": activity_name, "email": student_email}
    )
    
    # ASSERT first step
    assert unregister_response.status_code == 200
    
    # ACT: Then sign up again
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # ASSERT second step
    assert signup_response.status_code == 200
    
    # Verify student is back in the activity
    get_response = client.get("/activities")
    activities = get_response.json()
    assert student_email in activities[activity_name]["participants"]
