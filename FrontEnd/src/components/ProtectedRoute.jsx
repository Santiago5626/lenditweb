import React from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../api/auth';

const ProtectedRoute = ({ children }) => {
  const auth = isAuthenticated();
  
  if (!auth) {
    // Redirigir al login si no está autenticado
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
