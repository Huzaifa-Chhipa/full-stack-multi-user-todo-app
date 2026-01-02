"""
Test script to validate the functionality of the console todo application.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_manager import TaskManager
from src.models.task import Task

def test_task_creation():
    """Test creating tasks with validation."""
    print("Testing task creation...")

    # Test valid task creation
    try:
        task = Task(1, "Test task", "Test description")
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.completed == False
        print("[PASS] Valid task creation works")
    except Exception as e:
        print(f"[FAIL] Valid task creation failed: {e}")
        return False

    # Test empty title validation
    try:
        Task(1, "")
        print("[FAIL] Empty title validation failed")
        return False
    except ValueError:
        print("[PASS] Empty title validation works")

    # Test whitespace-only title validation
    try:
        Task(1, "   ")
        print("[FAIL] Whitespace-only title validation failed")
        return False
    except ValueError:
        print("[PASS] Whitespace-only title validation works")

    return True

def test_task_manager():
    """Test TaskManager functionality."""
    print("\nTesting TaskManager...")

    tm = TaskManager()

    # Test adding tasks
    try:
        task1 = tm.add_task("First task", "Description 1")
        task2 = tm.add_task("Second task", "Description 2")

        assert task1.id == 1
        assert task2.id == 2
        assert len(tm.get_all_tasks()) == 2
        print("[PASS] Task addition works")
    except Exception as e:
        print(f"[FAIL] Task addition failed: {e}")
        return False

    # Test getting all tasks (should be sorted by ID)
    try:
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2
        print("[PASS] Task retrieval and sorting works")
    except Exception as e:
        print(f"[FAIL] Task retrieval failed: {e}")
        return False

    # Test updating tasks
    try:
        updated_task = tm.update_task(1, "Updated task", "Updated description")
        assert updated_task.title == "Updated task"
        assert updated_task.description == "Updated description"
        print("[PASS] Task update works")
    except Exception as e:
        print(f"[FAIL] Task update failed: {e}")
        return False

    # Test toggling completion
    try:
        toggled_task = tm.toggle_task_completion(1)
        assert toggled_task.completed == True
        toggled_task2 = tm.toggle_task_completion(1)
        assert toggled_task2.completed == False
        print("[PASS] Task completion toggle works")
    except Exception as e:
        print(f"[FAIL] Task completion toggle failed: {e}")
        return False

    # Test deleting tasks
    try:
        initial_count = len(tm.get_all_tasks())
        deleted = tm.delete_task(1)
        assert deleted == True
        assert len(tm.get_all_tasks()) == initial_count - 1
        print("[PASS] Task deletion works")
    except Exception as e:
        print(f"[FAIL] Task deletion failed: {e}")
        return False

    # Test invalid ID handling
    try:
        task = tm.get_task(999)
        assert task is None
        updated = tm.update_task(999, "test")
        assert updated is None
        deleted = tm.delete_task(999)
        assert deleted == False
        toggled = tm.toggle_task_completion(999)
        assert toggled is None
        print("[PASS] Invalid ID handling works")
    except Exception as e:
        print(f"[FAIL] Invalid ID handling failed: {e}")
        return False

    return True

def run_manual_tests():
    """Run manual validation tests."""
    print("\n" + "="*50)
    print("MANUAL FUNCTIONALITY TESTS")
    print("="*50)

    print("\n1. Testing Task Creation...")
    success1 = test_task_creation()

    print("\n2. Testing TaskManager...")
    success2 = test_task_manager()

    print("\n" + "="*50)
    if success1 and success2:
        print("[PASS] ALL TESTS PASSED!")
        print("The console todo application is working correctly.")
    else:
        print("[FAIL] SOME TESTS FAILED!")
        print("There are issues with the implementation.")
    print("="*50)

    return success1 and success2

if __name__ == "__main__":
    run_manual_tests()