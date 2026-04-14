import pytest

def test_get_activities(client):
    """Test GET /activities returns all activities with correct structure"""
    # Arrange - No specific setup needed, activities are initialized in fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()

    # Should have 9 activities
    assert len(data) == 9

    # Check that all expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Drama Club", "Art Studio", "Debate Team", "Science Club"
    ]
    for activity in expected_activities:
        assert activity in data

    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_valid(client):
    """Test successful signup for an activity"""
    # Arrange - No specific setup needed

    # Act
    response = client.post("/activities/Chess Club/signup?email=test@example.com")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@example.com" in data["message"]
    assert "Chess Club" in data["message"]

    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "test@example.com" in activities["Chess Club"]["participants"]

def test_signup_duplicate(client):
    """Test signup fails when student is already signed up"""
    # Arrange
    client.post("/activities/Chess Club/signup?email=duplicate@example.com")

    # Act
    response = client.post("/activities/Chess Club/signup?email=duplicate@example.com")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found(client):
    """Test signup fails for non-existent activity"""
    # Arrange - No specific setup needed

    # Act
    response = client.post("/activities/NonExistent Activity/signup?email=test@example.com")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_remove_participant_valid(client):
    """Test successful removal of a participant"""
    # Arrange
    client.post("/activities/Chess Club/signup?email=remove@example.com")

    # Act
    response = client.delete("/activities/Chess Club/participants/remove@example.com")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "remove@example.com" in data["message"]
    assert "Chess Club" in data["message"]

    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "remove@example.com" not in activities["Chess Club"]["participants"]

def test_remove_participant_not_found(client):
    """Test removal fails when participant is not signed up"""
    # Arrange - No specific setup needed

    # Act
    response = client.delete("/activities/Chess Club/participants/nonexistent@example.com")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]

def test_remove_participant_activity_not_found(client):
    """Test removal fails for non-existent activity"""
    # Arrange - No specific setup needed

    # Act
    response = client.delete("/activities/NonExistent Activity/participants/test@example.com")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]