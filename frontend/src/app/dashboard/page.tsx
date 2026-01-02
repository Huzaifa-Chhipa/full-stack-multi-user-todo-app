/**
 * Dashboard page for the Todo Application
 * Displays all tasks for the authenticated user
 */
'use client';

import React, { useState, useEffect } from 'react';
import { taskApi, Task } from '../../services/api';
import { isAuthenticated, logout } from '../../lib/auth';

// TaskItem component for displaying individual tasks
const TaskItem: React.FC<{
  task: Task;
  onUpdate: (task: Task) => void;
  onDelete: (id: number) => void;
  onToggle: (id: number) => void;
}> = ({ task, onUpdate, onDelete, onToggle }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleUpdate = async () => {
    try {
      const updatedTask = await taskApi.updateTask(task.id, {
        title,
        description,
      });
      onUpdate(updatedTask);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await onDelete(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const handleToggle = async () => {
    try {
      await onToggle(task.id);
    } catch (error) {
      console.error('Error toggling task:', error);
    }
  };

  return (
    <div className="task-item">
      {isEditing ? (
        <div className="task-edit-form">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength={200}
            className="task-title-input"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            maxLength={1000}
            className="task-description-input"
          />
          <div className="task-actions">
            <button onClick={handleUpdate} className="save-btn">Save</button>
            <button onClick={() => setIsEditing(false)} className="cancel-btn">Cancel</button>
          </div>
        </div>
      ) : (
        <div className="task-display">
          <div className="task-header">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggle}
              className="task-checkbox"
            />
            <h3 className={task.completed ? 'completed' : ''}>{task.title}</h3>
            <div className="task-actions">
              <button onClick={() => setIsEditing(true)} className="edit-btn">Edit</button>
              <button onClick={handleDelete} className="delete-btn">Delete</button>
            </div>
          </div>
          {task.description && (
            <p className={`task-description ${task.completed ? 'completed' : ''}`}>
              {task.description}
            </p>
          )}
          <small className="task-timestamp">
            Created: {new Date(task.created_at).toLocaleString()}
            {task.updated_at !== task.created_at && ` | Updated: ${new Date(task.updated_at).toLocaleString()}`}
          </small>
        </div>
      )}
    </div>
  );
};

// Main dashboard component
export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);

  // Check if user is authenticated
  useEffect(() => {
    if (!isAuthenticated()) {
      window.location.href = '/login';
    }
  }, []);

  // Load tasks when component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const tasksData = await taskApi.getTasks();
        setTasks(tasksData);
      } catch (err) {
        setError('Failed to load tasks');
        console.error('Error loading tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated()) {
      fetchTasks();
    }
  }, []);

  const handleCreateTask = async () => {
    if (!newTaskTitle.trim()) {
      alert('Title is required');
      return;
    }

    try {
      const newTask = await taskApi.createTask({
        title: newTaskTitle,
        description: newTaskDescription,
      });
      setTasks([newTask, ...tasks]); // Add new task to the top
      setNewTaskTitle('');
      setNewTaskDescription('');
      setShowCreateForm(false);
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleUpdateTask = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await taskApi.deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleToggleTask = async (id: number) => {
    try {
      const toggledTask = await taskApi.toggleTaskCompletion(id);
      setTasks(tasks.map(task => task.id === id ? toggledTask : task));
      return toggledTask;
    } catch (error) {
      console.error('Error toggling task:', error);
      throw error;
    }
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  if (!isAuthenticated()) {
    return <div>Redirecting to login...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>My Todo List</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </header>

      {error && <div className="error">{error}</div>}

      {loading ? (
        <div className="loading">Loading tasks...</div>
      ) : (
        <>
          <div className="create-task-section">
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="create-task-btn"
            >
              {showCreateForm ? 'Cancel' : 'Add New Task'}
            </button>

            {showCreateForm && (
              <div className="create-task-form">
                <input
                  type="text"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  placeholder="Task title (1-200 characters)"
                  maxLength={200}
                  className="task-title-input"
                />
                <textarea
                  value={newTaskDescription}
                  onChange={(e) => setNewTaskDescription(e.target.value)}
                  placeholder="Task description (max 1000 characters)"
                  maxLength={1000}
                  className="task-description-input"
                />
                <button onClick={handleCreateTask} className="add-task-btn">
                  Add Task
                </button>
              </div>
            )}
          </div>

          <div className="tasks-list">
            {tasks.length === 0 ? (
              <div className="no-tasks">No tasks yet. Add a new task to get started!</div>
            ) : (
              tasks.map(task => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onUpdate={handleUpdateTask}
                  onDelete={handleDeleteTask}
                  onToggle={async (id: number) => {
                    await handleToggleTask(id);
                    // Refresh the task list to reflect the toggle
                    const updatedTasks = await taskApi.getTasks();
                    setTasks(updatedTasks);
                  }}
                />
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}