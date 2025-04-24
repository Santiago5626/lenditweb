import React from 'react';
import Sidebar from '../components/Sidebar';
import ResumenTarjetas from '../components/ResumenTarjetas';
import TablaResumenEstado from '../components/TablaResumenEstado';
import TablaUsuarios from '../components/TablaUsuarios';

const Inicio = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <main style={{ marginLeft: '240px', padding: '20px', flexGrow: 1 }}>
        <ResumenTarjetas />
        <TablaResumenEstado />
        <TablaUsuarios />
      </main>
    </div>
  );
};

export default Inicio;

