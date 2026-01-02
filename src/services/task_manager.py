"""
TaskManager service for the console todo application.

This module manages in-memory storage of tasks with operations to add, retrieve,
update, delete, and toggle completion status of tasks.
"""

from typing import List, Optional
from src.models.task import Task


class TaskManager:
    """
    Manages in-memory collection of tasks with various operations.
    """

    def __init__(self):
        """
        Initialize the TaskManager with an empty task collection.
        """
        self._tasks = {}  # Dictionary to store tasks with ID as key
        self._next_id = 1  # Auto-increment ID counter

    def _get_next_id(self) -> int:
        """
        Get the next available ID and increment the counter.

        Returns:
            int: The next available ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with auto-incremented ID.

        Args:
            title: Task title (must be non-empty)
            description: Optional task description

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If title is empty
        """
        # Validate title is non-empty (this is also checked in Task constructor)
        if not title or not title.strip():
            raise ValueError("Title must be non-empty")

        task_id = self._get_next_id()
        task = Task(task_id, title, description, completed=False)
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks sorted by ID.

        Returns:
            List[Task]: List of all tasks sorted by ID in ascending order
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional, keeps existing if None)
            description: New description (optional, keeps existing if None)

        Returns:
            Task: Updated task if successful, None if task doesn't exist

        Raises:
            ValueError: If new title is empty
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        # Use existing values if new values are not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        # Validate new title if it's being updated
        if title is not None and (not title or not title.strip()):
            raise ValueError("Title must be non-empty")

        # Update task attributes
        task.title = new_title.strip() if new_title else ""
        task.description = new_description.strip() if new_description else ""

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task didn't exist
        """
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            Task: Updated task if successful, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        task.completed = not task.completed
        return task

    def get_next_id(self) -> int:
        """
        Get the next available ID without incrementing the counter.
        Used for validation purposes.

        Returns:
            int: The next available ID
        """
        return self._next_id