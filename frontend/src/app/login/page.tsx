/**
 * Login page for the Todo Application
 */
'use client';

import React, { useState } from 'react';
import { login, isAuthenticated } from '../../lib/auth';
import Link from 'next/link';
import axios from 'axios';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Redirect if already authenticated
  if (typeof window !== 'undefined' && isAuthenticated()) {
    window.location.href = '/dashboard';
    return <div className="loading">Redirecting...</div>;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Get the API base URL
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      // Direct API call to login endpoint
      const response = await axios.post(`${API_BASE_URL}/auth/token`,
        new URLSearchParams({
          'username': username,
          'password': password
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        }
      );

      // Store the token
      if (typeof window !== 'undefined') {
        localStorage.setItem('todo_app_token', response.data.access_token);
      }

      // Redirect to dashboard on successful login
      if (typeof window !== 'undefined') {
        window.location.href = '/dashboard';
      }
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Invalid username or password');
      }
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Login</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group" data-label="USERNAME">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
              placeholder=" "
            />
          </div>
          <div className="form-group" data-label="PASSWORD">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
              placeholder=" "
            />
          </div>
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? (
              <>
                <div className="loading-spinner"></div>
                <span>Logging in...</span>
              </>
            ) : (
              'Login'
            )}
          </button>
        </form>
        <div className="auth-links">
          <p>Don't have an account? <Link href="/signup">Sign up</Link></p>
          <p><Link href="/">Back to home</Link></p>
        </div>
      </div>
    </div>
  );
}