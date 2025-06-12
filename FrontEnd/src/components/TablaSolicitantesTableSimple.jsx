import React from "react";
import "../styles/components/TablaSolicitantes.css";
import PaginationControls from "./PaginationControls";

const TablaSolicitantesTableSimple = ({
    usuarios = [],
    selectedUser,
    selectedUsers = [],
    multiSelectMode = false,
    onCheckboxChange = () => { },
    loading = false,
    error = null,
    onRetry = () => { },
    serverStatus = true,
    onVerificarServidor = () => { },
    // Props de paginación
    currentPage = 1,
    totalPages = 1,
    itemsPerPage = 10,
    totalItems = 0,
    onPageChange = () => { },
    onItemsPerPageChange = () => { }
}) => {
    console.log('TablaSolicitantesTableSimple - Props:', {
        usuariosLength: usuarios.length,
        totalItems,
        totalPages,
        currentPage,
        itemsPerPage
    });

    if (loading) {
        return (
            <div className="table-section">
                <div className="loading-container">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Cargando...</span>
                    </div>
                    <p>Cargando solicitantes...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="table-section">
                <div className="error-container alert alert-danger">
                    <h4>Error al cargar los datos</h4>
                    <p>{error}</p>
                    <button className="btn btn-primary mt-3" onClick={onRetry}>
                        Intentar nuevamente
                    </button>
                </div>
            </div>
        );
    }

    if (totalItems === 0 && usuarios.length === 0) {
        return (
            <div className="table-section">
                <div className="alert alert-info">No hay solicitantes registrados</div>
            </div>
        );
    }

    return (
        <div className="table-section">
            {/* Controles de paginación */}
            <PaginationControls
                currentPage={currentPage}
                totalPages={totalPages}
                itemsPerPage={itemsPerPage}
                totalItems={totalItems}
                onPageChange={onPageChange}
                onItemsPerPageChange={onItemsPerPageChange}
            />

            <table className="table table-bordered table-hover">
                <thead className="thead-light">
                    <tr>
                        <th style={{ width: '50px' }}>Sel.</th>
                        <th>Identificación</th>
                        <th>Nombre Completo</th>
                        <th>Teléfono</th>
                        <th>Correo</th>
                        <th>Ficha</th>
                        <th>Programa</th>
                    </tr>
                </thead>
                <tbody>
                    {usuarios.map((user, index) => {
                        const isSelected = multiSelectMode
                            ? selectedUsers.some(u => u.identificacion === user.identificacion)
                            : selectedUser && selectedUser.identificacion === user.identificacion;

                        const nombreCompleto = [
                            user.primer_nombre,
                            user.segundo_nombre,
                            user.primer_apellido,
                            user.segundo_apellido
                        ].filter(Boolean).join(" ");

                        return (
                            <tr
                                key={user.identificacion || index}
                                className={isSelected ? "table-active" : ""}
                                onClick={() => !multiSelectMode && onCheckboxChange(user)}
                                style={{ cursor: !multiSelectMode ? 'pointer' : 'default' }}
                            >
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={isSelected}
                                        onChange={() => onCheckboxChange(user)}
                                        onClick={e => e.stopPropagation()}
                                    />
                                </td>
                                <td>{user.identificacion}</td>
                                <td>{nombreCompleto}</td>
                                <td>{user.telefono}</td>
                                <td>{user.correo}</td>
                                <td>{user.ficha ? Math.floor(user.ficha) : "-"}</td>
                                <td>{user.programa || "-"}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default TablaSolicitantesTableSimple;
