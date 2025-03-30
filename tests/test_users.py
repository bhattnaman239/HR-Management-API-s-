import uuid

def get_auth_header(client, username, password):
    resp = client.post("/auth/login", data={"username": username, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def random_task_title():
    return f"{uuid.uuid4().hex[:5]}"

# --- GET USERS ---

def test_get_users_unauthorized(client):
    """No token => 401 Unauthorized."""
    response = client.get("/users/")
    assert response.status_code == 401

def test_get_users_admin(client):
    """Admin should be able to see all users."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

def test_get_users_user(client):
    """Normal user should not be allowed to list all users."""
    headers = get_auth_header(client, "test_user", "Test@1234")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 403

def test_get_users_reader(client):
    """Reader access for listing users; adjust based on your logic (here we assume allowed)."""
    headers = get_auth_header(client, "test_reader", "Test@1234")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# --- CREATE USER ---
def test_create_admin_as_admin(client):
    """Admin should be able to create a new admin user."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    random = random_task_title()
    payload = {
        "name": "NewAdmin(ADMIN)"+random,
        "username": random,
        "password": "Pass1234!",
        "role": "admin"
    }
    response = client.post("/users/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == random
 

def test_create_user_as_admin(client):
    """Admin can create new users."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    random = random_task_title()
    payload = {
        "name": "NewUser(Admin)"+random,
        "username": random ,
        "password": "Pass1234!",
        "role": "user"
    }
    resp = client.post("/users/", json=payload, headers=headers)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["username"] == random


def test_create_reader_as_admin(client):
    """Admin can create new readers."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    random = random_task_title()
    payload = {
        "name": "NewReader(Admin)"+random,
        "username": random ,
        "password": "Pass1234!",
        "role": "reader"
    }
    resp = client.post("/users/", json=payload, headers=headers)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["username"] == random


def test_create_user_as_normal_user(client):
    """Normal user is not allowed to create other users => 403."""
    headers = get_auth_header(client, "test_user", "Test@1234")
    payload = {
        "name": "User Attempt",
        "username": "NewUser(User)",
        "password": "Pass1234!",
        "role": "user"
    }
    resp = client.post("/users/", json=payload, headers=headers)
    assert resp.status_code == 403

def test_create_user_as_reader(client):
    """Reader cannot create users => 403."""
    headers = get_auth_header(client, "test_reader", "Test@1234")
    payload = {
        "name": "Reader Attempt",
        "username": "NewUser(Reader)",
        "password": "Pass1234!",
        "role": "user"
    }
    resp = client.post("/users/", json=payload, headers=headers)
    assert resp.status_code == 403

# --- UPDATE USER ---
def test_update_admin_as_admin(client):
    """Admin can update anything"""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    payload = {
        "name": "Update Admin(Admin)"+random_task_title(),
        "username": random_task_title(),
        "password": "Test@1234",
        "role": "admin"
        }
    create_resp = client.post("/users/", json=payload, headers=headers)
    assert create_resp.status_code == 201, create_resp.text
    user = create_resp.json()
    user_id = user["id"]
    update_payload = {"name": "Updated Admin(ADMIN)"}
    update_resp = client.put(f"/users/{user_id}", json=update_payload, headers=headers
    )
    assert update_resp.status_code in [200, 204]

def test_update_user_admin(client):
    """Admin can update any user's info."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    payload = {
        "name": "Update User(Admin)"+random_task_title(),
        "username": random_task_title(),
        "password": "Pass1234!",
        "role": "user"
    }
    create_resp = client.post("/users/", json=payload, headers=headers)
    assert create_resp.status_code == 201, create_resp.text
    user = create_resp.json()
    user_id = user["id"]
    update_payload = {"name": "Updated User(ADMIN)"}
    update_resp = client.put(f"/users/{user_id}", json=update_payload, headers=headers)
    assert update_resp.status_code in [200, 204]


def test_update_reader_as_admin(client):
    """Admin can update reader's info"""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    payload = {
        "name": "Update Reader(Admin)"+random_task_title(),
        "username": random_task_title(),
        "password": "Test@1234",
        "role": "reader"
    }
    create_resp = client.post("/users/", json=payload, headers=headers)
    assert create_resp.status_code == 201, create_resp.text
    user = create_resp.json()
    user_id = user["id"]
    update_payload = {"name": "Updated Reader(ADMIN)"}
    update_resp = client.put(f"/users/{user_id}", json=update_payload, headers=headers
    )
    assert update_resp.status_code in [200, 204]

def test_update_user_as_normal_user(client):
    """
    Normal user tries to update another user (e.g. admin) => 403.
    """
    user_headers = get_auth_header(client, "test_user", "Test@1234")
    update_payload = {"name": "Illegal Update on Admin"}
    resp = client.put("/users/1", json=update_payload, headers=user_headers)
    assert resp.status_code == 403

def test_update_user_as_reader(client):
    """Reader cannot update any user => 403."""
    reader_headers = get_auth_header(client, "test_reader", "Test@1234")
    update_payload = {"name": "Reader Attempted Update"}
    resp = client.put("/users/1", json=update_payload, headers=reader_headers)
    assert resp.status_code == 403
    

# --- DELETE USER ---
def test_delete_user_as_admin(client):
    """Admin can delete a admin."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    random = random_task_title()
    payload = {
        "name": "Delete Admin(ADMIN)"+random,
        "username": random,
        "password": "Pass1234!",
        "role": "admin"
    }
    create_resp = client.post("/users/", json=payload, headers=headers)
    assert create_resp.status_code == 201, create_resp.text
    user_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_resp.status_code in [200, 204]


def test_delete_user_as_admin(client):
    """Admin can delete a user."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    random = random_task_title()
    payload = {
        "name": "Delete User(ADMIN)"+random,
        "username": random,
        "password": "Pass1234!",
        "role": "user"
    }
    create_resp = client.post("/users/", json=payload, headers=headers)
    assert create_resp.status_code == 201, create_resp.text
    user_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_resp.status_code in [200, 204]


def test_delete_user_as_admin(client):
    """Admin can delete a reader."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    random = random_task_title()
    payload = {
        "name": "Delete Reader(ADMIN)"+random,
        "username": random,
        "password": "Pass1234!",
        "role": "reader"
    }
    create_resp = client.post("/users/", json=payload, headers=headers)
    assert create_resp.status_code == 201, create_resp.text
    user_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_resp.status_code in [200, 204]

def test_delete_user_as_normal_user(client):
    """Normal user cannot delete another user => 403."""
    headers = get_auth_header(client, "test_user", "Test@1234")
    resp = client.delete("/users/1", headers=headers)
    assert resp.status_code == 403

def test_delete_user_as_reader(client):
    """Reader cannot delete any user => 403."""
    headers = get_auth_header(client, "test_reader", "Test@1234")
    resp = client.delete("/users/1", headers=headers)
    assert resp.status_code == 403
