import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/login';
import Inicio from './pages/inicio';
import Inventario from './pages/Inventario';
import Circulacion from './pages/Circulacion';
import Reportes from './pages/Reportes';
import ProtectedRoute from './components/ProtectedRoute';
import { initializeAuth } from './api/auth';
import './styles/App.css';

function App() {
  useEffect(() => {
    // Inicializar el sistema de autenticación al cargar la aplicación
    initializeAuth();
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/inicio" element={<ProtectedRoute><Inicio /></ProtectedRoute>} />
        <Route path="/inventario" element={<ProtectedRoute><Inventario /></ProtectedRoute>} />
        <Route path="/circulacion" element={<ProtectedRoute><Circulacion /></ProtectedRoute>} />
        <Route path="/reportes" element={<ProtectedRoute><Reportes /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
