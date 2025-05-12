import React from "react";
import { Link, useLocation } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Sidebar.css";
import perfil from "../images/perfil.png";

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { name: "Inicio", icon: "home", path: "/inicio" },
    { name: "Circulacion", icon: "sync", path: "/Circulacion" },
    { name: "Reportes", icon: "lab_profile", path: "/reportes" },
    { name: "Inventario", icon: "inventory", path: "/inventario" },
  ];

  return (
    <div className="sidebar flex flex-col h-screen bg-[#04395e] text-white p-4">
      <div className="flex flex-col flex-grow">
        <div className="user-info mb-6">
          <img src={perfil} alt="Perfil" className="profile-image" />
          <div className="user-text">
            <h3>Sophia Wilson</h3>
            <span>Administrador</span>
          </div>
        </div>

        <div className="menu">
          <ul className="space-y-2">
            {menuItems.map((item) => (
              <li
                key={item.name}
                className={`${location.pathname === item.path ? "active" : ""}`}
              >
                <Link to={item.path} className="flex items-center gap-2">
                  <span className="material-symbols-outlined">{item.icon}</span>
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="menu bottom-menu">
        <ul>
          <li>
            <Link to="/configuracion" className="flex items-center gap-2">
              <span className="material-symbols-outlined">manufacturing</span>
              Configuración
            </Link>
          </li>
          <li>
            <a href="index.html" className="flex items-center gap-2">
              <span className="material-symbols-outlined">logout</span>
              Cerrar sesión
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
