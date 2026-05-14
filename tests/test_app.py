"""
Comprehensive test suite for FastAPI High School Management System API.

All tests follow the AAA (Arrange, Act, Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the operation being tested
- Assert: Verify the results

Tests are organized by endpoint to make them easy to navigate and maintain.
"""

import pytest
from fastapi.testclient import TestClient


# ============================================================================
# Tests for GET / (Root Endpoint)
# ============================================================================

class TestRootEndpoint:
    """Tests for the root endpoint that redirects to static content."""
    
    def test_root_redirects_to_static_index(self, test_client):
        """
        Test that GET / redirects to /static/index.html.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to root endpoint with follow_redirects=False
        - Assert: Verify response is a redirect (status 307) to /static/index.html
        """
        # Arrange
        # (test_client fixture is already set up)
        
        # Act
        response = test_client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


# ============================================================================
# Tests for GET /activities (Get All Activities)
# ============================================================================

class TestGetActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, test_client):
        """
        Test that GET /activities returns all available activities.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /activities endpoint
        - Assert: Verify response contains all activities with correct data
        """
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Basketball Training", "Art Club", "Drama Club", "Debate Team",
            "Science Olympiad"
        ]
        
        # Act
        response = test_client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert all(activity in activities for activity in expected_activities)
    
    def test_get_activities_response_structure(self, test_client):
        """
        Test that each activity in the response has the correct structure.
        
        AAA Pattern:
        - Arrange: Test client is ready, define expected fields
        - Act: Make GET request to /activities endpoint
        - Assert: Verify each activity has required fields with correct types
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = test_client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in {activity_name}"
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)


# ============================================================================
# Tests for POST /activities/{activity_name}/signup (Sign Up for Activity)
# ============================================================================

class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_successful(self, test_client):
        """
        Test that a student can successfully sign up for an activity.
        
        AAA Pattern:
        - Arrange: Prepare activity name and new student email
        - Act: Make POST request to sign up endpoint
        - Assert: Verify response is successful (200) and contains confirmation message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "signed up" in data["message"].lower()
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_activity_not_found(self, test_client):
        """
        Test that signing up for a non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Prepare non-existent activity name and student email
        - Act: Make POST request to sign up for non-existent activity
        - Assert: Verify response is 404 with "Activity not found" error
        """
        # Arrange
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_signup_student_already_signed_up(self, test_client):
        """
        Test that a student cannot sign up for an activity twice.
        
        AAA Pattern:
        - Arrange: Choose an activity and existing participant email
        - Act: Attempt to sign up with an email already registered
        - Assert: Verify response is 400 with "already signed up" error
        """
        # Arrange
        activity_name = "Chess Club"
        # Use an email that already exists in Chess Club participants
        email = "michael@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]


# ============================================================================
# Tests for DELETE /activities/{activity_name}/participants (Unregister)
# ============================================================================

class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/participants endpoint."""
    
    def test_unregister_successful(self, test_client):
        """
        Test that a student can successfully unregister from an activity.
        
        AAA Pattern:
        - Arrange: Choose an activity and existing participant
        - Act: Make DELETE request to unregister endpoint
        - Assert: Verify response is successful (200) with confirmation message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Removed" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_unregister_activity_not_found(self, test_client):
        """
        Test that unregistering from a non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Prepare non-existent activity name and email
        - Act: Make DELETE request for non-existent activity
        - Assert: Verify response is 404 with "Activity not found" error
        """
        # Arrange
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_unregister_participant_not_found(self, test_client):
        """
        Test that unregistering a non-existent participant returns 404.
        
        AAA Pattern:
        - Arrange: Choose an activity and email not registered for it
        - Act: Make DELETE request for participant not in the activity
        - Assert: Verify response is 404 with "Participant not found" error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegrationScenarios:
    """Integration tests for realistic user workflows."""
    
    def test_signup_and_unregister_flow(self, test_client):
        """
        Test the complete flow of signing up and then unregistering.
        
        AAA Pattern:
        - Arrange: Prepare activity and new student email
        - Act: Sign up for activity, then unregister
        - Assert: Verify both operations succeed and participant state changes
        """
        # Arrange
        activity_name = "Programming Class"
        email = "testflow@mergington.edu"
        
        # Act & Assert - First signup
        signup_response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify participant was added by checking activities list
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
        
        # Act & Assert - Then unregister
        unregister_response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify participant was removed
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]
