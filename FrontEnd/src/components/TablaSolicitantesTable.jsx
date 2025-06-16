import React from "react";
import "./TablaSolicitantes.css";

const TablaSolicitantesTable = ({
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
    // Props de paginación con valores por defecto
    currentPage = 1,
    totalPages = 1,
    itemsPerPage = 10,
    totalItems = 0,
    onPageChange = () => { },
    onItemsPerPageChange = () => { }
}) => {
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

    if (!serverStatus) {
        return (
            <div className="table-section">
                <div className="error-container alert alert-warning">
                    <h4>Error de conexión</h4>
                    <p>No se puede conectar al servidor. Por favor, verifica que el servidor esté corriendo.</p>
                    <button className="btn btn-primary mt-3" onClick={onVerificarServidor}>
                        Verificar conexión
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

    if (usuarios.length === 0 && totalItems > 0) {
        return (
            <div className="table-section">
                <div className="alert alert-warning">
                    No hay resultados en esta página.
                    <button
                        className="btn btn-link p-0 ms-2"
                        onClick={() => onPageChange(1)}
                    >
                        Ir a la primera página
                    </button>
                </div>
            </div>
        );
    }

    // Debug logging
    console.log('TablaSolicitantesTable - Props recibidos:', {
        usuariosLength: usuarios.length,
        totalItems,
        totalPages,
        currentPage,
        itemsPerPage,
        shouldShowPagination: totalItems > 0,
        calculatedPages: Math.ceil(totalItems / itemsPerPage)
    });

    return (
        <table className="table table-bordered table-hover">
                <thead className="thead-light">
                    <tr>
                        <th style={{ width: '50px' }}>
                            {multiSelectMode && (
                                <input
                                    type="checkbox"
                                    onChange={() => {
                                        // Seleccionar/deseleccionar todos en la página actual
                                        if (selectedUsers.length === usuarios.length) {
                                            selectedUsers.forEach(user => onCheckboxChange(user));
                                        } else {
                                            usuarios.forEach(user => {
                                                if (!selectedUsers.some(u => u.identificacion === user.identificacion)) {
                                                    onCheckboxChange(user);
                                                }
                                            });
                                        }
                                    }}
                                    checked={selectedUsers.length === usuarios.length && usuarios.length > 0}
                                    title="Seleccionar/Deseleccionar todos en esta página"
                                />
                            )}
                            {!multiSelectMode && <span style={{ fontSize: '12px', color: '#666' }}>Sel.</span>}
                        </th>
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
    );
};

export default TablaSolicitantesTable;
