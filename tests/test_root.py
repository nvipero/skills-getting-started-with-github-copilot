"""
Tests for the GET / endpoint (root redirect).
"""

import pytest


def test_root_redirects_to_static_index(client, reset_activities):
    """
    Test that GET / redirects to /static/index.html with 307 status.
    
    ARRANGE: Client is set up via fixture
    ACT: Make GET request to /
    ASSERT: Verify redirect status code (307) and location header
    """
    # ARRANGE
    # (client and reset_activities fixtures handle setup)
    
    # ACT
    response = client.get("/", follow_redirects=False)
    
    # ASSERT
    assert response.status_code == 307
    assert response.headers.get("location") == "/static/index.html"
