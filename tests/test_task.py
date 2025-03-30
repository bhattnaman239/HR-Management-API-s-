import uuid

def get_auth_header(client, username, password):
    """Helper to get the Bearer token header for a given user."""
    resp = client.post("/auth/login", data={"username": username, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def random_task_title():
    return f"{uuid.uuid4().hex[:5]}"

random = random_task_title()

# --- GET TASKS ---
def test_get_tasks_unauthorized(client):
    """No token => 401"""
    resp = client.get("/tasks/")
    assert resp.status_code == 401

def test_get_tasks_admin(client):
    """Admin can see all tasks."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    resp = client.get("/tasks/", headers=headers)
    assert resp.status_code == 200

def test_get_tasks_user(client):
    """User can see tasks ."""
    headers = get_auth_header(client, "test_user", "Test@1234")
    resp = client.get("/tasks/", headers=headers)
    assert resp.status_code == 200

def test_get_tasks_reader(client):
    """Reader can see tasks."""
    headers = get_auth_header(client, "test_reader", "Test@1234")
    resp = client.get("/tasks/", headers=headers)
    assert resp.status_code == 200

# --- CREATE TASK ---
def test_create_admin_admin(client):
    """Admin can create tasks for themselves."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    task_payload = {
        "title": "C_"+random,
        "description": "Create Admin task by ADMIN",
        "user_id": 1, 
        "status": "pending" 
    }
    resp = client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code in [200, 201], resp.text

def test_create_user_admin(client):
    """Admin can create tasks for anyone."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    task_payload = {
        "title": "C_"+random,
        "description": "Create User task by ADMIN",
        "user_id": 2,  
        "status": "pending"  
    }
    resp = client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code in [200, 201], resp.text

def test_create_reader_admin(client):
    """Admin can create tasks for anyone."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    task_payload = {
        "title": "C_"+random,
        "description": "Create Reader task by ADMIN",
        "user_id": 3,  
        "status": "pending" 
    }
    resp = client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code in [200, 201], resp.text

def test_create_task_user(client):
    """User can create tasks for themselves."""
    random= random_task_title()
    headers = get_auth_header(client, "test_user", "Test@1234")
    task_payload = {
        "title": "C_"+random+"_(ADMIN)",
        "description": "Create User task by USER",
        "user_id": 2 , 
        "status": "pending"  
    }
    resp = client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code in [200, 201]
    
def test_create_task_user_other(client):
    """User can create tasks for others."""
    headers = get_auth_header(client, "test_user", "Test@1234")
    task_payload = {
        "title": "C_"+random+"_(USER)",
        "description": "Create Admin/Reader task by USER",
        "user_id": 3 , 
        "status": "pending"  
        }
    resp = client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code == 200


def test_create_task_reader(client):
    """Reader should not be able to create tasks => 403."""
    headers = get_auth_header(client, "test_reader", "Test@1234")
    task_payload = {
        "title": "C_"+random,
        "description": "Reader attempt to create task",    
        "user_id": 3 , 
        "status": "pending" 
    }
    resp = client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code == 403

# --- UPDATE TASK ---
def test_update_task_admin(client):
    """Admin can update any task."""
    headers = get_auth_header(client, "admin_test", "Test@1234")

    create_payload = {
        "title": "U_"+random,
        "description": "Admin(ADMIN)",
        "user_id": 1,
        "status": "pending" 
    }
    create_resp = client.post("/tasks/", json=create_payload, headers=headers)
    assert create_resp.status_code in [200, 201], create_resp.text
    task = create_resp.json()
    task_id = task["id"]

    update_payload = {
        "title": "U_"+random+"_(ADMIN)",
        "description": "Updated Admin/User/Reader info by a ADMIN" , 
        "user_id": 1,
        "status": "Successful"
    }
    update_resp = client.put(f"/tasks/{task_id}", json=update_payload, headers=headers)
    assert update_resp.status_code in [200, 201, 204], update_resp.text


def test_update_own_task_user(client):
    """User can update their own task."""
    headers = get_auth_header(client, "test_user", "Test@1234")
    create_payload = {
        "title": "U_"+random,
        "description": "User(USER)",
        "user_id": 2, 
        "status": "pending" 
    }
    create_resp = client.post("/tasks/", json=create_payload, headers=headers)
    assert create_resp.status_code in [200, 201], create_resp.text
    task_id = create_resp.json()["id"]

    update_payload = {"title": "U_"+random+"_(USER)","description": "Updated Users info by a user", "status": "Successful"}
    update_resp = client.put(f"/tasks/{task_id}", json=update_payload, headers=headers)
    assert update_resp.status_code in [200, 201, 204], update_resp.text

def test_update_someone_else_task_user(client):
    """User tries to update admin's task => 403."""
    admin_headers = get_auth_header(client, "admin_test", "Test@1234")
    create_payload = {
        "title": "U_"+random,
        "description": "User successfully created task for admin, but cannot update it.",
        "user_id": 1, 
        "status": "pending"  
    }
    create_resp = client.post("/tasks/", json=create_payload, headers=admin_headers)
    assert create_resp.status_code in [200, 201]
    task_id = create_resp.json()["id"]
    user_headers = get_auth_header(client, "test_user", "Test@1234")
    update_resp = client.put(f"/tasks/{task_id}", json={"title": "User tries to update admin's task"}, headers=user_headers)
    assert update_resp.status_code == 403

def test_update_task_reader(client):
    """Reader cannot update any task => 403."""
    headers = get_auth_header(client, "test_reader", "Test@1234")
    update_resp = client.put("/tasks/1", json={"title": "Reader Attempt to update"}, headers=headers)
    assert update_resp.status_code == 403

# --- DELETE TASK ---
def test_delete_task_admin(client):
    """Admin can delete any task."""
    headers = get_auth_header(client, "admin_test", "Test@1234")
    random = random_task_title()
    create_payload = {
        "title": "D"+random,
        "description": "Task for Deletion",
        "user_id": 1
    }
    create_resp = client.post("/tasks/", json=create_payload, headers=headers)
    assert create_resp.status_code in [200, 201]
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_resp.status_code in [200, 204]

def test_delete_task_user(client):
    """Normal user should not be able to delete tasks => 403."""
    headers = get_auth_header(client, "test_user", "Test@1234")

    create_payload = {
        "title": "Delete attempt by User_"+random,
        "description": "User successfully created task, but cannot delete it.",
        "status": "pending", 
        "user_id": 2
    }
    create_resp = client.post("/tasks/", json=create_payload, headers=headers)
    assert create_resp.status_code in [200, 201]
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_resp.status_code == 403


def test_delete_task_reader(client):
    """Reader cannot delete tasks => 403."""
    headers = get_auth_header(client, "test_reader", "Test@1234")
    task_payload = {
        "title": "C_"+random,
        "description": "Reader attempt",    
        "user_id": 3 , 
        "status": "pending" 
    }
    resp = client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code == 403
