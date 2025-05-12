import React from 'react';
import './ResumenTarjetas.css';

const items = [
  'Equipos de cómputo disponibles',
  'Equipos de cómputo no disponibles',
  'Cargadores disponibles',
  'Cargadores no disponibles',
];

const ResumenTarjetas = () => {
  return (
    <div className="container">
      <div className="row">
        {items.map((item, index) => (
          <div className="col-6 mb-3" key={index}>
            <div className="card shadow-sm p-3 d-flex flex-row align-items-center">
              <div className="bg-primary rounded-circle" style={{width: '50px', height: '50px', marginRight: '15px'}}></div>
              <p className="mb-0 text-primary font-weight-bold">
                <strong>{item.split(' ')[0]} <br />{item.split(' ').slice(1).join(' ')}</strong>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResumenTarjetas;
