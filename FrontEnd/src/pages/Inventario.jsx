import React from 'react';
import Sidebar from '../components/Sidebar';

const Inventario = () => {
  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-[180px] p-5 flex-grow">
        <h1 className="text-2xl font-bold mb-4">Inventario</h1>
        <p>Contenido de la página de Inventario.</p>
      </main>
    </div>
  );
};

export default Inventario;
