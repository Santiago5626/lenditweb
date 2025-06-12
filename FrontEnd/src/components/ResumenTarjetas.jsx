import React, { useState, useEffect } from 'react';
import '../styles/components/ResumenTarjetas.css';
import { getContadores, fetchTiposProducto } from '../api/peticiones';

const ResumenTarjetas = () => {
  const [contadores, setContadores] = useState({});
  const [tiposProducto, setTiposProducto] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [contadoresData, tiposData] = await Promise.all([
          getContadores(),
          fetchTiposProducto()
        ]);
        setContadores(contadoresData);
        setTiposProducto(tiposData);
      } catch (error) {
        console.error('Error al obtener datos:', error);
      }
    };

    fetchData();
  }, []);

  // Solo mostrar contadores para equipo de cómputo y cargador
  const items = [
    {
      label: 'Equipos de cómputo disponibles',
      value: contadores.equipo_de_computo_disponibles || 0
    },
    {
      label: 'Equipos de cómputo no disponibles',
      value: contadores.equipo_de_computo_no_disponibles || 0
    },
    {
      label: 'Cargadores disponibles',
      value: contadores.cargador_disponibles || 0
    },
    {
      label: 'Cargadores no disponibles',
      value: contadores.cargador_no_disponibles || 0
    }
  ];

  const customColor = 'rgb(0, 48, 77)';

  return (
    <div className="container">
      <div className="row">
        {items.map((item, index) => (
          <div className="col-6 mb-3" key={index}>
            <div className="card shadow-sm p-3 d-flex flex-row align-items-center">
              <div className="rounded-circle d-flex align-items-center justify-content-center" style={{
                width: '50px',
                height: '50px',
                marginRight: '15px',
                backgroundColor: customColor,
                color: 'white',
                fontWeight: 'bold',
                fontSize: '16px'
              }}>
                {item.value}
              </div>
              <div>
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
