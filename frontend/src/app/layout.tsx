/**
 * Root layout for the Todo Application
 */
import React from 'react';
import './globals.css';

export const metadata = {
  title: 'Todo Application',
  description: 'A full-stack multi-user todo application',
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
      </body>
    </html>
  );
}