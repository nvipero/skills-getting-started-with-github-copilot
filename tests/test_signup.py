"""
Tests for the POST /activities/{activity_name}/signup endpoint (student signup).
"""

import pytest


def test_signup_new_student_success(client, reset_activities):
    """
    Test that a new student can successfully sign up for an activity.
    
    ARRANGE: Set up client and new email
    ACT: POST to signup endpoint with new email
    ASSERT: Verify status 200 and student added to participants
    """
    # ARRANGE
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    
    # Verify student was added to participants by checking via GET
    get_response = client.get("/activities")
    activities = get_response.json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client, reset_activities):
    """
    Test that signup fails with 404 when activity does not exist.
    
    ARRANGE: Set up client and invalid activity name
    ACT: POST to signup endpoint with non-existent activity
    ASSERT: Verify status 404 and error message
    """
    # ARRANGE
    invalid_activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # ACT
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student_fails(client, reset_activities):
    """
    Test that a student already signed up cannot sign up again.
    
    ARRANGE: Use existing participant from Chess Club
    ACT: Attempt to sign up the same student twice
    ASSERT: Verify second signup returns 400 error
    """
    # ARRANGE
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already in Chess Club
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # ASSERT
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_student_to_different_activity(client, reset_activities):
    """
    Test that a student can sign up for multiple different activities.
    
    ARRANGE: Use a student already in one activity
    ACT: Sign them up for a different activity
    ASSERT: Verify signup succeeds and student is in both activities
    """
    # ARRANGE
    student_email = "michael@mergington.edu"  # In Chess Club
    new_activity = "Programming Class"
    
    # ACT
    response = client.post(
        f"/activities/{new_activity}/signup",
        params={"email": student_email}
    )
    
    # ASSERT
    assert response.status_code == 200
    
    # Verify student is in both activities
    get_response = client.get("/activities")
    activities = get_response.json()
    assert student_email in activities["Chess Club"]["participants"]
    assert student_email in activities["Programming Class"]["participants"]
