import React, { useState, useEffect } from "react";
import "./RegistrarModal.css";

const EditarModal = ({ show, onClose, onEdit, userData }) => {
  const [cc, setCC] = useState("");
  const [nombre, setNombre] = useState("");
  const [apellido, setApellido] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    if (userData) {
      setCC(userData.cc || "");
      setNombre(userData.nombre || "");
      setApellido(userData.apellido || "");
      setEmail(userData.email || "");
    }
  }, [userData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onEdit({ cc, nombre, apellido, email });
    onClose();
  };

  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Editar Estudiante</h2>
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            id="cc"
            name="cc"
            placeholder="Cédula"
            required
            className="form-control"
            value={cc}
            onChange={(e) => setCC(e.target.value)}
          />
          <input
            type="text"
            id="nombre"
            name="nombre"
            placeholder="Nombre"
            required
            className="form-control"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
          />
          <input
            type="text"
            id="apellido"
            name="apellido"
            placeholder="Apellido"
            required
            className="form-control"
            value={apellido}
            onChange={(e) => setApellido(e.target.value)}
          />
          <input
            type="email"
            id="email"
            name="email"
            placeholder="Correo electrónico"
            required
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button type="submit" className="btn btn-primary">Actualizar</button>
        </form>
      </div>
    </div>
  );
};

export default EditarModal;
