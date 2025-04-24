import React from 'react';
import Sidebar from '../components/Sidebar';

const Circulacion = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <main style={{ marginLeft: '180px', padding: '20px', flexGrow: 1 }}>
        <h1>Circulación</h1>
        <p>Contenido de la página de Circulación.</p>
      </main>
    </div>
  );
};

export default Circulacion;
