import asyncio
import os
from typing import Dict, Any
from dotenv import load_dotenv
from sqlmodel import Session

from .tools.task_tools import (
    add_task, list_tasks, complete_task, delete_task, update_task,
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest, DeleteTaskRequest, UpdateTaskRequest
)

# Load environment variables
load_dotenv()


class TodoAgent:
    """
    AI agent for managing todo tasks using natural language.
    For now, this uses a simpler approach without openai-agents due to compatibility issues with Gemini API.
    """

    def __init__(self, db_session: Session, user_id: str):
        self.db_session = db_session
        self.user_id = user_id

        # Initialize Gemini API key
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

    async def process_message(self, message: str) -> str:
        """
        Process a user message and return the AI response.
        This is a simplified version that detects basic commands and executes them.

        Args:
            message: User's input message

        Returns:
            AI's response to the user
        """
        try:
            # Convert message to lowercase for easier parsing
            lower_message = message.lower().strip()

            # Detect commands - order matters: more specific commands first
            if any(word in lower_message for word in ["delete", "remove", "cancel"]):
                return await self._handle_delete_task(message)
            elif any(word in lower_message for word in ["complete", "done", "finish", "mark as"]):
                return await self._handle_complete_task(message)
            elif any(word in lower_message for word in ["update", "change", "modify", "edit"]):
                return await self._handle_update_task(message)
            elif any(word in lower_message for word in ["list", "show", "display", "my tasks", "what"]):
                return await self._handle_list_tasks(message)
            elif any(word in lower_message for word in ["add", "create", "new task", "make task"]):
                return await self._handle_add_task(message)
            else:
                # For other messages, return a helpful response
                return f"I understand you said: '{message}'. I can help you manage your tasks. Try commands like 'Add a task to buy groceries', 'Show me my tasks', 'Mark task 1 as complete', or 'Delete task 2'."

        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return f"Sorry, I encountered an error processing your request: {str(e)}. Please try again."

    async def _handle_add_task(self, message: str) -> str:
        """Handle adding a new task based on the user's message."""
        try:
            # Extract the task title from the message
            import re

            # Try to extract the task title after common phrases
            patterns = [
                # English patterns
                r"(?:add|create|make|task add kro|kro|krna|bnana)\s+(?:a\s+)?(?:task|todo|kam|kaam|karne|kar)\s+(?:to|ke\s+naam|par|pe|per|for|liye|ke liye|naam|name)\s+(.+?)(?:\.|$|,|!|\?)",
                r"(?:add|create|make|task add kro|kro|krna|bnana)\s+(?:a\s+)?(?:task|todo|kam|kaam|karne|kar)\s+(?:to|ke\s+naam|par|pe|per|for|liye|ke liye|naam|name)\s+(.+?)(?:\s+please|\s+now|\s+kro|\s+krdo|\s+de|s+do)?(?:\.|$|,|!|\?)",
                # Patterns for "task add kro name banana" type
                r"task\s+add\s+kro\s+(?:name|naam|title|shirshak)\s+(.+?)(?:\.|$|,|!|\?)",
                r"task\s+add\s+kro\s+(.+?)(?:\.|$|,|!|\?)",
                # General patterns
                r"(?:add|create|make)\s+(?:a\s+)?(?:task|todo)\s+to\s+(.+?)(?:\.|$|,|!|\?)",
                r"(?:add|create|make)\s+(?:a\s+)?(?:task|todo)\s+(.+?)(?:\.|$|,|!|\?)",
                # Fallback: take the entire message but remove common command words
                r"^(.+)$"
            ]

            title = ""
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    extracted = match.group(1).strip()
                    # Remove common filler words that might remain
                    extracted = re.sub(r"\b(?:please|now|kro|krdo|de|do|kar|karne|liye|ke liye|ke naam|naam)\b", "", extracted, flags=re.IGNORECASE).strip()
                    title = extracted.strip()
                    if title:
                        break

            # If still no title or it's too generic, use a fallback
            if not title or title.lower() in ["task", "a task", "the task", "kro", "krna"]:
                # Remove common command words from the original message to get the actual task
                title = re.sub(r"\b(?:task|add|create|make|kro|krna|bnana|ke naam|naam|name|title|shirshak|please|now|de|do|kar|karne|liye|ke liye|par|pe|per|to|for)\b", "", message, flags=re.IGNORECASE).strip()

            if not title or len(title) < 2:
                return "Please provide a more descriptive task title. For example: 'Add a task to buy groceries' or 'Task add kro name grocery shopping'."

            # Create the request
            request = AddTaskRequest(
                title=title[:200],  # Limit to 200 chars
                description=None,
                user_id=self.user_id
            )

            # Execute the tool
            result = add_task(request, self.db_session)

            return f"Great! I've added the task '{result.title}' (ID: {result.task_id}) to your list."

        except Exception as e:
            print(f"Error in _handle_add_task: {str(e)}")
            return f"Sorry, I couldn't add that task: {str(e)}"

    async def _handle_list_tasks(self, message: str) -> str:
        """Handle listing tasks based on the user's message."""
        try:
            # Determine if user wants all, pending, or completed tasks
            status_filter = "all"
            lower_msg = message.lower()
            if "pending" in lower_msg or "incomplete" in lower_msg:
                status_filter = "pending"
            elif "completed" in lower_msg or "done" in lower_msg:
                status_filter = "completed"

            # Create the request
            request = ListTasksRequest(
                user_id=self.user_id,
                status_filter=status_filter
            )

            # Execute the tool
            result = list_tasks(request, self.db_session)

            if not result.tasks:
                if status_filter == "all":
                    return "You don't have any tasks yet. Try adding one!"
                elif status_filter == "pending":
                    return "You don't have any pending tasks. Great job!"
                else:  # completed
                    return "You haven't completed any tasks yet."

            # Format the response
            task_list = []
            for task in result.tasks[:10]:  # Limit to first 10 tasks to avoid too much text
                status = "✓" if task["completed"] else "○"
                task_list.append(f"{status} {task['id']}. {task['title']}")

            if len(result.tasks) > 10:
                task_list.append(f"... and {len(result.tasks) - 10} more tasks")

            if status_filter == "all":
                return f"You have {result.total_count} tasks:\n" + "\n".join(task_list)
            elif status_filter == "pending":
                return f"You have {result.total_count} pending tasks:\n" + "\n".join(task_list)
            else:  # completed
                return f"You have completed {result.total_count} tasks:\n" + "\n".join(task_list)

        except Exception as e:
            print(f"Error in _handle_list_tasks: {str(e)}")
            return f"Sorry, I couldn't retrieve your tasks: {str(e)}"

    async def _handle_complete_task(self, message: str) -> str:
        """Handle completing a task based on the user's message."""
        try:
            import re

            # First, try to extract task ID from the message
            # Look for patterns like "task 1", "task #1", "#1", etc.
            task_id = None
            patterns = [
                r"task\s+#?(\d+)",
                r"#(\d+)",
                r"task\s+(\d+)"
            ]

            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    task_id = int(match.group(1))
                    break

            # If no task ID found, try to find task by name/title
            if task_id is None:
                # Extract potential task title from message
                # Look for patterns like "complete [task title]", "finish [task title]", etc.
                complete_patterns = [
                    r"(?:complete|finish|done|mark as complete|mark as done)\s+(?:the\s+)?(.+?)(?:\s+task|\s*$|\.|$)",
                ]

                task_title = None
                for pattern in complete_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        task_title = match.group(1).strip()
                        break

                if task_title:
                    # Find task by title
                    from .tools.task_tools import ListTasksRequest
                    request = ListTasksRequest(user_id=self.user_id)
                    result = list_tasks(request, self.db_session)

                    # Find task that matches the title (case-insensitive, partial match)
                    matched_task = None
                    for task in result.tasks:
                        if task_title.lower() in task['title'].lower():
                            matched_task = task
                            break

                    if matched_task:
                        task_id = matched_task['id']
                    else:
                        return f"Sorry, I couldn't find a task containing '{task_title}'. Here are your tasks:\n" + \
                               "\n".join([f"- {task['title']} (ID: {task['id']})" for task in result.tasks])
                else:
                    # If no specific task ID or title found, try to interpret the message differently
                    return "Please specify which task to complete. For example: 'Mark task 1 as complete', 'Complete the grocery task', or 'Finish dentist appointment'."

            # Create the request
            request = CompleteTaskRequest(
                task_id=task_id,
                user_id=self.user_id
            )

            # Execute the tool
            result = complete_task(request, self.db_session)

            if result.status == "not_found":
                return f"Sorry, I couldn't find task #{task_id}. Please check the task number."
            elif result.status == "already_completed":
                return f"Task #{task_id} ('{result.title}') is already marked as completed!"
            else:
                return f"Great! I've marked task #{task_id} ('{result.title}') as completed."

        except ValueError:
            return "Please specify a valid task number. For example: 'Mark task 1 as complete'."
        except Exception as e:
            print(f"Error in _handle_complete_task: {str(e)}")
            return f"Sorry, I couldn't complete that task: {str(e)}"

    async def _handle_delete_task(self, message: str) -> str:
        """Handle deleting a task based on the user's message."""
        try:
            import re

            # First, try to extract task ID from the message
            task_id = None
            patterns = [
                r"(?:remove|delete|cancel|get rid of)\s+task\s+#?(\d+)",
                r"(?:remove|delete|cancel|get rid of)\s+#?(\d+)\s+task",
                r"task\s+#?(\d+)\s+(?:please|now|)",
                r"#(\d+)",
                r"task\s+#?(\d+)"
            ]

            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    task_id = int(match.group(1))
                    break

            # If no task ID found, try to find task by name/title
            if task_id is None:
                # Extract potential task title from message
                # Look for patterns like "delete [task title]", "remove [task title]", etc.
                # Including Hindi/Urdu constructs like "ke naam se", "wlaa", etc.
                delete_patterns = [
                    # English patterns
                    r"(?:remove|delete|cancel|get rid of|eliminate)\s+(?:the\s+)?(.+?)(?:\s+task|\s*$|\.|$)",
                    # Specific pattern for "banana ke naam se jo task he usko delete kro"
                    r"(\w+)\s+ke\s+naam\s+se\s+jo\s+task\s+he\s+usko\s+delete\s+kro",
                    # Pattern for "banana ke naam se"
                    r"(\w+)\s+ke\s+naam\s+se",
                    # Pattern for "[task_name] ko delete kro"
                    r"(\w+)\s+ko\s+(?:delete|remove|cancel)\s+(?:kro|krdo|kar)",
                    # Pattern for "task delete kro [task_name] wlaa"
                    r"task\s+(?:delete|remove)\s+kro\s+(\w+)\s+wlaa",
                    # Pattern for "task delete kro [task_name] ka"
                    r"task\s+(?:delete|remove)\s+kro\s+(.+?)\s+ka",
                    # Pattern for "task delete kro [task_name]"
                    r"task\s+(?:delete|remove)\s+kro\s+(\w+)",
                    # Pattern for "delete kro [task_name]"
                    r"(?:delete|remove)\s+kro\s+(\w+)",
                    # Pattern for "[task_name] ka"
                    r"(.+?)\s+ka\s+(?:task|kam|kaam)",
                ]

                task_title = None
                for pattern in delete_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        task_title = match.group(1).strip()
                        break

                if task_title:
                    # Find task by title
                    from .tools.task_tools import ListTasksRequest
                    request = ListTasksRequest(user_id=self.user_id)
                    result = list_tasks(request, self.db_session)

                    # Find task that matches the title (case-insensitive, partial match)
                    matched_task = None
                    for task in result.tasks:
                        if task_title.lower() in task['title'].lower():
                            matched_task = task
                            break

                    if matched_task:
                        task_id = matched_task['id']
                    else:
                        return f"Sorry, I couldn't find a task containing '{task_title}'. Here are your tasks:\n" + \
                               "\n".join([f"- {task['title']} (ID: {task['id']})" for task in result.tasks])
                else:
                    return "Please specify which task to delete. For example: 'Delete the grocery task', 'Remove task 1', or 'Cancel dentist appointment'."

            # Create the request
            request = DeleteTaskRequest(
                task_id=task_id,
                user_id=self.user_id
            )

            # Execute the tool
            result = delete_task(request, self.db_session)

            if result.status == "not_found":
                return f"Sorry, I couldn't find task #{task_id}. Please check the task number."
            else:
                return f"Task #{task_id} has been deleted successfully."

        except ValueError:
            return "Please specify a valid task number. For example: 'Delete task 1'."
        except Exception as e:
            print(f"Error in _handle_delete_task: {str(e)}")
            return f"Sorry, I couldn't delete that task: {str(e)}"

    async def _handle_update_task(self, message: str) -> str:
        """Handle updating a task based on the user's message."""
        try:
            import re

            # Try to extract task ID and new title/description
            task_id = None
            new_title = None

            # Pattern to match "update task X to Y" or "change task X to Y"
            pattern = r"(?:update|change|modify)\s+task\s+#?(\d+)\s+(?:to|with title|and title)\s+(.+?)(?:\.|$)"
            match = re.search(pattern, message, re.IGNORECASE)

            if match:
                task_id = int(match.group(1))
                new_title = match.group(2).strip()

            # If no task ID found, try to find task by name/title
            if task_id is None:
                # Pattern to match "update [task name] to [new title]"
                update_patterns = [
                    r"(?:update|change|modify)\s+(?:the\s+)?(.+?)\s+(?:to|with)\s+(.+?)(?:\.|$)",
                ]

                task_title = None
                new_title = None
                for pattern in update_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        task_title = match.group(1).strip()
                        new_title = match.group(2).strip()
                        break

                if task_title and new_title:
                    # Find task by title
                    from .tools.task_tools import ListTasksRequest
                    request = ListTasksRequest(user_id=self.user_id)
                    result = list_tasks(request, self.db_session)

                    # Find task that matches the title (case-insensitive, partial match)
                    matched_task = None
                    for task in result.tasks:
                        if task_title.lower() in task['title'].lower():
                            matched_task = task
                            break

                    if matched_task:
                        task_id = matched_task['id']
                    else:
                        return f"Sorry, I couldn't find a task containing '{task_title}'. Here are your tasks:\n" + \
                               "\n".join([f"- {task['title']} (ID: {task['id']})" for task in result.tasks])
                else:
                    return "Please specify which task to update and the new title. For example: 'Update the grocery task to buy vegetables', 'Change task 1 to Call dentist', or 'Modify dentist appointment to tomorrow'."

            if task_id is None or new_title is None:
                return "Please specify which task to update and the new title. For example: 'Update task 1 to Call dentist' or 'Change task 2 to Buy milk'."

            # Create the request
            request = UpdateTaskRequest(
                task_id=task_id,
                user_id=self.user_id,
                title=new_title[:200]  # Limit to 200 chars
            )

            # Execute the tool
            result = update_task(request, self.db_session)

            if result.status == "not_found":
                return f"Sorry, I couldn't find task #{task_id}. Please check the task number."
            else:
                return f"Task #{task_id} has been updated successfully to '{result.title}'."

        except ValueError:
            return "Please specify a valid task number and new title. For example: 'Update task 1 to New title'."
        except Exception as e:
            print(f"Error in _handle_update_task: {str(e)}")
            return f"Sorry, I couldn't update that task: {str(e)}"


async def run_todo_agent_example():
    """
    Example of how to run the todo agent.
    """
    # This would typically be called with a real database session
    # For now, this is just a demonstration
    print("Todo agent example would run here.")


if __name__ == "__main__":
    # Example usage
    asyncio.run(run_todo_agent_example())