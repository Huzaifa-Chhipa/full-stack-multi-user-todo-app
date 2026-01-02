"""
Task data model for the console todo application.

This module defines the Task class with validation for non-empty titles.
"""

class Task:
    """
    Represents a single todo task with id, title, description, and completion status.
    """

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            id: Unique identifier for the task
            title: Task title (must be non-empty)
            description: Optional task description
            completed: Completion status (default: False)

        Raises:
            ValueError: If title is empty
        """
        if not title or not title.strip():
            raise ValueError("Title must be non-empty")

        self.id = id
        self.title = title.strip()
        self.description = description.strip()
        self.completed = completed

    def __str__(self):
        """
        Return a string representation of the task for display.

        Returns:
            str: Formatted string with completion status, ID, title, and description
        """
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}. {self.title}\n    {self.description}" if self.description else f"{status} {self.id}. {self.title}"

    def __repr__(self):
        """
        Return a detailed string representation of the task.

        Returns:
            str: Detailed representation for debugging purposes
        """
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"

    def to_dict(self):
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary containing all task attributes
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Task instance from a dictionary.

        Args:
            data: Dictionary containing task attributes

        Returns:
            Task: New Task instance
        """
        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )