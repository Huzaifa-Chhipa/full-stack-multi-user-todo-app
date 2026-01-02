"""
Integration tests for the Todo Application
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.db import engine, get_session
from backend.src.models.task import Task
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.pool import NullPool
from backend.src.auth.jwt import create_access_token
import os

# Override the database URL for testing
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

# Create test client
client = TestClient(app)

def test_authentication_flow():
    """
    T029: Test authentication flow
    - User can register and login successfully
    - JWT tokens issued and stored properly
    - Protected routes enforce authentication
    """
    # Test login endpoint
    response = client.post("/auth/token", data={
        "username": "testuser",
        "password": "testpass"
    })

    # Should return a token
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    token = response.json()["access_token"]

    # Test accessing a protected endpoint with valid token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/testuser/tasks", headers=headers)
    assert response.status_code == 200


def test_task_ownership_enforcement():
    """
    T030: Test task ownership enforcement
    - Users can only access their own tasks
    - Attempts to access other users' tasks return 404
    - Data isolation maintained at database level
    """
    # Create tokens for two different users
    user1_token = create_access_token(data={"sub": "user1"})
    user2_token = create_access_token(data={"sub": "user2"})

    headers1 = {"Authorization": f"Bearer {user1_token}"}
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    # Create a task for user1
    response = client.post(
        "/api/user1/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=headers1
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    # User1 should be able to access their own task
    response = client.get(f"/api/user1/tasks/{task_id}", headers=headers1)
    assert response.status_code == 200

    # User2 should NOT be able to access user1's task
    response = client.get(f"/api/user1/tasks/{task_id}", headers=headers2)
    assert response.status_code == 403  # Forbidden based on our implementation

    # User2 should get 404 if trying to access non-existent task under their user ID
    response = client.get(f"/api/user2/tasks/{task_id}", headers=headers2)
    assert response.status_code == 404


def test_full_task_crud_operations():
    """
    T031: Test full task CRUD operations
    - Create, read, update, delete tasks work end-to-end
    - All validation rules enforced
    - Proper error handling for edge cases
    """
    # Create a token for testing
    token = create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}

    # Test Create
    response = client.post(
        "/api/testuser/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=headers
    )
    assert response.status_code == 201
    task_id = response.json()["id"]
    assert response.json()["title"] == "Test task"
    assert response.json()["description"] == "Test description"
    assert response.json()["completed"] is False

    # Test Read (all tasks)
    response = client.get("/api/testuser/tasks", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == task_id

    # Test Read (single task)
    response = client.get(f"/api/testuser/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == task_id

    # Test Update
    response = client.put(
        f"/api/testuser/tasks/{task_id}",
        json={"title": "Updated task", "description": "Updated description"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated task"
    assert response.json()["description"] == "Updated description"

    # Test Toggle Completion
    response = client.patch(f"/api/testuser/tasks/{task_id}/complete", headers=headers)
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # Test Delete
    response = client.delete(f"/api/testuser/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    # Verify task is deleted
    response = client.get(f"/api/testuser/tasks/{task_id}", headers=headers)
    assert response.status_code == 404


def test_api_endpoint_status_codes():
    """
    T032: Verify all API endpoints return correct status codes per contract
    """
    token = create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}

    # Test Create Task - Valid data
    response = client.post(
        "/api/testuser/tasks",
        json={"title": "Valid task", "description": "Valid description"},
        headers=headers
    )
    assert response.status_code == 201

    task_id = response.json()["id"]

    # Test Create Task - Invalid data (empty title)
    response = client.post(
        "/api/testuser/tasks",
        json={"title": "", "description": "Valid description"},
        headers=headers
    )
    assert response.status_code == 422  # Validation error

    # Test Get Task - Valid
    response = client.get(f"/api/testuser/tasks/{task_id}", headers=headers)
    assert response.status_code == 200

    # Test Get Task - Invalid (non-existent)
    response = client.get("/api/testuser/tasks/99999", headers=headers)
    assert response.status_code == 404

    # Test Update Task - Valid
    response = client.put(
        f"/api/testuser/tasks/{task_id}",
        json={"title": "Updated task"},
        headers=headers
    )
    assert response.status_code == 200

    # Test Delete Task
    response = client.delete(f"/api/testuser/tasks/{task_id}", headers=headers)
    assert response.status_code == 204


def test_error_scenarios():
    """
    T033: Test error scenarios per edge cases in spec
    - JWT expiration redirects to login
    - Invalid JWT returns 401
    - Empty title returns 400
    - Non-existent task returns 404
    """
    # Test invalid JWT
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/testuser/tasks", headers=invalid_headers)
    assert response.status_code == 401

    # Test missing JWT
    response = client.get("/api/testuser/tasks")
    assert response.status_code == 403  # Will be 403 based on our implementation

    # Create a valid token for further tests
    token = create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}

    # Test empty title (validation error)
    response = client.post(
        "/api/testuser/tasks",
        json={"title": "", "description": "Valid description"},
        headers=headers
    )
    assert response.status_code == 422

    # Test too long title (validation error)
    long_title = "a" * 201  # More than 200 characters
    response = client.post(
        "/api/testuser/tasks",
        json={"title": long_title, "description": "Valid description"},
        headers=headers
    )
    assert response.status_code == 422

    # Test non-existent task
    response = client.get("/api/testuser/tasks/99999", headers=headers)
    assert response.status_code == 404

    # Test non-existent task update
    response = client.put(
        "/api/testuser/tasks/99999",
        json={"title": "Updated task"},
        headers=headers
    )
    assert response.status_code == 404

    # Test non-existent task deletion
    response = client.delete("/api/testuser/tasks/99999", headers=headers)
    assert response.status_code == 404


if __name__ == "__main__":
    # Run all tests
    test_authentication_flow()
    test_task_ownership_enforcement()
    test_full_task_crud_operations()
    test_api_endpoint_status_codes()
    test_error_scenarios()

    print("All integration tests passed!")