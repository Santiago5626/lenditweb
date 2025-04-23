import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/login';
import Inicio from './pages/inicio';
import Circulacion from './pages/Circulacion';
import Reportes from './pages/Reportes';
import Inventario from './pages/Inventario';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/inicio" element={<Inicio />} />
        <Route path="/circulacion" element={<Circulacion />} />
        <Route path="/reportes" element={<Reportes />} />
        <Route path="/inventario" element={<Inventario />} />
      </Routes>
    </Router>
  );
}

export default App;
