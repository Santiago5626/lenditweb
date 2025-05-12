import React, { useState } from "react";
import "./RegistrarModal.css";

const RegistrarModal = ({ show, onClose, onRegister }) => {
  const [cc, setCC] = useState("");
  const [nombre, setNombre] = useState("");
  const [apellido, setApellidpp] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onRegister({ cc, nombre, apellido, email });
    setCC("");
    setNombre("");
    setApellidpp("");
    setEmail("");
  };

  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            id="cc"
            name="cc"
            placeholder="Cedula"
            required
            className="form-control"
            value={cc}
            onChange={(e) => setCC(e.target.value)}
          />
          <input
            type="text"
            id="nombre"
            name="nombre"
            placeholder="Usuario"
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
            onChange={(e) => setApellidpp(e.target.value)}
          />
          <input
            type="email"
            id="email"
            name="email"
            placeholder="email"
            required
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button type="submit">AGREGAR</button>
        </form>
      </div>
    </div>
  );
};

export default RegistrarModal;
