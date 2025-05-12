import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import { useNavigate } from "react-router-dom";
import ResumenTarjetas from "../components/ResumenTarjetas";
import TablaResumenEstado from "../components/TablaResumenEstado";
import TablaUsuarios from "../components/TablaUsuarios";
import { agregar } from "../api/peticiones";

import "./inicio.css";

const Inicio = () => {
  const navigate = useNavigate();

  const [cc, setCC] = useState("");
  const [nombre, setNombre] = useState("");
  const [apellido, setApellido] = useState(""); // corregido
  const [email, setEmail] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const data = await agregar(cc, nombre, apellido, email);
      alert("AGREGADO");
      navigate("/inicio");
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="container">
      <Sidebar />
      <main className="main-content">
        <div className="top-components">
          <div className="resumen-wrapper">
            <ResumenTarjetas />
          </div>
          <div className="tabla-resumen-wrapper">
            <TablaResumenEstado />
          </div>
        </div>
        <TablaUsuarios />
      </main>
    </div>
  );
};

export default Inicio;
