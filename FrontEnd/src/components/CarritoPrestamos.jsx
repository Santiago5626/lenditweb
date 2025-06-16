import React from 'react';
import '../styles/components/CarritoPrestamos.css';

const CarritoPrestamos = ({ 
  items, 
  solicitanteSeleccionado, 
  onRemoveItem, 
  onClear, 
  onConfirm,
  fechaLimite,
  onFechaLimiteChange 
}) => {
  if (!solicitanteSeleccionado && items.length === 0) {
    return null;
  }

  const obtenerNombreProducto = (producto) => {
    return `${producto.NOMBRE} (${producto.CODIGO_INTERNO})`;
  };

  return (
    <div className="carrito-prestamos">
      <div className="carrito-header">
        <h3>Carrito de Préstamos</h3>
        {items.length > 0 && (
          <button className="btn btn-outline-danger btn-sm" onClick={onClear}>
            <i className="material-symbols-outlined">remove_shopping_cart</i>
            Limpiar
          </button>
        )}
      </div>

      {solicitanteSeleccionado && (
        <div className="solicitante-info">
          <h4>Solicitante:</h4>
          <p>
            {solicitanteSeleccionado.primer_nombre} {solicitanteSeleccionado.primer_apellido}
            <br />
            <small>ID: {solicitanteSeleccionado.identificacion}</small>
          </p>
        </div>
      )}

      {items.length > 0 ? (
        <>
          <div className="productos-lista">
            <h4>Productos seleccionados:</h4>
            <ul>
              {items.map((producto) => (
                <li key={producto.IDPRODUCTO}>
                  <span>{obtenerNombreProducto(producto)}</span>
                  <button
                    className="btn btn-outline-danger btn-sm"
                    onClick={() => onRemoveItem(producto)}
                  >
                    <i className="material-symbols-outlined">remove_circle</i>
                  </button>
                </li>
              ))}
            </ul>
          </div>

          <div className="fecha-devolucion">
            <label htmlFor="fechaLimite">Fecha de devolución:</label>
            <input
              type="date"
              id="fechaLimite"
              value={fechaLimite}
              onChange={(e) => onFechaLimiteChange(e.target.value)}
              min={new Date().toISOString().split('T')[0]}
              required
            />
          </div>

          <div className="carrito-footer">
            <button 
              className="btn btn-primary"
              onClick={onConfirm}
              disabled={!fechaLimite || !solicitanteSeleccionado}
            >
              <i className="material-symbols-outlined">check_circle</i>
              Confirmar Préstamos
            </button>
          </div>
        </>
      ) : (
        <div className="carrito-vacio">
          <i className="material-symbols-outlined">shopping_cart</i>
          <p>No hay productos seleccionados</p>
        </div>
      )}
    </div>
  );
};

export default CarritoPrestamos;
