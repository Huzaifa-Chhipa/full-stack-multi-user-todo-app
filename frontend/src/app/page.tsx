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
        <h2>Welcome to Modern Todo App</h2>
        <p style={{ color: '#34495e', marginBottom: '25px', fontSize: '1.1rem', lineHeight: '1.6' }}>
          Manage your tasks efficiently with our secure, modern todo application featuring 3D animations and gradient effects.
        </p>
        <div className="auth-links" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <Link href="/login" className="submit-btn">
            Login
          </Link>
          <Link href="/signup" className="submit-btn signup-btn">
            Sign Up
          </Link>
          <Link href="/dashboard" className="submit-btn dashboard-btn">
            Dashboard (if logged in)
          </Link>
        </div>
      </div>
    </div>
  );
}