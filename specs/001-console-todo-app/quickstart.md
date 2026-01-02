# Quickstart Guide: Console Todo Application

## Running the Application

1. Ensure Python 3.13+ is installed on your system
2. Navigate to the project root directory
3. Run the application:
   ```bash
   python src/cli/main.py
   ```

## Using the Application

### Main Menu
Once the application starts, you'll see a menu with the following options:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Exit

### Adding a Task
1. Select option 1 (Add Task)
2. Enter a title for the task (required, cannot be empty)
3. Optionally enter a description
4. The task will be added with an auto-incremented ID

### Viewing Tasks
1. Select option 2 (View Tasks)
2. All tasks will be displayed with their ID, title, description, and completion status ([ ] or [x])

### Updating a Task
1. Select option 3 (Update Task)
2. Enter the ID of the task you want to update
3. Enter the new title (or press Enter to keep current title)
4. Enter the new description (or press Enter to keep current description)

### Deleting a Task
1. Select option 4 (Delete Task)
2. Enter the ID of the task you want to delete
3. Confirm the deletion

### Marking a Task Complete/Incomplete
1. Select option 5 (Mark Complete)
2. Enter the ID of the task you want to toggle
3. The completion status will be switched

### Exiting the Application
1. Select option 6 (Exit)
2. The application will terminate cleanly

## Error Handling
- Invalid menu selections will prompt you to try again
- Invalid task IDs will show an error message
- Empty titles will be rejected when adding/updating tasks
- The application will never crash, even with invalid input