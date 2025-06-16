import React from 'react';

const LoadingSpinner = ({ message = "Cargando..." }) => {
    return (
        <div className="loading-container">
            <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Cargando...</span>
            </div>
            <p>{message}</p>
        </div>
    );
};

export default LoadingSpinner;
