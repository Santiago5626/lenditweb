import React, { useState, useEffect } from 'react';
import './ResumenTarjetas.css';
import { getContadores } from '../api/peticiones';

const ResumenTarjetas = () => {
  const [contadores, setContadores] = useState({
    equiposDisponibles: 0,
    equiposNoDisponibles: 0,
    cargadoresDisponibles: 0,
    cargadoresNoDisponibles: 0
  });

  useEffect(() => {
    const fetchContadores = async () => {
      try {
        const data = await getContadores();
        setContadores(data);
      } catch (error) {
        console.error('Error al obtener contadores:', error);
      }
    };

    fetchContadores();
  }, []);

  const items = [
    { label: 'Equipos de cómputo disponibles', value: contadores.equiposDisponibles },
    { label: 'Equipos de cómputo no disponibles', value: contadores.equiposNoDisponibles },
    { label: 'Cargadores disponibles', value: contadores.cargadoresDisponibles },
    { label: 'Cargadores no disponibles', value: contadores.cargadoresNoDisponibles }
  ];

  const customColor = 'rgb(0, 48, 77)';

  return (
    <div className="container">
      <div className="row">
        {items.map((item, index) => (
          <div className="col-6 mb-3" key={index}>
            <div className="card shadow-sm p-3 d-flex flex-row align-items-center">
              <div className="rounded-circle" style={{
                width: '50px', 
                height: '50px', 
                marginRight: '15px',
                backgroundColor: customColor
              }}></div>
              <div>
                <p className="mb-0 font-weight-bold" style={{ color: customColor }}>
                  <strong>{item.value}</strong>
                </p>
                <p className="mb-0" style={{ color: customColor }}>
                  <strong>{item.label}</strong>
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResumenTarjetas;
