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


def create_task_tool():
    """Create tool for adding tasks."""
    async def add_task_tool(title: str, description: str = None, user_id: str = None):
        """Add a new task to the user's todo list"""
        # We'll pass the db_session when we call the function, so we'll need to make it available
        # This is a limitation - we'll handle this differently in the actual agent
        pass

    return add_task_tool


def create_agent_with_tools(gemini_client: GeminiClient, db_session: Session):
    """
    Create an agent with all the MCP tools bound to it using openai-agents.

    Args:
        gemini_client: Initialized Gemini client
        db_session: Database session for the tools to use

    Returns:
        A function that can run the agent with tools
    """
    client = gemini_client.get_client()
    model_name = gemini_client.get_model()

    # Create the agent using openai-agents
    agent = Agent(
        name="TodoAssistant",
        instructions="You are a helpful assistant that helps users manage their todo list. You can add, list, update, complete, and delete tasks. Always be helpful and friendly.",
        model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
    )

    # Define the available tools that will be bound to the agent
    def bind_tools_to_agent():
        """Bind the task tools to the agent"""
        # In the actual implementation, we would register the tools with the agent
        # For now, we'll create a custom function to handle tool calls
        pass

    async def run_agent(messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
        """
        Run the agent with the provided messages and tools.

        Args:
            messages: List of messages in the conversation (with role and content)
            user_id: ID of the current user

        Returns:
            Response from the agent including potential tool calls and final response
        """
        # Convert messages to the format expected by the runner
        # The messages should be in the format "role: content"
        message_text = ""
        for msg in messages:
            message_text += f"{msg['role']}: {msg['content']}\n"

        # Run the agent with the messages
        result = await Runner.run(
            agent,
            message_text,
        )

        # Process the response
        response_content = result.final_output if result.final_output else ""

        # For now, returning a basic response structure
        # In a real implementation, we'd need to handle tool calls differently
        return {
            "response": response_content,
            "tool_calls": [],  # Actual tool calls would be handled by the agent framework
            "finish_reason": "stop"
        }

    return run_agent