import React, { useState, useEffect } from 'react';
import { crearPrestamo, fetchSolicitantes, fetchProductos } from '../api/peticiones';
import '../styles/components/RegistrarModal.css';
import '../styles/global-inputs.css';

const RegistrarPrestamoModal = ({ isOpen, onClose, onPrestamoCreado }) => {
    const [formData, setFormData] = useState({
        IDENTIFICACION_SOLICITANTE: '',
        IDPRODUCTO: '',
        FECHA_LIMITE: ''
    });

    const [solicitantes, setSolicitantes] = useState([]);
    const [productos, setProductos] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const cargarDatos = async () => {
            try {
                const [solicitantesData, productosData] = await Promise.all([
                    fetchSolicitantes(),
                    fetchProductos()
                ]);
                setSolicitantes(solicitantesData);
                setProductos(productosData.filter(p => p.ESTADO === 'Disponible'));
            } catch (error) {
                console.error('Error al cargar datos:', error);
                setError('Error al cargar datos necesarios');
            }
        };

        if (isOpen) {
            cargarDatos();
        }
    }, [isOpen]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log('Enviando datos del préstamo:', formData);
            console.log('Tipo de idProducto:', typeof formData.idProducto);
            const response = await crearPrestamo(formData);
            console.log('Respuesta del servidor:', response);
            onPrestamoCreado();
            onClose();
            setFormData({
                IDENTIFICACION_SOLICITANTE: '',
                IDPRODUCTO: '',
                FECHA_LIMITE: ''
            });
        } catch (error) {
            console.error('Error al crear préstamo:', error);
            setError(error.message || 'Error al crear el préstamo');
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'IDPRODUCTO' ? parseInt(value) || '' : value
        }));
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>Registrar Préstamo</h2>
                {error && <div className="error-message">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="IDENTIFICACION_SOLICITANTE">Solicitante</label>
                        <select
                            id="IDENTIFICACION_SOLICITANTE"
                            name="IDENTIFICACION_SOLICITANTE"
                            className="select-standard"
                            value={formData.IDENTIFICACION_SOLICITANTE}
                            onChange={handleChange}
                            required
                        >
                            <option value="">Seleccione un solicitante</option>
                            {solicitantes.map(solicitante => (
                                <option key={solicitante.identificacion} value={solicitante.identificacion}>
                                    {solicitante.primer_nombre} {solicitante.primer_apellido} - {solicitante.identificacion}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="IDPRODUCTO">Producto</label>
                        <select
                            id="IDPRODUCTO"
                            name="IDPRODUCTO"
                            className="select-standard"
                            value={formData.IDPRODUCTO}
                            onChange={handleChange}
                            required
                        >
                            <option value="">Seleccione un producto</option>
                            {productos.map(producto => (
                                <option key={producto.IDPRODUCTO} value={producto.IDPRODUCTO}>
                                    {producto.NOMBRE} - {producto.CODIGO_INTERNO}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="FECHA_LIMITE">Fecha de Devolución</label>
                        <input
                            type="date"
                            id="FECHA_LIMITE"
                            name="FECHA_LIMITE"
                            className="input-standard"
                            value={formData.FECHA_LIMITE}
                            onChange={handleChange}
                            required
                            min={new Date().toISOString().split('T')[0]}
                        />
                    </div>

                    <div className="modal-buttons">
                        <button type="submit" className="btn-primary">
                            Registrar Préstamo
                        </button>
                        <button type="button" onClick={onClose} className="btn-secondary">
                            Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default RegistrarPrestamoModal;
