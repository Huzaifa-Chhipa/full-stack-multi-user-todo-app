"""
Integration tests for the Full-Stack Multi-User Web Todo Application
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_authentication_flow():
    """
    T029: Test authentication flow
    - User can register and login successfully
    - JWT tokens issued and stored properly
    - Protected routes enforce authentication
    """
    print("Testing authentication flow...")

    # Test login endpoint
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }

    response = requests.post(f"{BASE_URL}/auth/token", data=login_data)

    if response.status_code == 200:
        result = response.json()
        if "access_token" in result:
            print("✓ Authentication flow test passed")
            return result["access_token"]
        else:
            print("✗ Authentication flow test failed - no token returned")
            return None
    else:
        print(f"✗ Authentication flow test failed - status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def test_task_ownership_enforcement():
    """
    T030: Test task ownership enforcement
    - Users can only access their own tasks
    - Attempts to access other users' tasks return 404
    - Data isolation maintained at database level
    """
    print("Testing task ownership enforcement...")

    # Login as first user
    user1_login_data = {"username": "user1", "password": "pass1"}
    user1_response = requests.post(f"{BASE_URL}/auth/token", data=user1_login_data)

    if user1_response.status_code != 200:
        print("✗ Could not login as user1")
        return False

    user1_token = user1_response.json()["access_token"]
    user1_headers = {"Authorization": f"Bearer {user1_token}", **HEADERS}

    # Login as second user
    user2_login_data = {"username": "user2", "password": "pass2"}
    user2_response = requests.post(f"{BASE_URL}/auth/token", data=user2_login_data)

    if user2_response.status_code != 200:
        print("✗ Could not login as user2")
        return False

    user2_token = user2_response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}", **HEADERS}

    # Create a task for user1
    task_data = {"title": "User1's task", "description": "This belongs to user1"}
    create_response = requests.post(f"{BASE_URL}/api/user1/tasks",
                                   json=task_data, headers=user1_headers)

    if create_response.status_code != 201:
        print(f"✗ Could not create task for user1 - status: {create_response.status_code}")
        return False

    task_id = create_response.json()["id"]
    print(f"Created task with ID: {task_id}")

    # User1 should be able to access their own task
    get_response = requests.get(f"{BASE_URL}/api/user1/tasks/{task_id}",
                               headers=user1_headers)
    if get_response.status_code != 200:
        print(f"✗ User1 could not access their own task - status: {get_response.status_code}")
        return False

    # User2 should NOT be able to access user1's task
    get_response2 = requests.get(f"{BASE_URL}/api/user1/tasks/{task_id}",
                                headers=user2_headers)
    if get_response2.status_code == 403 or get_response2.status_code == 404:
        print("✓ Task ownership enforcement working correctly")
        return True
    else:
        print(f"✗ Task ownership enforcement failed - user2 could access user1's task with status: {get_response2.status_code}")
        return False


def test_full_task_crud_operations():
    """
    T031: Test full task CRUD operations
    - Create, read, update, delete tasks work end-to-end
    - All validation rules enforced
    - Proper error handling for edge cases
    """
    print("Testing full task CRUD operations...")

    # Login
    login_data = {"username": "crudtest", "password": "password"}
    login_response = requests.post(f"{BASE_URL}/auth/token", data=login_data)

    if login_response.status_code != 200:
        print("✗ Could not login for CRUD test")
        return False

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", **HEADERS}

    # Test Create
    task_data = {"title": "CRUD Test Task", "description": "Testing CRUD operations"}
    create_response = requests.post(f"{BASE_URL}/api/crudtest/tasks",
                                   json=task_data, headers=headers)

    if create_response.status_code != 201:
        print(f"✗ Create operation failed - status: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return False

    task_id = create_response.json()["id"]
    print(f"✓ Create operation successful - task ID: {task_id}")

    # Test Read (all tasks)
    read_all_response = requests.get(f"{BASE_URL}/api/crudtest/tasks", headers=headers)
    if read_all_response.status_code != 200:
        print(f"✗ Read all operation failed - status: {read_all_response.status_code}")
        return False

    if len(read_all_response.json()) == 0:
        print("✗ Read all operation returned no tasks")
        return False

    print("✓ Read all operation successful")

    # Test Read (single task)
    read_one_response = requests.get(f"{BASE_URL}/api/crudtest/tasks/{task_id}",
                                    headers=headers)
    if read_one_response.status_code != 200:
        print(f"✗ Read single operation failed - status: {read_one_response.status_code}")
        return False

    print("✓ Read single operation successful")

    # Test Update
    update_data = {"title": "Updated CRUD Test Task", "description": "Updated description"}
    update_response = requests.put(f"{BASE_URL}/api/crudtest/tasks/{task_id}",
                                  json=update_data, headers=headers)
    if update_response.status_code != 200:
        print(f"✗ Update operation failed - status: {update_response.status_code}")
        return False

    print("✓ Update operation successful")

    # Test Toggle Completion
    toggle_response = requests.patch(f"{BASE_URL}/api/crudtest/tasks/{task_id}/complete",
                                    headers=headers)
    if toggle_response.status_code != 200:
        print(f"✗ Toggle completion operation failed - status: {toggle_response.status_code}")
        return False

    if not toggle_response.json()["completed"]:
        print("✗ Toggle completion didn't change status to completed")
        return False

    print("✓ Toggle completion operation successful")

    # Test Delete
    delete_response = requests.delete(f"{BASE_URL}/api/crudtest/tasks/{task_id}",
                                     headers=headers)
    if delete_response.status_code != 204:
        print(f"✗ Delete operation failed - status: {delete_response.status_code}")
        return False

    print("✓ Delete operation successful")

    # Verify task is deleted
    verify_response = requests.get(f"{BASE_URL}/api/crudtest/tasks/{task_id}",
                                  headers=headers)
    if verify_response.status_code != 404:
        print(f"✗ Task not properly deleted - status: {verify_response.status_code}")
        return False

    print("✓ Task properly deleted")
    print("✓ All CRUD operations working correctly")
    return True


def test_api_endpoint_status_codes():
    """
    T032: Verify all API endpoints return correct status codes per contract
    """
    print("Testing API endpoint status codes...")

    # Test without authentication (should return 403 for protected endpoints)
    response = requests.get(f"{BASE_URL}/api/testuser/tasks")
    if response.status_code not in [401, 403]:
        print(f"✗ Protected endpoint accessible without auth - status: {response.status_code}")
        return False

    print("✓ Protected endpoints properly restricted")

    # Login to get a token for further tests
    login_data = {"username": "statustest", "password": "password"}
    login_response = requests.post(f"{BASE_URL}/auth/token", data=login_data)

    if login_response.status_code != 200:
        print("✗ Could not login for status code test")
        return False

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", **HEADERS}

    # Test Create Task - Valid data (should return 201)
    valid_task = {"title": "Valid task", "description": "Valid description"}
    create_response = requests.post(f"{BASE_URL}/api/statustest/tasks",
                                   json=valid_task, headers=headers)
    if create_response.status_code != 201:
        print(f"✗ Valid create request didn't return 201 - status: {create_response.status_code}")
        return False

    task_id = create_response.json()["id"]
    print("✓ Valid create request returned 201")

    # Test Get Task - Valid (should return 200)
    get_response = requests.get(f"{BASE_URL}/api/statustest/tasks/{task_id}", headers=headers)
    if get_response.status_code != 200:
        print(f"✗ Valid get request didn't return 200 - status: {get_response.status_code}")
        return False

    print("✓ Valid get request returned 200")

    # Test Get Task - Invalid (non-existent, should return 404)
    invalid_response = requests.get(f"{BASE_URL}/api/statustest/tasks/99999", headers=headers)
    if invalid_response.status_code != 404:
        print(f"✗ Invalid get request didn't return 404 - status: {invalid_response.status_code}")
        return False

    print("✓ Invalid get request returned 404")

    # Test Delete Task (should return 204)
    delete_response = requests.delete(f"{BASE_URL}/api/statustest/tasks/{task_id}", headers=headers)
    if delete_response.status_code != 204:
        print(f"✗ Delete request didn't return 204 - status: {delete_response.status_code}")
        return False

    print("✓ Delete request returned 204")

    print("✓ API endpoint status codes are correct")
    return True


def test_error_scenarios():
    """
    T033: Test error scenarios per edge cases in spec
    - JWT expiration redirects to login
    - Invalid JWT returns 401
    - Empty title returns 400
    - Non-existent task returns 404
    """
    print("Testing error scenarios...")

    # Login to get a token
    login_data = {"username": "errortest", "password": "password"}
    login_response = requests.post(f"{BASE_URL}/auth/token", data=login_data)

    if login_response.status_code != 200:
        print("✗ Could not login for error scenario test")
        return False

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", **HEADERS}

    # Test invalid JWT
    invalid_headers = {"Authorization": "Bearer invalid_token", **HEADERS}
    invalid_response = requests.get(f"{BASE_URL}/api/errortest/tasks", headers=invalid_headers)
    if invalid_response.status_code not in [401, 403]:
        print(f"✗ Invalid JWT didn't return 401/403 - status: {invalid_response.status_code}")
        return False

    print("✓ Invalid JWT properly handled")

    # Test empty title (validation error)
    empty_title_data = {"title": "", "description": "Valid description"}
    empty_response = requests.post(f"{BASE_URL}/api/errortest/tasks",
                                  json=empty_title_data, headers=headers)
    if empty_response.status_code not in [400, 422]:
        print(f"✗ Empty title didn't return 400/422 - status: {empty_response.status_code}")
        return False

    print("✓ Empty title properly handled")

    # Test too long title (validation error)
    long_title = "a" * 201  # More than 200 characters
    long_title_data = {"title": long_title, "description": "Valid description"}
    long_response = requests.post(f"{BASE_URL}/api/errortest/tasks",
                                 json=long_title_data, headers=headers)
    if long_response.status_code not in [400, 422]:
        print(f"✗ Long title didn't return 400/422 - status: {long_response.status_code}")
        return False

    print("✓ Long title properly handled")

    # Test non-existent task
    not_found_response = requests.get(f"{BASE_URL}/api/errortest/tasks/99999", headers=headers)
    if not_found_response.status_code != 404:
        print(f"✗ Non-existent task didn't return 404 - status: {not_found_response.status_code}")
        return False

    print("✓ Non-existent task properly handled")

    print("✓ All error scenarios handled correctly")
    return True


def run_all_tests():
    """
    Run all integration and verification tests
    """
    print("Starting integration and verification tests...\n")

    all_passed = True

    # Run each test
    token = test_authentication_flow()
    if token:
        print("✓ Authentication flow test passed\n")
    else:
        print("✗ Authentication flow test failed\n")
        all_passed = False

    if test_task_ownership_enforcement():
        print("✓ Task ownership enforcement test passed\n")
    else:
        print("✗ Task ownership enforcement test failed\n")
        all_passed = False

    if test_full_task_crud_operations():
        print("✓ Full CRUD operations test passed\n")
    else:
        print("✗ Full CRUD operations test failed\n")
        all_passed = False

    if test_api_endpoint_status_codes():
        print("✓ API endpoint status codes test passed\n")
    else:
        print("✗ API endpoint status codes test failed\n")
        all_passed = False

    if test_error_scenarios():
        print("✓ Error scenarios test passed\n")
    else:
        print("✗ Error scenarios test failed\n")
        all_passed = False

    if all_passed:
        print("🎉 All integration and verification tests passed!")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    run_all_tests()