/**
 * Signup page for the Todo Application
 */
'use client';

import React, { useState } from 'react';
import { login, isAuthenticated } from '../../lib/auth';
import Link from 'next/link';

export default function SignupPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Redirect if already authenticated
  if (isAuthenticated()) {
    if (typeof window !== 'undefined') {
      window.location.href = '/dashboard';
    }
    return <div>Redirecting...</div>;
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

    setLoading(true);

    try {
      // For this demo, we'll use the same login endpoint for signup
      // In a real app, you'd have a separate signup endpoint
      const result = await login(username, password);
      if (result) {
        // Redirect to dashboard on successful signup/login
        if (typeof window !== 'undefined') {
          window.location.href = '/dashboard';
        }
      } else {
        setError('Signup failed. Please try again.');
      }
    } catch (err) {
      setError('An error occurred during signup');
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
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
              placeholder="Choose a username"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
              placeholder="Create a password (min 6 chars)"
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={loading}
              placeholder="Confirm your password"
            />
          </div>
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Creating account...' : 'Sign Up'}
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