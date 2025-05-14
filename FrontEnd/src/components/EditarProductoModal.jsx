import React, { useState, useEffect } from 'react';
import './RegistrarModal.css';

const EditarProductoModal = ({ show, onClose, onEdit, productData }) => {
  const [formData, setFormData] = useState({
    codigoInterno: '',
    codigoSena: '',
    serial: '',
    nombreProducto: '',
    marca: '',
    descripcion: '',
    estado: 'Disponible',
    idTipoProducto: '1'
  });

  useEffect(() => {
    if (productData) {
      setFormData({
        codigoInterno: productData.codigoInterno || '',
        codigoSena: productData.codigoSena || '',
        serial: productData.serial || '',
        nombreProducto: productData.nombreProducto || '',
        marca: productData.marca || '',
        descripcion: productData.descripcion || '',
        estado: productData.estado || 'Disponible',
        idTipoProducto: productData.idTipoProducto.toString() || '1'
      });
    }
  }, [productData]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onEdit(formData);
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
          <h2>Editar Producto</h2>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="codigoInterno">Código Interno*</label>
            <input
              type="text"
              id="codigoInterno"
              name="codigoInterno"
              value={formData.codigoInterno}
              onChange={handleChange}
              required
              className="form-control"
              readOnly
            />
          </div>

          <div className="form-group">
            <label htmlFor="nombreProducto">Nombre del Producto*</label>
            <input
              type="text"
              id="nombreProducto"
              name="nombreProducto"
              value={formData.nombreProducto}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label htmlFor="idTipoProducto">Tipo de Producto*</label>
            <select
              id="idTipoProducto"
              name="idTipoProducto"
              value={formData.idTipoProducto}
              onChange={handleChange}
              required
              className="form-control"
            >
              <option value="1">Equipo</option>
              <option value="2">Accesorio</option>
            </select>
          </div>

          {formData.idTipoProducto === '1' && (
            <>
              <div className="form-group">
                <label htmlFor="codigoSena">PLACA SENA</label>
                <input
                  type="text"
                  id="codigoSena"
                  name="codigoSena"
                  value={formData.codigoSena}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label htmlFor="serial">Serial</label>
                <input
                  type="text"
                  id="serial"
                  name="serial"
                  value={formData.serial}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label htmlFor="marca">Marca</label>
                <input
                  type="text"
                  id="marca"
                  name="marca"
                  value={formData.marca}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label htmlFor="estado">Estado*</label>
            <select
              id="estado"
              name="estado"
              value={formData.estado}
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
            <label htmlFor="descripcion">Observaciones</label>
            <textarea
              id="descripcion"
              name="descripcion"
              value={formData.descripcion}
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
              Guardar Cambios
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditarProductoModal;
