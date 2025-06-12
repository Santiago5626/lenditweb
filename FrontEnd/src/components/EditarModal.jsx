import React, { useState, useEffect } from "react";
import "../styles/components/RegistrarModal.css";

const EditarModal = ({ show, onClose, onEdit, userData }) => {
  const [formData, setFormData] = useState({
    identificacion: "",
    primer_nombre: "",
    segundo_nombre: "",
    primer_apellido: "",
    segundo_apellido: "",
    correo: "",
    telefono: "",
    rol: "aprendiz",
    ficha: "",
    programa: ""
  });

  useEffect(() => {
    if (userData) {
      setFormData({
        identificacion: userData.identificacion || "",
        primer_nombre: userData.primer_nombre || "",
        segundo_nombre: userData.segundo_nombre || "",
        primer_apellido: userData.primer_apellido || "",
        segundo_apellido: userData.segundo_apellido || "",
        correo: userData.correo || "",
        telefono: userData.telefono || "",
        genero: userData.genero || "M",
        rol: userData.rol || "aprendiz",
        ficha: userData.ficha || "",
        programa: userData.programa || ""
      });
    }
  }, [userData]);

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
    await onEdit(dataToSubmit);
  };

  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Editar Solicitante</h2>
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
            readOnly
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
            name="genero"
            className="form-control"
            value={formData.genero}
            onChange={handleChange}
            required
          >
            <option value="M">Masculino</option>
            <option value="F">Femenino</option>
            <option value="O">Otro</option>
          </select>
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
          
          <button type="submit" className="btn btn-primary">Actualizar</button>
        </form>
      </div>
    </div>
  );
};

export default EditarModal;
