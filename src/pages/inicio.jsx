import React from 'react';
import Sidebar from '../components/Sidebar';

const Inicio = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <main style={{ marginLeft: '180px', padding: '20px', flexGrow: 1 }}>
        <h1>Bienvenido a la página de inicio</h1>
        <p>Contenido principal aquí.</p>
      </main>
    </div>
  );
};

export default Inicio;
