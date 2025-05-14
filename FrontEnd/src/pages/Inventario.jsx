import React from 'react';
import Sidebar from '../components/Sidebar';
import TablaInventario from '../components/TablaInventario';

const Inventario = () => {
  return (
    <div className="page-container">
      <Sidebar />
      <main className="main-content">
        <h1 className="text-2xl font-bold mb-4">Inventario</h1>
        <TablaInventario />
      </main>
    </div>
  );
};

export default Inventario;
