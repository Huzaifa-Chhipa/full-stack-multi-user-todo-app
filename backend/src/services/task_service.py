from typing import List, Optional
from sqlmodel import Session, select
from ..models import Task, TaskCreate, TaskUpdate


def create_task(db_session: Session, task: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for the specified user.

    Args:
        db_session: Database session
        task: TaskCreate object containing task details
        user_id: ID of the user creating the task

    Returns:
        Created Task object
    """
    # Create task with user_id directly
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=getattr(task, 'completed', False),  # Use getattr for safer access
        user_id=user_id
    )

    db_session.add(db_task)
    db_session.commit()

    # Refresh to get the generated ID
    db_session.refresh(db_task)

    # Verify that the task has been created with a valid ID
    if db_task.id is None:
        # Force refresh to ensure the ID is populated
        db_session.refresh(db_task)

    # Final check - if still no ID, raise an error
    if db_task.id is None:
        raise ValueError("Task was not created with a valid ID - check database connection and table structure")

    return db_task


def get_tasks(db_session: Session, user_id: str, completed: Optional[bool] = None) -> List[Task]:
    """
    Get tasks for a specific user with optional completion status filter.

    Args:
        db_session: Database session
        user_id: ID of the user whose tasks to retrieve
        completed: Optional filter for completion status (None=all, False=pending, True=completed)

    Returns:
        List of Task objects
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    return db_session.exec(query).all()


def get_task(db_session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user.

    Args:
        db_session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task object if found, None otherwise
    """
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return db_session.exec(query).first()


def update_task(db_session: Session, task_id: int, user_id: str, task_update: dict) -> Optional[Task]:
    """
    Update a task with the provided data.

    Args:
        db_session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        task_update: Dictionary containing fields to update

    Returns:
        Updated Task object if successful, None if task not found
    """
    task = get_task(db_session, task_id, user_id)
    if not task:
        return None

    # Update task attributes
    for field, value in task_update.items():
        if hasattr(task, field):
            setattr(task, field, value)

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    return task


def delete_task(db_session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task by ID for a specific user.

    Args:
        db_session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task

    Returns:
        True if task was deleted, False if not found
    """
    task = get_task(db_session, task_id, user_id)
    if not task:
        return False

    db_session.delete(task)
    db_session.commit()

    return True