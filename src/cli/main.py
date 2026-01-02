"""
Main CLI application for the console todo application.

This module provides a menu-driven interface for users to manage their tasks.
"""

from src.services.task_manager import TaskManager
from src.models.task import Task
from typing import Optional


class TodoApp:
    """
    Main CLI application for managing todo tasks.
    """

    def __init__(self):
        """
        Initialize the TodoApp with a TaskManager instance.
        """
        self.task_manager = TaskManager()
        self.running = True

    def display_menu(self):
        """
        Display the main menu options to the user.
        """
        print("\n" + "="*40)
        print("         TODO LIST APPLICATION")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        print("="*40)

    def get_user_choice(self) -> str:
        """
        Get and validate user menu choice.

        Returns:
            str: The user's menu choice
        """
        try:
            choice = input("Enter your choice (1-6): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nApplication interrupted. Exiting...")
            return "6"  # Return exit choice

    def add_task(self):
        """
        Handle adding a new task based on user input.
        """
        try:
            print("\n--- Add New Task ---")
            title = input("Enter task title: ").strip()

            if not title:
                print("Error: Title cannot be empty!")
                return

            description = input("Enter task description (optional): ").strip()

            task = self.task_manager.add_task(title, description)
            print(f"Task added successfully with ID: {task.id}")

        except ValueError as e:
            print(f"Error: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def view_tasks(self):
        """
        Display all tasks to the user.
        """
        try:
            print("\n--- All Tasks ---")
            tasks = self.task_manager.get_all_tasks()

            if not tasks:
                print("No tasks found.")
                return

            for task in tasks:
                print(task)

        except Exception as e:
            print(f"An error occurred while viewing tasks: {e}")

    def update_task(self):
        """
        Handle updating an existing task based on user input.
        """
        try:
            print("\n--- Update Task ---")
            task_id_str = input("Enter task ID to update: ").strip()

            if not task_id_str.isdigit():
                print("Error: Task ID must be a number!")
                return

            task_id = int(task_id_str)

            # Check if task exists
            existing_task = self.task_manager.get_task(task_id)
            if not existing_task:
                print(f"Error: Task with ID {task_id} does not exist!")
                return

            print(f"Current task: {existing_task}")

            # Get new title (keep existing if empty input)
            new_title_input = input(f"Enter new title (current: '{existing_task.title}', press Enter to keep): ").strip()
            new_title = new_title_input if new_title_input else None

            # Get new description (keep existing if empty input)
            new_description_input = input(f"Enter new description (current: '{existing_task.description}', press Enter to keep): ").strip()
            new_description = new_description_input if new_description_input else None

            # Update task
            updated_task = self.task_manager.update_task(task_id, new_title, new_description)

            if updated_task:
                print(f"Task {task_id} updated successfully!")
            else:
                print(f"Failed to update task {task_id}.")

        except ValueError as e:
            print(f"Error: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete_task(self):
        """
        Handle deleting a task based on user input.
        """
        try:
            print("\n--- Delete Task ---")
            task_id_str = input("Enter task ID to delete: ").strip()

            if not task_id_str.isdigit():
                print("Error: Task ID must be a number!")
                return

            task_id = int(task_id_str)

            # Check if task exists
            existing_task = self.task_manager.get_task(task_id)
            if not existing_task:
                print(f"Error: Task with ID {task_id} does not exist!")
                return

            print(f"Task to delete: {existing_task}")
            confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()

            if confirm in ['y', 'yes']:
                deleted = self.task_manager.delete_task(task_id)
                if deleted:
                    print(f"Task {task_id} deleted successfully!")
                else:
                    print(f"Failed to delete task {task_id}.")
            else:
                print("Deletion cancelled.")

        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def toggle_task_completion(self):
        """
        Handle toggling task completion status based on user input.
        """
        try:
            print("\n--- Mark Task Complete/Incomplete ---")
            task_id_str = input("Enter task ID to toggle: ").strip()

            if not task_id_str.isdigit():
                print("Error: Task ID must be a number!")
                return

            task_id = int(task_id_str)

            # Check if task exists
            existing_task = self.task_manager.get_task(task_id)
            if not existing_task:
                print(f"Error: Task with ID {task_id} does not exist!")
                return

            print(f"Current task: {existing_task}")

            # Toggle completion status
            toggled_task = self.task_manager.toggle_task_completion(task_id)

            if toggled_task:
                status = "completed" if toggled_task.completed else "incomplete"
                print(f"Task {task_id} marked as {status}!")
            else:
                print(f"Failed to toggle task {task_id}.")

        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def exit_app(self):
        """
        Handle application exit.
        """
        print("Thank you for using the Todo List Application!")
        self.running = False

    def handle_choice(self, choice: str):
        """
        Handle the user's menu choice.

        Args:
            choice: The user's menu choice
        """
        if choice == "1":
            self.add_task()
        elif choice == "2":
            self.view_tasks()
        elif choice == "3":
            self.update_task()
        elif choice == "4":
            self.delete_task()
        elif choice == "5":
            self.toggle_task_completion()
        elif choice == "6":
            self.exit_app()
        else:
            print("Invalid choice! Please enter a number between 1-6.")

    def run(self):
        """
        Run the main application loop.
        """
        print("Welcome to the Todo List Application!")

        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                self.handle_choice(choice)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again.")


def main():
    """
    Main entry point for the application.
    """
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()