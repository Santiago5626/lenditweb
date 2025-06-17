import React, { useState, useEffect, useCallback, useMemo } from "react";
import { fetchSolicitantes, agregar, actualizar, eliminar } from "../api/peticiones";
import RegistrarModal from "./RegistrarModal";
import EditarModal from "./EditarModal";
import ImportarSolicitantesModal from "./ImportarSolicitantesModal";
import TablaSolicitantesTableSimple from "./TablaSolicitantesTableSimple";
import "../styles/components/TablaSolicitantes.css";
import "../styles/global-inputs.css";

const PanelSolicitante = () => {
    const [usuarios, setUsuarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState(true);

    const [showModal, setShowModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [showImportModal, setShowImportModal] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const [filtroId, setFiltroId] = useState("");
    const [filtroFicha, setFiltroFicha] = useState("");

    // Estados para paginación
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);

    const fetchUsuarios = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchSolicitantes();
            setUsuarios(data);
            setServerStatus(true);
        } catch (error) {
            console.error("Error al cargar usuarios:", error);
            setError(error.message);
            if (error.message.includes("Failed to fetch") || error.message.includes("Network Error")) {
                setServerStatus(false);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleVerificarServidor = () => {
        fetchUsuarios();
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

    // Función para filtrar y ordenar usuarios con memoización
    const usuariosFiltrados = useMemo(() => {
        if (!Array.isArray(usuarios)) {
            return [];
        }

        // Primero filtramos
        const filtrados = usuarios.filter(user => {
            const matchId = user.identificacion?.toLowerCase().includes(filtroId.toLowerCase()) ?? true;
            const matchFicha = filtroFicha === "" ||
                (user.rol === 'aprendiz' && user.ficha && user.ficha.toString().toLowerCase().includes(filtroFicha.toLowerCase()));
            return matchId && matchFicha;
        });

        // Luego invertimos el orden para mostrar los últimos primero
        return [...filtrados].reverse();
    }, [usuarios, filtroId, filtroFicha]);

    // Calcular total de items y páginas
    const totalItems = useMemo(() => {
        return usuariosFiltrados.length;
    }, [usuariosFiltrados]);

    const totalPages = useMemo(() => {
        return Math.max(1, Math.ceil(totalItems / itemsPerPage));
    }, [totalItems, itemsPerPage]);

    // Calcular usuarios paginados
    const usuariosPaginados = useMemo(() => {
        if (!Array.isArray(usuariosFiltrados) || usuariosFiltrados.length === 0) {
            return [];
        }

        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, totalItems);
        return usuariosFiltrados.slice(startIndex, endIndex);
    }, [usuariosFiltrados, currentPage, itemsPerPage, totalItems]);

    // Handler para cambiar de página
    const handlePageChange = useCallback((page) => {
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
            setSelectedUser(null);
        }
    }, [totalPages]);

    // Handler para cambiar items por página
    const handleItemsPerPageChange = useCallback((newItemsPerPage) => {
        setItemsPerPage(newItemsPerPage);
        setCurrentPage(1);
        setSelectedUser(null);
    }, []);

    // Asegurarnos de que currentPage sea válido
    useEffect(() => {
        const maxPage = Math.max(1, totalPages);
        if (currentPage > maxPage) {
            setCurrentPage(1);
        }
    }, [currentPage, totalPages]);

    // Resetear página cuando se aplican filtros
    const handleFiltroIdChange = (value) => {
        setFiltroId(value);
        setCurrentPage(1);
        setSelectedUser(null);
    };

    const handleFiltroFichaChange = (value) => {
        setFiltroFicha(value);
        setCurrentPage(1);
        setSelectedUser(null);
    };

    return (
        <div className="container">
            <div className="controls-section">
                <div className="filters">
                    <input
                        type="text"
                        className="input-standard"
                        placeholder="Filtrar por Identificación"
                        value={filtroId}
                        onChange={(e) => handleFiltroIdChange(e.target.value)}
                    />
                    <input
                        type="text"
                        className="input-standard"
                        placeholder="Filtrar por Ficha"
                        value={filtroFicha}
                        onChange={(e) => handleFiltroFichaChange(e.target.value)}
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

            <TablaSolicitantesTableSimple
                usuarios={usuariosPaginados}
                selectedUser={selectedUser}
                onCheckboxChange={handleCheckboxChange}
                loading={loading}
                error={error}
                onRetry={fetchUsuarios}
                serverStatus={serverStatus}
                onVerificarServidor={handleVerificarServidor}
                // Props de paginación
                currentPage={currentPage}
                totalPages={totalPages}
                itemsPerPage={itemsPerPage}
                totalItems={totalItems}
                onPageChange={handlePageChange}
                onItemsPerPageChange={handleItemsPerPageChange}
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

export default PanelSolicitante;
