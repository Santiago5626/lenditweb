import React, { useState } from 'react';
import '../styles/components/SelectorSolicitantes.css';

const SelectorSolicitantes = ({ solicitantes, onSelectSolicitante, solicitanteSeleccionado }) => {
  const [filtroBusqueda, setFiltroBusqueda] = useState('');

  const filtrarSolicitantes = () => {
    return solicitantes.filter(solicitante => {
      const nombreCompleto = `${solicitante.primer_nombre} ${solicitante.segundo_nombre || ''} ${solicitante.primer_apellido} ${solicitante.segundo_apellido || ''}`.toLowerCase();
      const busqueda = filtroBusqueda.toLowerCase();
      
      return nombreCompleto.includes(busqueda) ||
             solicitante.identificacion.toString().includes(busqueda) ||
             (solicitante.correo && solicitante.correo.toLowerCase().includes(busqueda)) ||
             (solicitante.programa && solicitante.programa.toLowerCase().includes(busqueda));
    });
  };

  const solicitantesFiltrados = filtrarSolicitantes();

  const obtenerNombreCompleto = (solicitante) => {
    return [
      solicitante.primer_nombre,
      solicitante.segundo_nombre,
      solicitante.primer_apellido,
      solicitante.segundo_apellido
    ].filter(Boolean).join(' ');
  };

  return (
    <div className="selector-solicitantes">
      <div className="selector-header">
        <h3>Seleccionar Solicitante</h3>
        <div className="filtro-busqueda">
          <input
            type="text"
            placeholder="Buscar por nombre, identificación, correo o programa..."
            value={filtroBusqueda}
            onChange={(e) => setFiltroBusqueda(e.target.value)}
            className="form-control"
          />
        </div>
      </div>

      <div className="solicitantes-grid">
        {solicitantesFiltrados.length > 0 ? (
          solicitantesFiltrados.map(solicitante => (
            <div 
              key={solicitante.identificacion} 
              className={`solicitante-card ${solicitanteSeleccionado?.identificacion === solicitante.identificacion ? 'selected' : ''}`}
              onClick={() => onSelectSolicitante(solicitante)}
            >
              <div className="solicitante-avatar">
                <i className="material-symbols-outlined">person</i>
              </div>
              <div className="solicitante-info">
                <h4>{obtenerNombreCompleto(solicitante)}</h4>
                <p className="identificacion">{solicitante.identificacion}</p>
                {solicitante.programa && (
                  <p className="programa">{solicitante.programa}</p>
                )}
              </div>
              {solicitanteSeleccionado?.identificacion === solicitante.identificacion && (
                <div className="selected-indicator">
                  <i className="material-symbols-outlined">check_circle</i>
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="no-solicitantes">
            <i className="material-symbols-outlined">person_search</i>
            <p>No se encontraron solicitantes con los criterios de búsqueda</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SelectorSolicitantes;
