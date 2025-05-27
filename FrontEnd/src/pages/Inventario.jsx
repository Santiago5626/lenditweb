import React from 'react';
import Sidebar from '../components/Sidebar';
import TablaInventario from '../components/TablaInventario';

const Inventario = () => {
  return (
    <div className="page-container">
      <Sidebar />
      <main className="main-content">
        <TablaInventario />
      </main>
    </div>
  );
};

export default Inventario;
