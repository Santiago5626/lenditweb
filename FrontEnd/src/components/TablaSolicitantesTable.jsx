import React from "react";
import "./TablaSolicitantes.css";

const TablaSolicitantesTable = ({ usuarios, selectedUser, onCheckboxChange, loading, error, onRetry, serverStatus, onVerificarServidor }) => {
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
                    <button
                        className="btn btn-primary mt-3"
                        onClick={onRetry}
                    >
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
                    <button
                        className="btn btn-primary mt-3"
                        onClick={onVerificarServidor}
                    >
                        Verificar conexión
                    </button>
                </div>
            </div>
        );
    }

    if (usuarios.length === 0) {
        return (
            <div className="table-section">
                <div className="alert alert-info">
                    No hay solicitantes registrados
                </div>
            </div>
        );
    }

    return (
        <div className="table-section">
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
                    {usuarios.map((user, index) => (
                        <tr
                            key={user.identificacion || index}
                            className={selectedUser === user ? "table-active" : ""}
                        >
                            <td>
                                <input
                                    type="checkbox"
                                    checked={selectedUser === user}
                                    onChange={() => onCheckboxChange(user)}
                                />
                            </td>
                            <td>{user.identificacion}</td>
                            <td>{user.primer_nombre}</td>
                            <td>{user.primer_apellido}</td>
                            <td>{user.segundo_apellido || "-"}</td>
                            <td>{user.telefono}</td>
                            <td>{user.correo}</td>
                            <td>{user.ficha || "-"}</td>
                            <td>{user.programa || "-"}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TablaSolicitantesTable;
