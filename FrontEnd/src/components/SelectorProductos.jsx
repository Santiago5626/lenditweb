import React, { useState } from 'react';
import '../styles/components/SelectorProductos.css';
import '../styles/global-inputs.css';

const SelectorProductos = ({ productos, tiposProducto, onAddToCart, selectedProducts = [], onRemoveProduct }) => {
  const [filtroCodigo, setFiltroCodigo] = useState('');
  const [filtroBusqueda, setFiltroBusqueda] = useState('');

  const getTipoProductoNombre = (idTipo) => {
    const tipo = tiposProducto.find(t => t.IDTIPOPRODUCTO === idTipo);
    return tipo ? tipo.NOMBRE_TIPO_PRODUCTO : 'Desconocido';
  };

  const filtrarProductos = () => {
    return productos.filter(producto => {
      const matchCodigo = filtroCodigo === '' ||
        producto.CODIGO_INTERNO.toLowerCase().includes(filtroCodigo.toLowerCase());
      const matchBusqueda = filtroBusqueda === '' ||
        producto.NOMBRE.toLowerCase().includes(filtroBusqueda.toLowerCase()) ||
        (producto.PLACA_SENA && producto.PLACA_SENA.toLowerCase().includes(filtroBusqueda.toLowerCase()));

      return matchCodigo && matchBusqueda && producto.ESTADO === 'Disponible';
    });
  };

  const productosDisponibles = filtrarProductos();

  const isProductSelected = (producto) => {
    return selectedProducts.some(p => p.IDPRODUCTO === producto.IDPRODUCTO);
  };

  return (
    <div className="selector-productos">
      <div className="selector-header">
        <h3>Productos Disponibles</h3>
        <div className="filtros">
          <input
            type="text"
            placeholder="Buscar por nombre o placa..."
            value={filtroBusqueda}
            onChange={(e) => setFiltroBusqueda(e.target.value)}
            className="input-standard"
          />
          <input
            type="text"
            placeholder="Buscar por código..."
            value={filtroCodigo}
            onChange={(e) => setFiltroCodigo(e.target.value)}
            className="input-standard"
          />
        </div>
      </div>

      <div className="productos-grid">
        {productosDisponibles.length > 0 ? (
          productosDisponibles.map(producto => {
            const isSelected = isProductSelected(producto);
            return (
              <div key={producto.IDPRODUCTO} className={`producto-card ${isSelected ? 'selected' : ''}`}>
                <div className="producto-info">
                  <h4>{producto.NOMBRE}</h4>
                  <p className="codigo">{producto.CODIGO_INTERNO}</p>
                  <p className="tipo">{getTipoProductoNombre(producto.IDTIPOPRODUCTO)}</p>
                </div>
                <div className="producto-actions">
                  <button
                    className={`btn ${isSelected ? 'btn-danger' : 'btn-primary'}`}
                    onClick={() => isSelected ? onRemoveProduct(producto) : onAddToCart(producto)}
                  >
                    {isSelected ? 'Quitar' : 'Agregar'}
                  </button>
                </div>
              </div>
            );
          })
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
