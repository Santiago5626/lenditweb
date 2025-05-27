import React from 'react';
import Sidebar from '../components/Sidebar';

const Reportes = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <main style={{ marginLeft: '180px', padding: '20px', flexGrow: 1 }}>
        <h1>Reportes</h1>
        <p>Contenido de la página de Reportes.</p>
      </main>
    </div>
  );
};

export default Reportes;
