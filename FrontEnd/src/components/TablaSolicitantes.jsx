import React, { useState, useEffect } from "react";
import { fetchSolicitantes, agregar, actualizar, eliminar, checkServerStatus } from "../api/peticiones";
import RegistrarModal from "./RegistrarModal";
import EditarModal from "./EditarModal";
import "./TablaSolicitantes.css";

const TablaSolicitantes = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [serverStatus, setServerStatus] = useState(true);
  const [filtroId, setFiltroId] = useState("");
  const [filtroFicha, setFiltroFicha] = useState("");

  const verificarServidor = async () => {
    const isServerUp = await checkServerStatus();
    setServerStatus(isServerUp);
    return isServerUp;
  };

  useEffect(() => {
  const fetchUsuarios = async () => {
    try {
      setLoading(true);
      setError(null);

      const isServerUp = await checkServerStatus();
      setServerStatus(isServerUp);

      if (!isServerUp) {
        setError("No se puede conectar al servidor.");
        return;
      }

      const data = await fetchSolicitantes();
      setUsuarios(data);
    } catch (error) {
      console.error("Error al cargar usuarios:", error);
      setError(error.message || "Error al cargar los datos");
    } finally {
      setLoading(false);
    }
  };

  fetchUsuarios();
}, []);

  const handleRegister = async (solicitanteData) => {
    try {
      await agregar(solicitanteData);
      alert("¡Solicitante agregado exitosamente!");
      setShowModal(false);
      const data = await fetchSolicitantes();
      setUsuarios(data);
    } catch (error) {
      console.error("Error al registrar:", error);
      alert("Error al agregar solicitante: " + error.message);
    }
  };

  const handleEdit = async (solicitanteData) => {
    try {
      await actualizar(solicitanteData);
      alert("¡Solicitante actualizado exitosamente!");
      setShowEditModal(false);
      const data = await fetchSolicitantes();
      setUsuarios(data);
      setSelectedUser(null);
    } catch (error) {
      console.error("Error al actualizar:", error);
      alert("Error al actualizar solicitante: " + error.message);
    }
  };

  const handleDelete = async () => {
    if (!selectedUser) {
      alert("Por favor seleccione un solicitante para eliminar");
      return;
    }

    if (window.confirm(`¿Está seguro que desea eliminar a ${selectedUser.primer_nombre} ${selectedUser.primer_apellido}?`)) {
      try {
        await eliminar(selectedUser.identificacion);
        alert("¡Solicitante eliminado exitosamente!");
        const data = await fetchSolicitantes();
        setUsuarios(data);
        setSelectedUser(null);
      } catch (error) {
        console.error("Error al eliminar:", error);
        alert("Error al eliminar solicitante: " + error.message);
      }
    }
  };

  const handleCheckboxChange = (user) => {
    setSelectedUser(user === selectedUser ? null : user);
  };

  const handleEditClick = () => {
    if (!selectedUser) {
      alert("Por favor seleccione un solicitante para editar");
      return;
    }
    setShowEditModal(true);
  };

  const handleRetry = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchSolicitantes();
      setUsuarios(data);
      setLoading(false);
    } catch (error) {
      console.error("Error al cargar usuarios:", error);
      setError(error.message || "Error al cargar los datos");
      setLoading(false);
    }
  };

  const filtrarUsuarios = () => {
    return usuarios.filter(user => {
      const matchId = user.identificacion.toLowerCase().includes(filtroId.toLowerCase());
      const matchFicha = user.ficha?.toLowerCase().includes(filtroFicha.toLowerCase()) ?? true;
      return matchId && matchFicha;
    });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
        <p>Cargando solicitantes...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container alert alert-danger">
        <h4>Error al cargar los datos</h4>
        <p>{error}</p>
        <button 
          className="btn btn-primary mt-3" 
          onClick={handleRetry}
        >
          Intentar nuevamente
        </button>
      </div>
    );
  }

  if (!serverStatus) {
    return (
      <div className="error-container alert alert-warning">
        <h4>Error de conexión</h4>
        <h4>Error de conexión</h4>
        <p>No se puede conectar al servidor. Por favor, verifica que el servidor esté corriendo.</p>
        <button 
          className="btn btn-primary mt-3" 
          onClick={verificarServidor}
        >
          Verificar conexión
        </button>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="controls-section">
        <div className="filters">
          <input
            type="text"
            className="form-control"
            placeholder="Filtrar por Identificación"
            value={filtroId}
            onChange={(e) => setFiltroId(e.target.value)}
          />
          <input
            type="text"
            className="form-control"
            placeholder="Filtrar por Ficha"
            value={filtroFicha}
            onChange={(e) => setFiltroFicha(e.target.value)}
          />
        </div>
        <div className="buttons">
          <button 
            className="btn btn-outline-danger"
            onClick={handleDelete}
            title="Eliminar solicitante"
          >
            <span className="material-symbols-outlined">delete</span>
          </button>
          <button 
            className="btn btn-outline-primary"
            onClick={handleEditClick}
            title="Editar solicitante"
          >
            <span className="material-symbols-outlined">person_edit</span>
          </button>
          <button 
            className="btn btn-outline-success" 
            onClick={() => setShowModal(true)}
            title="Agregar solicitante"
          >
            <span className="material-symbols-outlined">person_add</span>
          </button>
        </div>
      </div>

      <div className="table-section">
        {usuarios.length === 0 ? (
          <div className="alert alert-info">
            No hay solicitantes registrados
          </div>
        ) : (
          <table className="table table-bordered table-hover">
            <thead className="thead-light">
              <tr>
                <th>Seleccionar</th>
                <th>Identificación</th>
                <th>Primer Nombre</th>
                <th>Primer Apellido</th>
                <th>Segundo Apellido</th>
                <th>Teléfono</th>
                <th>Correo</th>
                <th>Ficha</th>
                <th>Programa</th>
              </tr>
            </thead>
            <tbody>
              {filtrarUsuarios().map((user, index) => (
                <tr 
                  key={user.identificacion || index}
                  className={selectedUser === user ? "table-active" : ""}
                >
                  <td>
                    <input 
                      type="checkbox" 
                      checked={selectedUser === user}
                      onChange={() => handleCheckboxChange(user)}
                    />
                  </td>
                  <td>{user.identificacion}</td>
                  <td>{user.primer_nombre}</td>
                  <td>{user.primer_apellido}</td>
                  <td>{user.segundo_apellido || '-'}</td>
                  <td>{user.telefono}</td>
                  <td>{user.correo}</td>
                  <td>{user.ficha || '-'}</td>
                  <td>{user.programa || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
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

export default TablaSolicitantes;
