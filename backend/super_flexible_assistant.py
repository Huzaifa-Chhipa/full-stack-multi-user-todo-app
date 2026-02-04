from openai import OpenAI
from .openai_assistant_functions import FUNCTION_MAP
from .advanced_nlp_parser import AdvancedNLPTaskParser
import json

# Initialize OpenAI client
client = OpenAI(api_key="your-openai-api-key")

def create_super_flexible_todo_assistant(model_name="gpt-4-turbo-preview"):
    """
    Create a Super Flexible Todo Assistant that understands any way the user speaks
    """
    assistant = client.beta.assistants.create(
        name="Super Flexible Todo Assistant",
        instructions="""You are an extremely flexible assistant that understands ANY way the user expresses themselves.
        Whether they speak in English, Hindi, Urdu, mixed language, or any creative way, you understand them.

        You have advanced NLP capabilities to parse commands like:
        - 'task add kro name X' → Add task named X
        - 'task delete kro X wlaa' → Find and delete task X
        - 'X ke naam se jo task he usko delete kro' → Find and delete task X
        - 'mere tasks dikhao' → List all tasks
        - 'X ko complete kro' → Find and complete task X

        You understand that the user can express themselves in any format and you adapt to their language.
        Always be helpful, patient, and friendly regardless of how they phrase their request.""",
        model=model_name,
        tools=[{
            "type": "function",
            "function": {
                "name": "parse_and_execute_command",
                "description": "Parse any user command and execute the appropriate task operation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_input": {"type": "string", "description": "The user's original input"},
                        "user_id": {"type": "string", "description": "ID of the user"}
                    },
                    "required": ["user_input", "user_id"]
                }
            }
        }]
    )

    return assistant

def handle_super_flexible_response(thread_id, run_id, user_id: str):
    """
    Handle the assistant's response with advanced NLP parsing
    """
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls

        tool_outputs = []
        parser = AdvancedNLPTaskParser()

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if function_name == "parse_and_execute_command":
                user_input = arguments['user_input']

                # Parse the user's flexible input
                parsed_result = parser.handle_flexible_input(user_input)

                # Execute the appropriate action
                result = execute_parsed_action(parsed_result, user_id)

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

def execute_parsed_action(parsed_result: dict, user_id: str):
    """
    Execute the action based on parsed result
    """
    action = parsed_result.get('action')

    if action == 'add_task':
        task_title = parsed_result.get('task_title', '')
        return FUNCTION_MAP['add_task']({'user_id': user_id, 'title': task_title})

    elif action == 'find_and_delete_task':
        task_name = parsed_result.get('task_name', '')
        # First list tasks to find the one with matching name
        list_result = FUNCTION_MAP['list_tasks']({'user_id': user_id})

        if list_result.get('success'):
            tasks = list_result.get('tasks', [])
            matching_task = None

            # Find task with matching name
            for task in tasks:
                if task_name.lower() in task['title'].lower():
                    matching_task = task
                    break

            if matching_task:
                return FUNCTION_MAP['delete_task']({
                    'user_id': user_id,
                    'task_id': matching_task['id']
                })
            else:
                return {
                    "success": False,
                    "error": f"Could not find a task containing '{task_name}'. Available tasks: {[t['title'] for t in tasks]}"
                }
        else:
            return list_result

    elif action == 'find_and_complete_task':
        task_name = parsed_result.get('task_name', '')
        # First list tasks to find the one with matching name
        list_result = FUNCTION_MAP['list_tasks']({'user_id': user_id})

        if list_result.get('success'):
            tasks = list_result.get('tasks', [])
            matching_task = None

            # Find task with matching name
            for task in tasks:
                if task_name.lower() in task['title'].lower():
                    matching_task = task
                    break

            if matching_task:
                return FUNCTION_MAP['complete_task']({
                    'user_id': user_id,
                    'task_id': matching_task['id']
                })
            else:
                return {
                    "success": False,
                    "error": f"Could not find a task containing '{task_name}'. Available tasks: {[t['title'] for t in tasks]}"
                }
        else:
            return list_result

    elif action == 'list_tasks':
        return FUNCTION_MAP['list_tasks']({'user_id': user_id})

    else:
        return {
            "success": False,
            "error": "Could not understand the command. Please try rephrasing."
        }

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
            # We can't handle recursive calls in this simplified version
            return "Processing..."

        time.sleep(1)

# Example usage with any way of speaking
def example_flexible_usage():
    """
    Example of how the flexible assistant handles any input
    """
    # Create the super flexible assistant
    assistant = create_super_flexible_todo_assistant()

    # Create a thread for the conversation
    thread = client.beta.threads.create()

    # Try different ways of expressing the same thing
    test_commands = [
        "task add kro name buy groceries",
        "task delete kro groceries wlaa",
        "banana ke naam se jo task he usko delete kro",
        "mere tasks dikhao",
        "complete the milk task"
    ]

    for command in test_commands:
        # Add a user message
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=command
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Handle the response
        response = wait_for_run_completion(thread.id, run.id)
        print(f"Command: {command}")
        print(f"Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    example_flexible_usage()