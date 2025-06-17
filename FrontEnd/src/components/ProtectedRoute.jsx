import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated, verifyToken } from '../api/auth';
import LoadingSpinner from './LoadingSpinner';

const ProtectedRoute = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Verificar si hay token en localStorage
        if (!isAuthenticated()) {
          setIsAuth(false);
          setIsLoading(false);
          return;
        }

        // Verificar si el token es válido en el servidor
        const isValid = await verifyToken();
        setIsAuth(isValid);
      } catch (error) {
        console.error('Error verificando autenticación:', error);
        setIsAuth(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Mostrar spinner mientras se verifica la autenticación
  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh'
      }}>
        <LoadingSpinner />
      </div>
    );
  }

  // Redirigir al login si no está autenticado
  if (!isAuth) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;
