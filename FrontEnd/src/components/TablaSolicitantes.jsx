import React, { useState, useEffect } from "react";
import { fetchSolicitantes, agregar, actualizar, eliminar } from "../api/peticiones";
import RegistrarModal from "./RegistrarModal";
import EditarModal from "./EditarModal";
import ImportarSolicitantesModal from "./ImportarSolicitantesModal";
import TablaSolicitantesTable from "./TablaSolicitantesTable";
import "./TablaSolicitantes.css";

const TablaSolicitantes = () => {
  const [usuarios, setUsuarios] = useState([]);

  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [filtroId, setFiltroId] = useState("");
  const [filtroFicha, setFiltroFicha] = useState("");

  const fetchUsuarios = async () => {
    try {
      const data = await fetchSolicitantes();
      setUsuarios(data);
    } catch (error) {
      console.error("Error al cargar usuarios:", error);
    }
  };

  useEffect(() => {
    fetchUsuarios();
  }, []);

  const handleRegister = async (solicitanteData) => {
    try {
      await agregar(solicitanteData);
      alert("¡Solicitante agregado exitosamente!");
      setShowModal(false);
      fetchUsuarios();
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
      fetchUsuarios();
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
        fetchUsuarios();
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

  const filtrarUsuarios = () => {
    return usuarios.filter(user => {
      const matchId = user.identificacion.toLowerCase().includes(filtroId.toLowerCase());
      const matchFicha = user.ficha?.toLowerCase().includes(filtroFicha.toLowerCase()) ?? true;
      return matchId && matchFicha;
    });
  };

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
          <button
            className="btn btn-outline-primary"
            onClick={() => setShowImportModal(true)}
            title="Importar solicitantes"
          >
            <span className="material-symbols-outlined">upload_file</span>
          </button>
        </div>
      </div>

      <TablaSolicitantesTable
        usuarios={filtrarUsuarios()}
        selectedUser={selectedUser}
        onCheckboxChange={handleCheckboxChange}
        onRetry={fetchUsuarios}
      />

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

      <ImportarSolicitantesModal
        show={showImportModal}
        onClose={() => setShowImportModal(false)}
        onImportComplete={fetchUsuarios}
      />
    </div>
  );
};

export default TablaSolicitantes;