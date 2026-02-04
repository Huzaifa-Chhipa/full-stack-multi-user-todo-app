from openai import OpenAI
from .openai_assistant_functions import FUNCTION_SCHEMAS, FUNCTION_MAP
import json

# Initialize OpenAI client
client = OpenAI(api_key="your-openai-api-key")

def create_todo_assistant(model_name="gpt-4-turbo-preview"):
    """
    Create a Todo Assistant with function calling capabilities
    """
    assistant = client.beta.assistants.create(
        name="Todo Assistant",
        instructions="""You are a helpful assistant that helps users manage their todo list.
        You can add, list, update, complete, and delete tasks.
        You understand both English and Hindi/Urdu commands.
        When a user gives a command like 'task add kro name X', call the add_task function.
        When a user gives a command like 'task delete kro X wlaa', first list tasks to find the correct ID, then call delete_task function.
        When a user says 'X ke naam se jo task he usko delete kro', first list tasks to find the correct ID, then call delete_task function.
        Always be helpful and friendly.""",
        model=model_name,
        tools=FUNCTION_SCHEMAS  # This is where you pass the function schemas
    )

    return assistant

def handle_assistant_response(thread_id, run_id):
    """
    Handle the assistant's response and execute any required functions
    """
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls

        tool_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Execute the function
            if function_name in FUNCTION_MAP:
                result = FUNCTION_MAP[function_name](arguments)

                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(result)
                })

        # Submit tool outputs back to the assistant
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

        # Wait for the run to complete
        return wait_for_run_completion(thread_id, run_id)

    return run

def wait_for_run_completion(thread_id, run_id):
    """
    Wait for a run to complete
    """
    import time

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        if run.status == "completed":
            # Get the messages
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            return messages.data[0].content[0].text.value
        elif run.status == "failed":
            return f"Error: {run.last_error.message}"
        elif run.status == "requires_action":
            return handle_assistant_response(thread_id, run_id)

        time.sleep(1)

# Example usage:
def example_usage():
    """
    Example of how to use the assistant
    """
    # Create the assistant
    assistant = create_todo_assistant()

    # Create a thread for the conversation
    thread = client.beta.threads.create()

    # Add a user message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="task add kro name buy groceries"
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Handle the response
    response = wait_for_run_completion(thread.id, run.id)
    print(response)

if __name__ == "__main__":
    example_usage()