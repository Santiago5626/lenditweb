import React from "react";
import Sidebar from "../components/Sidebar";
import ResumenTarjetas from "../components/ResumenTarjetas";
import TablaResumenEstado from "../components/TablaResumenEstado";
import TablaSolicitantes from "../components/TablaSolicitantes";

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
          <div className="tabla-resumen-wrapper">
            <TablaResumenEstado />
          </div>
        </div>
        <TablaSolicitantes />
      </main>
    </div>
  );
};

export default Inicio;
