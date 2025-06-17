import React, { useState, useEffect } from 'react';
import '../styles/components/RegistrarModal.css';
import { fetchTiposProducto } from '../api/peticiones';

const RegistrarProductoModal = ({ show, onClose, onRegister }) => {
  const [formData, setFormData] = useState({
    CODIGO_INTERNO: '',
    NOMBRE: '',
    IDTIPOPRODUCTO: '1',
    PLACA_SENA: '',
    SERIAL: '',
    MARCA: '',
    ESTADO: 'Disponible',
    OBSERVACIONES: ''
  });

  const [tiposProducto, setTiposProducto] = useState([]);

  useEffect(() => {
    const cargarTiposProducto = async () => {
      try {
        const tipos = await fetchTiposProducto();
        setTiposProducto(tipos);
      } catch (error) {
        console.error('Error al cargar tipos de producto:', error);
      }
    };

    if (show) {
      cargarTiposProducto();
    }
  }, [show]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onRegister(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  if (!show) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Registrar Nuevo Producto</h2>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="CODIGO_INTERNO">Código Interno*</label>
            <input
              type="text"
              id="CODIGO_INTERNO"
              name="CODIGO_INTERNO"
              value={formData.CODIGO_INTERNO}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label htmlFor="NOMBRE">Nombre del Producto*</label>
            <input
              type="text"
              id="NOMBRE"
              name="NOMBRE"
              value={formData.NOMBRE}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label htmlFor="IDTIPOPRODUCTO">Tipo de Producto*</label>
            <select
              id="IDTIPOPRODUCTO"
              name="IDTIPOPRODUCTO"
              value={formData.IDTIPOPRODUCTO}
              onChange={handleChange}
              required
              className="form-control"
            >
              {tiposProducto.map(tipo => (
                <option key={tipo.IDTIPOPRODUCTO} value={tipo.IDTIPOPRODUCTO.toString()}>
                  {tipo.NOMBRE_TIPO_PRODUCTO}
                </option>
              ))}
            </select>
          </div>

          {/* Solo mostrar campos adicionales para equipo de cómputo */}
          {tiposProducto.find(t => t.IDTIPOPRODUCTO === parseInt(formData.IDTIPOPRODUCTO))?.NOMBRE_TIPO_PRODUCTO === "equipo de cómputo" && (
            <>
              <div className="form-group">
                <label htmlFor="PLACA_SENA">PLACA SENA</label>
                <input
                  type="text"
                  id="PLACA_SENA"
                  name="PLACA_SENA"
                  value={formData.PLACA_SENA}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label htmlFor="SERIAL">Serial</label>
                <input
                  type="text"
                  id="SERIAL"
                  name="SERIAL"
                  value={formData.SERIAL}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label htmlFor="MARCA">Marca</label>
                <input
                  type="text"
                  id="MARCA"
                  name="MARCA"
                  value={formData.MARCA}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label htmlFor="ESTADO">Estado*</label>
            <select
              id="ESTADO"
              name="ESTADO"
              value={formData.ESTADO}
              onChange={handleChange}
              required
              className="form-control"
            >
              <option value="Disponible">Disponible</option>
              <option value="En Préstamo">En Préstamo</option>
              <option value="En Mantenimiento">En Mantenimiento</option>
              <option value="Fuera de Servicio">Fuera de Servicio</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="OBSERVACIONES">Observaciones</label>
            <textarea
              id="OBSERVACIONES"
              name="OBSERVACIONES"
              value={formData.OBSERVACIONES}
              onChange={handleChange}
              className="form-control"
              rows="3"
            />
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit" className="btn btn-primary">
              Registrar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegistrarProductoModal;
