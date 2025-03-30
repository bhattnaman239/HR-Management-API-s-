def test_login_admin_success(client):
    """Admin can log in successfully."""
    response = client.post(
        "/auth/login", data={"username": "admin_test", "password": "Test@1234"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_success(client):
    """Normal user can log in successfully."""
    response = client.post(
        "/auth/login", data={"username": "test_user", "password": "Test@1234"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_reader_success(client):
    """Reader can log in successfully."""
    response = client.post(
        "/auth/login", data={"username": "test_reader", "password": "Test@1234"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_failure(client):
    """Invalid credentials should fail."""
    response = client.post(
        "/auth/login", data={"username": "wrong_user", "password": "Nope"}
    )
    assert response.status_code == 404
