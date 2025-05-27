import React from "react";
import Sidebar from "../components/Sidebar";
import ResumenTarjetas from "../components/ResumenTarjetas";
import PanelSolicitante from "../components/PanelSolicitante";
import "./inicio.css";

const Inicio = () => {

  return (
    <div className="page-container">
      <Sidebar />
      <main className="main-content">
        <div className="top-components">
          <div className="resumen-wrapper">
            <ResumenTarjetas />
          </div>
        </div>
        <PanelSolicitante />
      </main>
    </div>
  );
};

export default Inicio;
