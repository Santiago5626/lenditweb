import React from 'react';
import './SelectedItemsChips.css';

const SelectedItemsChips = ({
    solicitanteSeleccionado,
    productosSeleccionados,
    fechaLimite,
    onFechaLimiteChange,
    onRemoveSolicitante,
    onRemoveProduct,
    onConfirm,
    onClear,
    loading
}) => {
    if (!solicitanteSeleccionado && productosSeleccionados.length === 0) {
        return null;
    }

    return (
        <div className="selected-items-container">
            <div className="chips-section">
                {/* Chip del solicitante */}
                {solicitanteSeleccionado && (
                    <div className="chip chip-solicitante">
                        <span className="chip-label">Solicitante:</span>
                        <span className="chip-value">
                            {`${solicitanteSeleccionado.primer_nombre} ${solicitanteSeleccionado.primer_apellido}`}
                        </span>
                        <button 
                            className="chip-remove"
                            onClick={onRemoveSolicitante}
                            disabled={loading}
                        >
                            ×
                        </button>
                    </div>
                )}

                {/* Chips de productos */}
                {productosSeleccionados.map(producto => (
                    <div key={producto.IDPRODUCTO} className="chip chip-producto">
                        <span className="chip-value">{producto.CODIGO_INTERNO}</span>
                        <button 
                            className="chip-remove"
                            onClick={() => onRemoveProduct(producto)}
                            disabled={loading}
                        >
                            ×
                        </button>
                    </div>
                ))}
            </div>

            {/* Controles de acción */}
            {(solicitanteSeleccionado || productosSeleccionados.length > 0) && (
                <div className="action-controls">
                    <div className="fecha-control">
                        <label>Fecha límite:</label>
                        <input
                            type="date"
                            value={fechaLimite}
                            onChange={(e) => onFechaLimiteChange(e.target.value)}
                            min={new Date().toISOString().split('T')[0]}
                            disabled={loading}
                        />
                    </div>
                    
                    <div className="action-buttons">
                        <button
                            className="btn-clear"
                            onClick={onClear}
                            disabled={loading}
                        >
                            Limpiar Todo
                        </button>
                        
                        <button
                            className="btn-confirm"
                            onClick={onConfirm}
                            disabled={loading || !solicitanteSeleccionado || productosSeleccionados.length === 0}
                        >
                            {loading ? 'Procesando...' : 'Registrar Préstamo'}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SelectedItemsChips;
