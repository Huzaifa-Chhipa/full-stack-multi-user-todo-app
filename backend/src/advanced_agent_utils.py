import os
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from typing import List, Dict, Any
from pydantic import BaseModel
from .tools.task_tools import (
    add_task, list_tasks, complete_task, delete_task, update_task,
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest, DeleteTaskRequest, UpdateTaskRequest
)
from sqlmodel import Session
import re


# Load environment variables
load_dotenv()

# Disable tracing
set_tracing_disabled(disabled=True)


class GeminiClient:
    """
    Client wrapper for Google's Gemini API using openai-agents library.
    """

    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Configure the AsyncOpenAI client with Gemini's base URL
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = "gemini-2.0-flash"

    def get_client(self):
        return self.client

    def get_model(self):
        return self.model


class AdvancedNLPProcessor:
    """
    Advanced processor for natural language commands in English, Hindi, Urdu, and mixed language
    """

    def __init__(self, db_session: Session, user_id: str):
        self.db_session = db_session
        self.user_id = user_id

    def detect_intent(self, text: str) -> str:
        """
        Detect the user's intent regardless of language or phrasing
        """
        text_lower = text.lower()

        # Keywords for different intents
        add_keywords = [
            'task add kro', 'add task', 'create task', 'bnana', 'bnaye',
            'add kro', 'krdo task', 'task do', 'task bnana', 'add krdo'
        ]

        delete_keywords = [
            'task delete kro', 'delete task', 'remove task', 'hatao', 'nikalo',
            'delete kro', 'hatana', 'task hatao', 'task nikal', 'hata do'
        ]

        complete_keywords = [
            'complete task', 'finish task', 'done task', 'ho gya', 'ho gaya',
            'complete kro', 'kr diya', 'kar diya', 'task complete', 'task done'
        ]

        list_keywords = [
            'my tasks', 'all tasks', 'show tasks', 'list tasks', 'tasks dikhao',
            'mere tasks', 'task list', 'sab tasks', 'show me', 'kya kaam hai'
        ]

        # Check for intents
        for keyword in add_keywords:
            if keyword in text_lower:
                return 'add'

        for keyword in delete_keywords:
            if keyword in text_lower:
                return 'delete'

        for keyword in complete_keywords:
            if keyword in text_lower:
                return 'complete'

        for keyword in list_keywords:
            if keyword in text_lower:
                return 'list'

        # Default to add if no specific intent detected
        return 'add'

    def extract_task_name(self, text: str) -> str:
        """
        Extract task name from any kind of expression
        """
        text_lower = text.lower()

        # Patterns to extract task name
        patterns = [
            # Pattern: "task add kro name X" or "task add kro X"
            r'(?:task\s+add\s+kro|add\s+kro|task\s+bnana|bnana)\s+(?:name\s+)?(\w+)',

            # Pattern: "task delete kro X wlaa/ka" or "task delete kro X"
            r'(?:task\s+delete\s+kro|delete\s+kro|task\s+hatao|hatao)\s+(\w+)\s*(?:wlaa|wala|vala|ka)?',

            # Pattern: "X ke naam se jo task he usko delete kro"
            r'(\w+)\s+ke\s+naam\s+se\s+jo\s+task\s+he\s+usko\s+(?:delete|remove|hatao)\s+kro',

            # Pattern: "X ko delete kro" or "X ko complete kro"
            r'(\w+)\s+ko\s+(?:delete|remove|complete|done|ho\s+gaya|hatao)\s+(?:kro|krdo|kar)',

            # Pattern: "X ka task"
            r'(\w+)\s+ka\s+(?:task|kam|kaam)',

            # General patterns
            r'(?:to|for|par|pe)\s+(\w+)',  # "add task to X"
            r'(\w+)\s+(?:task|kam|kaam)',  # "X task"
        ]

        # Try each pattern
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                task_name = match.group(1)
                # Clean up the extracted name
                task_name = re.sub(r'\b(?:kro|krdo|kar|naam|se|jo|task|he|usko|ke|ko|wlaa|wala|vala|ka|par|pe|to|for|the|a|an|hai|krna|karna|krdo|karne)\b', '', task_name).strip()
                if task_name and len(task_name) >= 1:
                    return task_name

        # If no pattern matches, try to extract any meaningful word
        words = re.findall(r'\b\w{2,}\b', text_lower)
        for word in words:
            if word not in ['task', 'tasks', 'kro', 'krdo', 'kar', 'ke', 'ko', 'naam', 'se', 'jo', 'he', 'usko', 'ka', 'ko', 'wlaa', 'wala', 'vala', 'par', 'pe', 'to', 'for', 'the', 'a', 'an', 'to', 'for', 'on', 'at', 'in', 'is', 'are', 'was', 'were', 'mera', 'mere', 'mujhe', 'mai', 'main', 'maine', 'ne', 'krna', 'karna', 'krdo', 'karne']:
                return word

        return ""

    def find_task_by_name(self, task_name: str) -> Dict:
        """
        Find a task by name from the user's task list
        """
        try:
            # Create request to list tasks
            request = ListTasksRequest(user_id=self.user_id)
            result = list_tasks(request, self.db_session)

            # Search for the task with the matching name
            for task in result.tasks:
                if task_name.lower() in task['title'].lower():
                    return {
                        'found': True,
                        'task_id': task['id'],
                        'title': task['title']
                    }

            # If not found, return available tasks
            return {
                'found': False,
                'available_tasks': [t['title'] for t in result.tasks],
                'message': f"Could not find a task containing '{task_name}'. Available tasks: {', '.join([t['title'] for t in result.tasks])}"
            }
        except Exception as e:
            return {
                'found': False,
                'error': str(e)
            }

    def process_command(self, text: str) -> Dict:
        """
        Process any command and execute appropriate action
        """
        intent = self.detect_intent(text)
        task_name = self.extract_task_name(text)

        if intent == 'add':
            if task_name:
                try:
                    # Create add task request
                    request = AddTaskRequest(
                        title=task_name,
                        description=None,
                        user_id=self.user_id
                    )
                    result = add_task(request, self.db_session)
                    return {
                        'success': True,
                        'message': f"Great! I've added the task '{result.title}' (ID: {result.task_id}) to your list."
                    }
                except Exception as e:
                    return {
                        'success': False,
                        'message': f"Sorry, I couldn't add that task: {str(e)}"
                    }
            else:
                return {
                    'success': False,
                    'message': "Please specify what task you'd like to add."
                }

        elif intent == 'delete':
            if task_name:
                # Find the task first
                find_result = self.find_task_by_name(task_name)

                if find_result['found']:
                    try:
                        # Delete the found task
                        request = DeleteTaskRequest(
                            task_id=find_result['task_id'],
                            user_id=self.user_id
                        )
                        result = delete_task(request, self.db_session)

                        if result.status == "not_found":
                            return {
                                'success': False,
                                'message': f"Sorry, I couldn't find that task to delete."
                            }
                        else:
                            return {
                                'success': True,
                                'message': f"Task '{find_result['title']}' has been deleted successfully."
                            }
                    except Exception as e:
                        return {
                            'success': False,
                            'message': f"Sorry, I couldn't delete that task: {str(e)}"
                        }
                else:
                    return {
                        'success': False,
                        'message': find_result.get('message', 'Could not find the specified task.')
                    }
            else:
                # If no specific task name, list tasks and ask
                try:
                    request = ListTasksRequest(user_id=self.user_id)
                    result = list_tasks(request, self.db_session)
                    task_list = [f"- {task['title']} (ID: {task['id']})" for task in result.tasks]
                    return {
                        'success': True,
                        'message': f"Which task would you like to delete? Here are your tasks:\n" + "\n".join(task_list)
                    }
                except Exception as e:
                    return {
                        'success': False,
                        'message': f"Sorry, I couldn't retrieve your tasks: {str(e)}"
                    }

        elif intent == 'complete':
            if task_name:
                # Find the task first
                find_result = self.find_task_by_name(task_name)

                if find_result['found']:
                    try:
                        # Complete the found task
                        request = CompleteTaskRequest(
                            task_id=find_result['task_id'],
                            user_id=self.user_id
                        )
                        result = complete_task(request, self.db_session)

                        if result.status == "not_found":
                            return {
                                'success': False,
                                'message': f"Sorry, I couldn't find that task to complete."
                            }
                        elif result.status == "already_completed":
                            return {
                                'success': True,
                                'message': f"Task '{find_result['title']}' is already marked as completed!"
                            }
                        else:
                            return {
                                'success': True,
                                'message': f"Great! I've marked task '{find_result['title']}' as completed."
                            }
                    except Exception as e:
                        return {
                            'success': False,
                            'message': f"Sorry, I couldn't complete that task: {str(e)}"
                        }
                else:
                    return {
                        'success': False,
                        'message': find_result.get('message', 'Could not find the specified task.')
                    }
            else:
                # If no specific task name, list tasks and ask
                try:
                    request = ListTasksRequest(user_id=self.user_id)
                    result = list_tasks(request, self.db_session)
                    task_list = [f"- {task['title']} (ID: {task['id']})" for task in result.tasks]
                    return {
                        'success': True,
                        'message': f"Which task would you like to complete? Here are your tasks:\n" + "\n".join(task_list)
                    }
                except Exception as e:
                    return {
                        'success': False,
                        'message': f"Sorry, I couldn't retrieve your tasks: {str(e)}"
                    }

        elif intent == 'list':
            try:
                # List all tasks
                request = ListTasksRequest(user_id=self.user_id)
                result = list_tasks(request, self.db_session)

                if not result.tasks:
                    return {
                        'success': True,
                        'message': "You don't have any tasks yet. Try adding one!"
                    }

                # Format the response
                task_list = []
                for task in result.tasks[:10]:  # Limit to first 10 tasks
                    status = "✓" if task["completed"] else "○"
                    task_list.append(f"{status} {task['id']}. {task['title']}")

                if len(result.tasks) > 10:
                    task_list.append(f"... and {len(result.tasks) - 10} more tasks")

                return {
                    'success': True,
                    'message': f"You have {result.total_count} tasks:\n" + "\n".join(task_list)
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f"Sorry, I couldn't retrieve your tasks: {str(e)}"
                }

        else:
            return {
                'success': False,
                'message': "I'm not sure what you'd like to do. You can add, delete, complete, or list tasks."
            }


def create_advanced_agent_with_tools(gemini_client: GeminiClient, db_session: Session):
    """
    Create an advanced agent with natural language processing capabilities
    """
    client = gemini_client.get_client()
    model_name = gemini_client.get_model()

    # Create the agent using openai-agents with enhanced instructions
    agent = Agent(
        name="SuperFlexibleTodoAssistant",
        instructions="""
        You are a SUPER FLEXIBLE assistant that understands ANY way the user wants to express themselves.
        Whether they speak in English, Hindi, Urdu, mixed language, or any creative way, you understand them perfectly.

        You are connected to an advanced NLP processor that handles all the actual task operations.
        Your job is to:
        1. Understand the user's intent regardless of how they express it
        2. Communicate with the NLP processor to perform the requested action
        3. Respond in a friendly, helpful manner

        You understand commands like:
        - 'task add kro name X' → Add task named X
        - 'task delete kro X wlaa/ka' → Find and delete task X
        - 'X ke naam se jo task he usko delete kro' → Find and delete task X
        - 'X ko complete kro' → Find and complete task X
        - 'mere tasks dikhao' → List all tasks
        - ANY creative combination the user comes up with

        Always be helpful, patient, and friendly regardless of how they phrase their request.
        """,
        model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
    )

    async def run_advanced_agent(messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
        """
        Run the advanced agent with natural language processing
        """
        # Get the last user message to process
        user_messages = [msg for msg in messages if msg['role'] == 'user']
        if not user_messages:
            return {
                "response": "Hello! How can I help you with your tasks today?",
                "tool_calls": [],
                "finish_reason": "stop"
            }

        last_message = user_messages[-1]['content']

        # Create the advanced NLP processor
        nlp_processor = AdvancedNLPProcessor(db_session, user_id)

        # Process the command
        result = nlp_processor.process_command(last_message)

        return {
            "response": result['message'],
            "tool_calls": [] if result['success'] else [],
            "finish_reason": "stop"
        }

    return run_advanced_agent