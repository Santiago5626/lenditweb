import React, { useState } from "react";
import "./RegistrarModal.css";

const RegistrarModal = ({ show, onClose, onRegister }) => {
  const [formData, setFormData] = useState({
    identificacion: "",
    primer_nombre: "",
    segundo_nombre: "",
    primer_apellido: "",
    segundo_apellido: "",
    correo: "",
    telefono: "",
    genero: "M",
    rol: "aprendiz",
    ficha: "",
    programa: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dataToSubmit = {
      ...formData,
      // Si el rol es empleado, no enviamos ficha ni programa
      ...(formData.rol !== 'aprendiz' && { ficha: undefined, programa: undefined })
    };
    await onRegister(dataToSubmit);
    // Limpiar el formulario
    setFormData({
      identificacion: "",
      primer_nombre: "",
      segundo_nombre: "",
      primer_apellido: "",
      segundo_apellido: "",
      correo: "",
      telefono: "",
      genero: "M",
      rol: "aprendiz",
      ficha: "",
      programa: ""
    });
  };

  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Registrar Solicitante</h2>
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="identificacion"
            placeholder="Identificación"
            required
            className="form-control"
            value={formData.identificacion}
            onChange={handleChange}
          />
          <input
            type="text"
            name="primer_nombre"
            placeholder="Primer Nombre"
            required
            className="form-control"
            value={formData.primer_nombre}
            onChange={handleChange}
          />
          <input
            type="text"
            name="segundo_nombre"
            placeholder="Segundo Nombre"
            className="form-control"
            value={formData.segundo_nombre}
            onChange={handleChange}
          />
          <input
            type="text"
            name="primer_apellido"
            placeholder="Primer Apellido"
            required
            className="form-control"
            value={formData.primer_apellido}
            onChange={handleChange}
          />
          <input
            type="text"
            name="segundo_apellido"
            placeholder="Segundo Apellido"
            className="form-control"
            value={formData.segundo_apellido}
            onChange={handleChange}
          />
          <input
            type="email"
            name="correo"
            placeholder="Correo electrónico"
            required
            className="form-control"
            value={formData.correo}
            onChange={handleChange}
          />
          <input
            type="tel"
            name="telefono"
            placeholder="Teléfono"
            required
            className="form-control"
            value={formData.telefono}
            onChange={handleChange}
          />
          <select
            name="rol"
            className="form-control"
            value={formData.rol}
            onChange={handleChange}
            required
          >
            <option value="aprendiz">Aprendiz</option>
            <option value="contratista">Contratista</option>
            <option value="funcionario">Funcionario</option>
            <option value="instructor">Instructor</option>
          </select>
          
          {formData.rol === 'aprendiz' && (
            <>
              <input
                type="text"
                name="ficha"
                placeholder="Ficha"
                required
                className="form-control"
                value={formData.ficha}
                onChange={handleChange}
              />
              <input
                type="text"
                name="programa"
                placeholder="Programa"
                required
                className="form-control"
                value={formData.programa}
                onChange={handleChange}
              />
            </>
          )}
          
          <button type="submit" className="btn btn-primary">Registrar</button>
        </form>
      </div>
    </div>
  );
};

export default RegistrarModal;
