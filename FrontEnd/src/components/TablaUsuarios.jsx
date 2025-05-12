import React, { useState, useEffect } from "react";
import { fetchSolicitantes, agregar, actualizar, eliminar } from "../api/peticiones";
import RegistrarModal from "./RegistrarModal";
import EditarModal from "./EditarModal";

import "./TablaUsuarios.css";

const TablaUsuarios = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  const fetchUsuarios = async () => {
    try {
      const data = await fetchSolicitantes(
        "http://127.0.0.1:8000/estudiantes/obtener"
      );
      setUsuarios(data);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsuarios();
  }, []);

  const handleRegister = async ({ cc, nombre, apellido, email }) => {
    try {
      await agregar(cc, nombre, apellido, email);
      alert("¡Estudiante agregado exitosamente!");
      setShowModal(false);
      await fetchUsuarios();
    } catch (error) {
      alert("Error al agregar estudiante: " + error.message);
    }
  };

  const handleEdit = async ({ cc, nombre, apellido, email }) => {
    try {
      await actualizar(cc, nombre, apellido, email);
      alert("¡Estudiante actualizado exitosamente!");
      setShowEditModal(false);
      await fetchUsuarios();
      setSelectedUser(null);
    } catch (error) {
      alert("Error al actualizar estudiante: " + error.message);
    }
  };

  const handleDelete = async () => {
    if (!selectedUser) {
      alert("Por favor seleccione un estudiante para eliminar");
      return;
    }

    if (window.confirm(`¿Está seguro que desea eliminar al estudiante ${selectedUser.nombre} ${selectedUser.apellido}?`)) {
      try {
        await eliminar(selectedUser.cc);
        alert("¡Estudiante eliminado exitosamente!");
        await fetchUsuarios();
        setSelectedUser(null);
      } catch (error) {
        alert("Error al eliminar estudiante: " + error.message);
      }
    }
  };

  const handleCheckboxChange = (user) => {
    setSelectedUser(user === selectedUser ? null : user);
  };

  const handleEditClick = () => {
    if (!selectedUser) {
      alert("Por favor seleccione un estudiante para editar");
      return;
    }
    setShowEditModal(true);
  };

  if (loading) {
    return <div>Cargando estudiantes...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="container">
      <div className="controls-section">
        <input
          type="text"
          className="form-control"
          placeholder="Número de ID"
        />
        <input 
          type="text" 
          className="form-control" 
          placeholder="Ficha" 
        />
        <button 
          className="btn btn-outline-danger"
          onClick={handleDelete}
          title="Eliminar estudiante"
        >
          <span className="material-symbols-outlined">delete</span>
        </button>
        <button 
          className="btn btn-outline-primary"
          onClick={handleEditClick}
          title="Editar estudiante"
        >
          <span className="material-symbols-outlined">person_edit</span>
        </button>
        <button 
          className="btn btn-outline-success" 
          onClick={() => setShowModal(true)}
          title="Agregar estudiante"
        >
          <span className="material-symbols-outlined">person_add</span>
        </button>
      </div>

      <div className="table-section">
        <table className="table table-bordered table-hover">
          <thead className="thead-light">
            <tr>
              <th>Seleccionar</th>
              <th>Cédula</th>
              <th>Nombre</th>
              <th>Apellido</th>
              <th>Correo</th>
            </tr>
          </thead>
          <tbody>
            {usuarios.map((user, index) => (
              <tr 
                key={index}
                className={selectedUser === user ? "table-active" : ""}
              >
                <td>
                  <input 
                    type="checkbox" 
                    checked={selectedUser === user}
                    onChange={() => handleCheckboxChange(user)}
                  />
                </td>
                <td>{user.cc}</td>
                <td>{user.nombre}</td>
                <td>{user.apellido}</td>
                <td>{user.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <RegistrarModal
        show={showModal}
        onClose={() => setShowModal(false)}
        onRegister={handleRegister}
      />

      <EditarModal
        show={showEditModal}
        onClose={() => {
          setShowEditModal(false);
          setSelectedUser(null);
        }}
        onEdit={handleEdit}
        userData={selectedUser}
      />
    </div>
  );
};

export default TablaUsuarios;
