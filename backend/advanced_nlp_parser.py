import re
from typing import Dict, Any, Optional, Tuple
import json

class AdvancedNLPTaskParser:
    """
    Advanced Natural Language Parser that can understand any way the user expresses themselves
    """

    def __init__(self):
        # Common keywords and phrases in multiple languages
        self.add_keywords = [
            r'task\s+add\s+kro', r'add\s+a\s+task', r'create\s+task', r'make\s+task',
            r'bnana', r'bnaye', r'kar', r'karna', r'task\s+bnana', r'add\s+kro',
            r'task\s+do', r'do\s+task', r'add\s+krdo', r'krdo\s+task'
        ]

        self.delete_keywords = [
            r'task\s+delete\s+kro', r'delete\s+task', r'remove\s+task',
            r'hatao', r'nikalo', r'hatana', r'task\s+hatao', r'task\s+nikal',
            r'delete\s+kro', r'nikal\s+do', r'task\s+delete', r'hata\s+do'
        ]

        self.complete_keywords = [
            r'complete\s+task', r'finish\s+task', r'done\s+task', r'ho\s+gya',
            r'ho\s+gaya', r'kr\s+diya', r'kar\s+diya', r'complete\s+kro',
            r'task\s+complete', r'task\s+done', r'finish\s+kro'
        ]

        self.list_keywords = [
            r'my\s+tasks', r'all\s+tasks', r'show\s+tasks', r'list\s+tasks',
            r'tasks\s+dikhao', r'mere\s+tasks', r'tasks\s+hai', r'task\s+list',
            r'sab\s+tasks', r'show\s+me'
        ]

        # Task name extraction patterns (very flexible)
        self.task_name_patterns = [
            # Pattern: "task add kro name X" or "task add kro X"
            r'(?:task\s+add\s+kro|add\s+kro|task\s+bnana|bnana)\s+(?:name\s+)?(\w+)',

            # Pattern: "task delete kro X wlaa" or "task delete kro X"
            r'(?:task\s+delete\s+kro|delete\s+kro|task\s+hatao|hatao)\s+(\w+)\s*(?:wlaa|wala|vala)?',

            # Pattern: "X ke naam se jo task he usko delete kro"
            r'(\w+)\s+ke\s+naam\s+se\s+jo\s+task\s+he\s+usko\s+(?:delete|remove|hatao)\s+kro',

            # Pattern: "X ko delete kro"
            r'(\w+)\s+ko\s+(?:delete|remove|hatao)\s+(?:kro|krdo|kar)',

            # General patterns
            r'(?:to|for|par|pe)\s+(\w+)',  # "add task to X"
            r'(\w+)\s+(?:task|kam|kaam)',  # "X task"
            r'(\w+)',  # Just the word itself
        ]

    def detect_intent(self, text: str) -> str:
        """
        Detect the user's intent regardless of how they express it
        """
        text_lower = text.lower()

        # Check for add intent
        for pattern in self.add_keywords:
            if re.search(pattern, text_lower):
                return 'add'

        # Check for delete intent
        for pattern in self.delete_keywords:
            if re.search(pattern, text_lower):
                return 'delete'

        # Check for complete intent
        for pattern in self.complete_keywords:
            if re.search(pattern, text_lower):
                return 'complete'

        # Check for list intent
        for pattern in self.list_keywords:
            if re.search(pattern, text_lower):
                return 'list'

        # Default to add if nothing else matches
        return 'add'

    def extract_task_name(self, text: str) -> Optional[str]:
        """
        Extract task name from any kind of expression
        """
        text_lower = text.lower()

        # Try each pattern to extract task name
        for pattern in self.task_name_patterns:
            match = re.search(pattern, text_lower)
            if match:
                task_name = match.group(1)
                # Clean up the extracted name
                task_name = re.sub(r'\b(?:kro|krdo|kar|naam|se|jo|task|he|usko|ke|ko|wlaa|wala|vala|par|pe|to|for)\b', '', task_name).strip()
                if task_name and len(task_name) >= 1:
                    return task_name

        # If no pattern matches, try to extract any meaningful word
        words = re.findall(r'\b\w{2,}\b', text_lower)
        for word in words:
            if word not in ['task', 'tasks', 'kro', 'krdo', 'kar', 'ke', 'ko', 'naam', 'se', 'jo', 'he', 'usko', 'the', 'a', 'an', 'to', 'for', 'on', 'at', 'in', 'is', 'are', 'was', 'were']:
                return word

        return None

    def parse_command(self, text: str) -> Dict[str, Any]:
        """
        Parse any command and extract intent and task name
        """
        intent = self.detect_intent(text)
        task_name = self.extract_task_name(text)

        return {
            'intent': intent,
            'task_name': task_name,
            'original_text': text
        }

    def handle_flexible_input(self, text: str) -> Dict[str, Any]:
        """
        Handle any flexible input from the user
        """
        parsed = self.parse_command(text)

        # Generate appropriate response based on intent
        if parsed['intent'] == 'add':
            if parsed['task_name']:
                return {
                    'action': 'add_task',
                    'task_title': parsed['task_name'],
                    'message': f"Adding task: {parsed['task_name']}"
                }
            else:
                return {
                    'action': 'clarify',
                    'message': "Please specify what task you'd like to add."
                }

        elif parsed['intent'] == 'delete':
            if parsed['task_name']:
                return {
                    'action': 'find_and_delete_task',
                    'task_name': parsed['task_name'],
                    'message': f"Finding and deleting task: {parsed['task_name']}"
                }
            else:
                return {
                    'action': 'list_and_ask',
                    'message': "Which task would you like to delete? Here are your tasks:"
                }

        elif parsed['intent'] == 'complete':
            if parsed['task_name']:
                return {
                    'action': 'find_and_complete_task',
                    'task_name': parsed['task_name'],
                    'message': f"Finding and completing task: {parsed['task_name']}"
                }
            else:
                return {
                    'action': 'list_and_ask',
                    'message': "Which task would you like to mark as complete?"
                }

        elif parsed['intent'] == 'list':
            return {
                'action': 'list_tasks',
                'message': "Listing all your tasks"
            }

        else:
            return {
                'action': 'unknown',
                'message': "I'm not sure what you'd like to do. You can add, delete, complete, or list tasks."
            }

# Example usage
def test_parser():
    parser = AdvancedNLPTaskParser()

    test_inputs = [
        "task add kro name banana",
        "task delete kro banana wlaa",
        "banana ke naam se jo task he usko delete kro",
        "mere sab tasks dikhao",
        "complete the groceries task",
        "groceries ko complete krdo",
        "add task to buy milk",
        "task bnana hai name chocolate",
        "chocolate task hatao",
        "chocolate ko hatado",
        "what are my tasks?",
        "show me my todo list"
    ]

    for inp in test_inputs:
        result = parser.handle_flexible_input(inp)
        print(f"Input: '{inp}'")
        print(f"Output: {result}")
        print("-" * 50)

if __name__ == "__main__":
    test_parser()