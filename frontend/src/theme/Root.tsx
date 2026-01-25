import React from 'react';
import { AuthProvider } from '../context/AuthContext';
import Chatbot from '../components/Chatbot';

interface RootProps {
  children: React.ReactNode;
}

export default function Root({ children }: RootProps): JSX.Element {
  return (
    <AuthProvider>
      {children}
      <Chatbot />
    </AuthProvider>
  );
}
