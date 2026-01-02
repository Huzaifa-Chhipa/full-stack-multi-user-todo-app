/**
 * Home page for the Todo Application
 */
'use client';

import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2 style={{ color: '#2c3e50' }}>Welcome to Todo App</h2>
        <p style={{ color: '#34495e', marginBottom: '20px' }}>
          Manage your tasks efficiently with our secure todo application.
        </p>
        <div className="auth-links" style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <Link href="/login" className="submit-btn" style={{
            textAlign: 'center',
            textDecoration: 'none',
            color: 'white'
          }}>
            Login
          </Link>
          <Link href="/signup" className="submit-btn" style={{
            textAlign: 'center',
            textDecoration: 'none',
            backgroundColor: '#27ae60',
            color: 'white'
          }}>
            Sign Up
          </Link>
          <Link href="/dashboard" className="submit-btn" style={{
            textAlign: 'center',
            textDecoration: 'none',
            backgroundColor: '#3498db',
            color: 'white'
          }}>
            Dashboard (if logged in)
          </Link>
        </div>
      </div>
    </div>
  );
}