/**
 * Signup page for the Todo Application
 */
'use client';

import React, { useState } from 'react';
import { isAuthenticated } from '../../lib/auth';
import Link from 'next/link';
import axios from 'axios';

export default function SignupPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
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

    // Basic validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    if (username.length < 3) {
      setError('Username must be at least 3 characters');
      return;
    }

    setLoading(true);

    try {
      // Get the API base URL
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      // Call the register endpoint
      const response = await axios.post(`${API_BASE_URL}/auth/register`, {
        username,
        password
      });

      // If registration is successful, log in the user
      const loginResponse = await axios.post(`${API_BASE_URL}/auth/token`,
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
        localStorage.setItem('todo_app_token', loginResponse.data.access_token);
      }

      // Redirect to dashboard on successful signup/login
      if (typeof window !== 'undefined') {
        window.location.href = '/dashboard';
      }
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An error occurred during signup. Please try again.');
      }
      console.error('Signup error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Sign Up</h2>
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
          <div className="form-group" data-label="CONFIRM PASSWORD">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={loading}
              placeholder=" "
            />
          </div>
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? (
              <>
                <div className="loading-spinner"></div>
                <span>Creating account...</span>
              </>
            ) : (
              'Sign Up'
            )}
          </button>
        </form>
        <div className="auth-links">
          <p>Already have an account? <Link href="/login">Log in</Link></p>
          <p><Link href="/">Back to home</Link></p>
        </div>
      </div>
    </div>
  );
}