from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from src.models import TaskCreate, Task
from src.services.task_service import create_task as create_task_service
from sqlmodel import select
from sqlmodel import Session


class AddTaskRequest(BaseModel):
    """Request to add a new task to the user's todo list."""
    title: str = Field(..., description="Title of the task (1-200 characters)", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Optional description of the task (max 1000 characters)", max_length=1000)
    user_id: str = Field(..., description="ID of the user creating the task")


class AddTaskResponse(BaseModel):
    """Response after adding a task."""
    task_id: int = Field(..., description="ID of the created task")
    status: str = Field(..., description="Status of the operation ('created')")
    title: str = Field(..., description="Title of the created task")


def add_task(request: AddTaskRequest, db_session: Session) -> AddTaskResponse:
    """
    Add a new task to the user's todo list using the task service.

    Args:
        request: Contains the task details and user_id
        db_session: Database session to use for the operation

    Returns:
        AddTaskResponse with the created task details
    """
    # Create a TaskCreate object from the request
    task_create_data = TaskCreate(
        title=request.title,
        description=request.description,
        completed=False  # New tasks are not completed by default
    )

    # Use the existing task service to create the task
    task = create_task_service(db_session, task_create_data, user_id=request.user_id)

    # Ensure the task has all required fields before creating response
    if task.id is None:
        raise ValueError("Task was not created with a valid ID")

    return AddTaskResponse(
        task_id=task.id,
        status="created",
        title=task.title
    )


class ListTasksRequest(BaseModel):
    """Request to list tasks for a user."""
    user_id: str = Field(..., description="ID of the user whose tasks to list")
    status_filter: Optional[str] = Field("all", description="Filter tasks by status: 'all', 'pending', or 'completed'")


class ListTasksResponse(BaseModel):
    """Response containing the user's tasks."""
    tasks: list[Dict[str, Any]] = Field(..., description="List of tasks")
    total_count: int = Field(..., description="Total number of tasks returned")


from src.services.task_service import get_tasks as get_tasks_service


def list_tasks(request: ListTasksRequest, db_session: Session) -> ListTasksResponse:
    """
    List tasks for the user with optional status filtering.

    Args:
        request: Contains the user_id and optional status filter
        db_session: Database session to use for the operation

    Returns:
        ListTasksResponse with the user's tasks
    """
    # Map status filter to the format expected by get_tasks_service
    status = None
    if request.status_filter == "pending":
        status = False
    elif request.status_filter == "completed":
        status = True

    # Get tasks from the service
    tasks = get_tasks_service(db_session, user_id=request.user_id, completed=status)

    # Convert tasks to dictionaries
    tasks_dict = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
        tasks_dict.append(task_dict)

    return ListTasksResponse(
        tasks=tasks_dict,
        total_count=len(tasks_dict)
    )


class CompleteTaskRequest(BaseModel):
    """Request to mark a task as completed."""
    task_id: int = Field(..., description="ID of the task to complete")
    user_id: str = Field(..., description="ID of the user who owns the task")


class CompleteTaskResponse(BaseModel):
    """Response after completing a task."""
    task_id: int = Field(..., description="ID of the completed task")
    status: str = Field(..., description="Status of the operation ('completed' or 'already_completed')")
    title: str = Field(..., description="Title of the completed task")


from src.services.task_service import get_task as get_task_service, update_task as update_task_service


def complete_task(request: CompleteTaskRequest, db_session: Session) -> CompleteTaskResponse:
    """
    Mark a task as completed.

    Args:
        request: Contains the task_id and user_id
        db_session: Database session to use for the operation

    Returns:
        CompleteTaskResponse with the updated task details
    """
    # First, verify the task exists and belongs to the user
    task = get_task_service(db_session, task_id=request.task_id, user_id=request.user_id)
    if not task:
        raise ValueError(f"Task with ID {request.task_id} not found or doesn't belong to user")

    if task.completed:
        return CompleteTaskResponse(
            task_id=task.id,
            status="already_completed",
            title=task.title
        )

    # Update the task to mark as completed
    task_update_data = {"completed": True}
    updated_task = update_task_service(db_session, task_id=request.task_id, user_id=request.user_id, task_update=task_update_data)

    return CompleteTaskResponse(
        task_id=updated_task.id,
        status="completed",
        title=updated_task.title
    )


class DeleteTaskRequest(BaseModel):
    """Request to delete a task."""
    task_id: int = Field(..., description="ID of the task to delete")
    user_id: str = Field(..., description="ID of the user who owns the task")


class DeleteTaskResponse(BaseModel):
    """Response after deleting a task."""
    task_id: int = Field(..., description="ID of the deleted task")
    status: str = Field(..., description="Status of the operation ('deleted' or 'not_found')")


from src.services.task_service import delete_task as delete_task_service


def delete_task(request: DeleteTaskRequest, db_session: Session) -> DeleteTaskResponse:
    """
    Delete a task from the user's todo list.

    Args:
        request: Contains the task_id and user_id
        db_session: Database session to use for the operation

    Returns:
        DeleteTaskResponse confirming the deletion
    """
    try:
        # Attempt to delete the task
        success = delete_task_service(db_session, task_id=request.task_id, user_id=request.user_id)

        if success:
            return DeleteTaskResponse(
                task_id=request.task_id,
                status="deleted"
            )
        else:
            return DeleteTaskResponse(
                task_id=request.task_id,
                status="not_found"
            )
    except Exception:
        # If an exception occurs (like task not found), return not_found status
        return DeleteTaskResponse(
            task_id=request.task_id,
            status="not_found"
        )


class UpdateTaskRequest(BaseModel):
    """Request to update a task."""
    task_id: int = Field(..., description="ID of the task to update")
    user_id: str = Field(..., description="ID of the user who owns the task")
    title: Optional[str] = Field(None, description="New title (1-200 characters)", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="New description (max 1000 characters)", max_length=1000)


class UpdateTaskResponse(BaseModel):
    """Response after updating a task."""
    task_id: int = Field(..., description="ID of the updated task")
    status: str = Field(..., description="Status of the operation ('updated' or 'not_found')")
    title: str = Field(..., description="Updated title of the task")


def update_task(request: UpdateTaskRequest, db_session: Session) -> UpdateTaskResponse:
    """
    Update a task's title or description.

    Args:
        request: Contains the task_id, user_id, and optional fields to update
        db_session: Database session to use for the operation

    Returns:
        UpdateTaskResponse with the updated task details
    """
    # Verify the task exists and belongs to the user
    task = get_task_service(db_session, task_id=request.task_id, user_id=request.user_id)
    if not task:
        return UpdateTaskResponse(
            task_id=request.task_id,
            status="not_found",
            title=""
        )

    # Prepare update data
    update_data = {}
    if request.title is not None:
        update_data["title"] = request.title
    if request.description is not None:
        update_data["description"] = request.description

    # If no updates were requested, return the current task
    if not update_data:
        return UpdateTaskResponse(
            task_id=task.id,
            status="updated",
            title=task.title
        )

    # Update the task
    updated_task = update_task_service(db_session, task_id=request.task_id, user_id=request.user_id, task_update=update_data)

    return UpdateTaskResponse(
        task_id=updated_task.id,
        status="updated",
        title=updated_task.title
    )