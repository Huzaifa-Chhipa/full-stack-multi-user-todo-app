/**
 * Root layout for the Todo Application
 */
import React from 'react';
import './globals.css';

export const metadata = {
  title: 'Modern Todo Application',
  description: 'A full-stack multi-user todo application with 3D animations and gradient effects',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          {children}
        </div>
        {/* Floating particles for extra visual effect */}
        <div className="particles">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="particle"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                width: `${Math.random() * 10 + 2}px`,
                height: `${Math.random() * 10 + 2}px`,
              }}
            />
          ))}
        </div>
      </body>
    </html>
  );
}