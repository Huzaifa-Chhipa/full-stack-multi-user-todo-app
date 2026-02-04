from typing import Dict, Any, List
import json
from sqlmodel import create_engine, Session, select
from .models import Task, User
from .db import get_sync_session
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost/todo_db")
engine = create_engine(DATABASE_URL.replace('+asyncpg', '+psycopg2'))

def add_task_function(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Function to add a new task to the user's todo list.
    Expected params: {'user_id': str, 'title': str, 'description': str}
    """
    try:
        with Session(engine) as session:
            # Create new task
            new_task = Task(
                title=params['title'],
                description=params.get('description'),
                completed=False,
                user_id=params['user_id']
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return {
                "success": True,
                "task_id": new_task.id,
                "message": f"Task '{new_task.title}' added successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def delete_task_function(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Function to delete a task from the user's todo list.
    Expected params: {'user_id': str, 'task_id': int}
    """
    try:
        with Session(engine) as session:
            # Find task by ID and user
            statement = select(Task).where(Task.id == params['task_id'], Task.user_id == params['user_id'])
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found or doesn't belong to user"
                }

            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": f"Task {params['task_id']} deleted successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def complete_task_function(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Function to mark a task as completed.
    Expected params: {'user_id': str, 'task_id': int}
    """
    try:
        with Session(engine) as session:
            # Find task by ID and user
            statement = select(Task).where(Task.id == params['task_id'], Task.user_id == params['user_id'])
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found or doesn't belong to user"
                }

            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Task {params['task_id']} marked as completed"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_tasks_function(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Function to list all tasks for a user.
    Expected params: {'user_id': str}
    """
    try:
        with Session(engine) as session:
            # Get all tasks for the user
            statement = select(Task).where(Task.user_id == params['user_id'])
            tasks = session.exec(statement).all()

            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })

            return {
                "success": True,
                "tasks": task_list,
                "total_count": len(task_list)
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def update_task_function(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Function to update a task.
    Expected params: {'user_id': str, 'task_id': int, 'title': str, 'description': str, 'completed': bool}
    """
    try:
        with Session(engine) as session:
            # Find task by ID and user
            statement = select(Task).where(Task.id == params['task_id'], Task.user_id == params['user_id'])
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found or doesn't belong to user"
                }

            # Update fields if provided
            if 'title' in params:
                task.title = params['title']
            if 'description' in params:
                task.description = params.get('description')
            if 'completed' in params:
                task.completed = params['completed']

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Task {params['task_id']} updated successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Function schemas for OpenAI
FUNCTION_SCHEMAS = [
    {
        "name": "add_task",
        "description": "Add a new task to the user's todo list",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "ID of the user"},
                "title": {"type": "string", "description": "Title of the task"},
                "description": {"type": "string", "description": "Description of the task (optional)"}
            },
            "required": ["user_id", "title"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task from the user's todo list",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "ID of the user"},
                "task_id": {"type": "integer", "description": "ID of the task to delete"}
            },
            "required": ["user_id", "task_id"]
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "ID of the user"},
                "task_id": {"type": "integer", "description": "ID of the task to complete"}
            },
            "required": ["user_id", "task_id"]
        }
    },
    {
        "name": "list_tasks",
        "description": "List all tasks for a user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "ID of the user"}
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "update_task",
        "description": "Update a task",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "ID of the user"},
                "task_id": {"type": "integer", "description": "ID of the task to update"},
                "title": {"type": "string", "description": "New title (optional)"},
                "description": {"type": "string", "description": "New description (optional)"},
                "completed": {"type": "boolean", "description": "New completion status (optional)"}
            },
            "required": ["user_id", "task_id"]
        }
    }
]


# Function mapping
FUNCTION_MAP = {
    "add_task": add_task_function,
    "delete_task": delete_task_function,
    "complete_task": complete_task_function,
    "list_tasks": list_tasks_function,
    "update_task": update_task_function
}