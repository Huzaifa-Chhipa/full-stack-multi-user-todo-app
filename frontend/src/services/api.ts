/**
 * API client for the Todo Application
 * Handles all communication with the backend API
 */
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { getToken, getUserIdFromToken } from '../lib/auth';

// API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      console.error('Unauthorized access - token may be expired');
    }
    return Promise.reject(error);
  }
);

// Define API service functions
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Task API functions
export const taskApi = {
  // Get user ID from token
  getCurrentUserId: (): string | null => {
    return getUserIdFromToken();
  },

  // Get all tasks for the authenticated user
  getTasks: async (): Promise<Task[]> => {
    const userId = getUserIdFromToken();
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const token = getToken();
    const response = await apiClient.get<Task[]>(`/api/${userId}/tasks`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    return response.data;
  },

  // Get a specific task by ID
  getTask: async (taskId: number): Promise<Task> => {
    const userId = getUserIdFromToken();
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const token = getToken();
    const response = await apiClient.get<Task>(`/api/${userId}/tasks/${taskId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    return response.data;
  },

  // Create a new task
  createTask: async (taskData: CreateTaskData): Promise<Task> => {
    const userId = getUserIdFromToken();
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const token = getToken();
    const response = await apiClient.post<Task>(`/api/${userId}/tasks`, taskData, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    return response.data;
  },

  // Update a task
  updateTask: async (taskId: number, taskData: UpdateTaskData): Promise<Task> => {
    const userId = getUserIdFromToken();
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const token = getToken();
    const response = await apiClient.put<Task>(`/api/${userId}/tasks/${taskId}`, taskData, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    return response.data;
  },

  // Delete a task
  deleteTask: async (taskId: number): Promise<void> => {
    const userId = getUserIdFromToken();
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const token = getToken();
    await apiClient.delete(`/api/${userId}/tasks/${taskId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
  },

  // Toggle task completion status
  toggleTaskCompletion: async (taskId: number): Promise<Task> => {
    const userId = getUserIdFromToken();
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const token = getToken();
    const response = await apiClient.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {}, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    return response.data;
  },
};

export default apiClient;