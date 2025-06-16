import React, { useState } from 'react';
import '../styles/components/SelectorProductos.css';

const SelectorProductos = ({ productos, tiposProducto, onAddToCart }) => {
  const [filtroTipo, setFiltroTipo] = useState('');
  const [filtroBusqueda, setFiltroBusqueda] = useState('');

  const getTipoProductoNombre = (idTipo) => {
    const tipo = tiposProducto.find(t => t.IDTIPOPRODUCTO === idTipo);
    return tipo ? tipo.NOMBRE_TIPO_PRODUCTO : 'Desconocido';
  };

  const filtrarProductos = () => {
    return productos.filter(producto => {
      const matchTipo = filtroTipo === '' || producto.IDTIPOPRODUCTO.toString() === filtroTipo;
      const matchBusqueda = filtroBusqueda === '' ||
        producto.NOMBRE.toLowerCase().includes(filtroBusqueda.toLowerCase()) ||
        producto.CODIGO_INTERNO.toLowerCase().includes(filtroBusqueda.toLowerCase()) ||
        (producto.PLACA_SENA && producto.PLACA_SENA.toLowerCase().includes(filtroBusqueda.toLowerCase()));

      return matchTipo && matchBusqueda && producto.ESTADO === 'Disponible';
    });
  };

  const productosDisponibles = filtrarProductos();

  return (
    <div className="selector-productos">
      <div className="selector-header">
        <h3>Productos Disponibles</h3>
        <div className="filtros">
          <input
            type="text"
            placeholder="Buscar por nombre, código o placa..."
            value={filtroBusqueda}
            onChange={(e) => setFiltroBusqueda(e.target.value)}
            className="form-control"
          />
          <select
            value={filtroTipo}
            onChange={(e) => setFiltroTipo(e.target.value)}
            className="form-control"
          >
            <option value="">Todos los tipos</option>
            {tiposProducto.map(tipo => (
              <option key={tipo.IDTIPOPRODUCTO} value={tipo.IDTIPOPRODUCTO.toString()}>
                {tipo.NOMBRE_TIPO_PRODUCTO}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="productos-grid">
        {productosDisponibles.length > 0 ? (
          productosDisponibles.map(producto => (
            <div key={producto.IDPRODUCTO} className="producto-card">
              <div className="producto-info">
                <h4>{producto.NOMBRE}</h4>
                <p className="codigo">{producto.CODIGO_INTERNO}</p>
                <p className="tipo">{getTipoProductoNombre(producto.IDTIPOPRODUCTO)}</p>
              </div>
              <div className="producto-actions">
                <button
                  className="btn btn-primary"
                  onClick={() => onAddToCart(producto)}
                >
                  Agregar
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="no-productos">
            <i className="material-symbols-outlined">inventory_2</i>
            <p>No hay productos disponibles con los filtros seleccionados</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SelectorProductos;
