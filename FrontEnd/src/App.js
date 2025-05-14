import "./App.css";
import "./styles/layout.css";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./pages/login";
import Inicio from "./pages/inicio";
import Reportes from "./pages/Reportes";
import Inventario from "./pages/Inventario";
import Circulacion from "./pages/Circulacion";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/inicio"
          element={
            <ProtectedRoute>
              <Inicio />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Circulacion"
          element={
            <ProtectedRoute>
              <Circulacion />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Reportes"
          element={
            <ProtectedRoute>
              <Reportes />
            </ProtectedRoute>
          }
        />
        <Route
          path="/inventario"
          element={
            <ProtectedRoute>
              <Inventario />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
