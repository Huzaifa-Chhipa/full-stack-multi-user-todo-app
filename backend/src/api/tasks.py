"""
Task API endpoints for the Todo Application
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from ..db import get_session
from ..models.task import Task, TaskRead, TaskCreate, TaskUpdate
from ..auth import get_current_user, verify_user_owns_resource

router = APIRouter()

@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new task for the authenticated user"""
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create the task with the authenticated user's ID
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.get("/tasks", response_model=List[TaskRead])
async def read_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all tasks for the authenticated user"""
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    # Query tasks for the authenticated user, ordered by created_at descending
    from sqlalchemy import select
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    result = await session.execute(statement)
    tasks = result.scalars().all()

    return tasks


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific task by ID for the authenticated user"""
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    from sqlalchemy import select
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a specific task by ID for the authenticated user"""
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    from sqlalchemy import select
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    result = await session.execute(statement)
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with provided values
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    from datetime import datetime
    db_task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a specific task by ID for the authenticated user"""
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete tasks for this user"
        )

    from sqlalchemy import select
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    result = await session.execute(statement)
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await session.delete(db_task)
    await session.commit()

    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Toggle the completion status of a specific task for the authenticated user"""
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    from sqlalchemy import select
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    result = await session.execute(statement)
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status
    db_task.completed = not db_task.completed

    # Update the updated_at timestamp
    from datetime import datetime
    db_task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(db_task)

    return db_task