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
        <h2>Welcome to TaskFlow Pro</h2>
        <p style={{ color: '#f0f0f0', marginBottom: '25px', fontSize: '1.1rem', lineHeight: '1.6', fontWeight: '500' }}>
          Streamline your productivity with our cutting-edge task management platform. Experience seamless workflow, stunning visuals, and unmatched efficiency.
        </p>
        <div className="auth-links" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <Link href="/login" className="submit-btn">
            Login
          </Link>
          <Link href="/signup" className="submit-btn signup-btn">
            Create Account
          </Link>
          <Link href="/dashboard" className="submit-btn dashboard-btn">
            Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}