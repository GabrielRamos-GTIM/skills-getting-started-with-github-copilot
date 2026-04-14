def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html"""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"