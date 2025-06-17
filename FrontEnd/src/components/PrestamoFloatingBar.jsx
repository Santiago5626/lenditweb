import React from 'react';
import './PrestamoFloatingBar.css';

const PrestamoFloatingBar = ({
    solicitanteSeleccionado,
    productosSeleccionados,
    fechaLimite,
    onFechaLimiteChange,
    onConfirm,
    onClear,
    loading
}) => {
    if (!solicitanteSeleccionado && productosSeleccionados.length === 0) {
        return null; // No mostrar la barra si no hay nada seleccionado
    }

    return (
        <div className="prestamo-floating-bar">
            <div className="prestamo-floating-content">
                <div className="solicitante-info">
                    {solicitanteSeleccionado && (
                        <span className="solicitante-name">
                            {solicitanteSeleccionado.nombre} ({solicitanteSeleccionado.identificacion})
                        </span>
                    )}
                </div>
                
                <div className="productos-info">
                    <span className="productos-count">
                        {productosSeleccionados.length} producto(s)
                    </span>
                    {productosSeleccionados.length > 0 && (
                        <button 
                            className="btn-clear"
                            onClick={onClear}
                            disabled={loading}
                        >
                            Limpiar
                        </button>
                    )}
                </div>

                <div className="fecha-limite">
                    <input
                        type="date"
                        value={fechaLimite}
                        onChange={(e) => onFechaLimiteChange(e.target.value)}
                        min={new Date().toISOString().split('T')[0]}
                        disabled={loading}
                    />
                </div>

                <button
                    className="btn-confirm"
                    onClick={onConfirm}
                    disabled={loading || !solicitanteSeleccionado || productosSeleccionados.length === 0}
                >
                    {loading ? 'Procesando...' : 'Confirmar Préstamo'}
                </button>
            </div>
        </div>
    );
};

export default PrestamoFloatingBar;
