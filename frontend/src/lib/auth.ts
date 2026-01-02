/**
 * Authentication utilities for the Todo Application
 * Handles JWT token storage and management
 */
import axios from 'axios';

// API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Store JWT token in localStorage
const TOKEN_KEY = 'todo_app_token';

// Get token from localStorage
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
};

// Set token in localStorage
export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
};

// Remove token from localStorage
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
};

// Get user ID from token (decode JWT without verification)
export const getUserIdFromToken = (): string | null => {
  const token = getToken();
  if (!token) return null;

  try {
    const payload = token.split('.')[1];
    const decodedPayload = atob(payload);
    const parsedPayload = JSON.parse(decodedPayload);
    return parsedPayload.sub || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Login function
export const login = async (username: string, password: string): Promise<{ access_token: string; token_type: string } | null> => {
  try {
    // In a real application, this would be a separate signup endpoint
    // For this demo, we'll use the same endpoint for both login and signup
    // FastAPI expects form data by default for login endpoints
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await axios.post(`${API_BASE_URL}/auth/token`, params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
    const { access_token } = response.data;
    setToken(access_token);
    return response.data;
  } catch (error: any) {
    console.error('Login/Signup error:', error);
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
      console.error('Response headers:', error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('Request:', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error message:', error.message);
    }
    return null;
  }
};

// Logout function
export const logout = (): void => {
  removeToken();
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return !!getToken();
};