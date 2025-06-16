import React, { useState, useEffect } from 'react';

const ProlongarPrestamoModal = ({ show, onHide, onConfirm, esAprendiz }) => {
    const [dias, setDias] = useState(esAprendiz ? 1 : 7);

    useEffect(() => {
        setDias(esAprendiz ? 1 : 7);
    }, [esAprendiz]);

    const handleConfirm = () => {
        onConfirm(dias);
    };

    if (!show) return null;

    return (
        <>
            <div className="modal-backdrop fade show" onClick={onHide}></div>
            <div className="modal fade show" style={{ display: 'block', zIndex: 1055 }} tabIndex="-1">
                <div className="modal-dialog modal-dialog-centered">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Prolongar Préstamo</h5>
                            <button type="button" className="btn-close" onClick={onHide}></button>
                        </div>
                        <div className="modal-body">
                            <div className="mb-3">
                                <label htmlFor="dias" className="form-label">
                                    Días de prolongación
                                </label>
                                {esAprendiz ? (
                                    <div>
                                        <div className="alert alert-info">
                                            <i className="material-symbols-outlined me-2">info</i>
                                            Los aprendices solo pueden prolongar por 1 día
                                        </div>
                                        <input
                                            type="number"
                                            className="form-control"
                                            id="dias"
                                            value={1}
                                            disabled
                                        />
                                    </div>
                                ) : (
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="dias"
                                        value={dias}
                                        onChange={(e) => setDias(parseInt(e.target.value) || 1)}
                                        min="1"
                                        max="30"
                                    />
                                )}
                                {!esAprendiz && (
                                    <div className="form-text">
                                        Puedes prolongar entre 1 y 30 días
                                    </div>
                                )}
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" onClick={onHide}>
                                Cancelar
                            </button>
                            <button type="button" className="btn btn-primary" onClick={handleConfirm}>
                                <i className="material-symbols-outlined me-2">schedule</i>
                                Prolongar {dias} día{dias !== 1 ? 's' : ''}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ProlongarPrestamoModal;
