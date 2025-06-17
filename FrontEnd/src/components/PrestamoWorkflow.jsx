import React, { useState } from 'react';
import SelectorSolicitantes from './SelectorSolicitantes';
import SelectorProductos from './SelectorProductos';
import SelectedItemsChips from './SelectedItemsChips';
import AlertMessage from './AlertMessage';
import { crearSolicitud, agregarProductoASolicitud, crearPrestamo } from '../api/peticiones';

const PrestamoWorkflow = ({
    solicitantes,
    productos,
    tiposProducto,
    onPrestamoCompleted,
    onError
}) => {
    const [solicitanteSeleccionado, setSolicitanteSeleccionado] = useState(null);
    const [productosSeleccionados, setProductosSeleccionados] = useState([]);
    const [fechaLimite, setFechaLimite] = useState(new Date().toISOString().split('T')[0]);
    const [loading, setLoading] = useState(false);

    const handleAddToCart = (producto) => {
        if (!productosSeleccionados.some(p => p.IDPRODUCTO === producto.IDPRODUCTO)) {
            setProductosSeleccionados([...productosSeleccionados, producto]);
        }
    };

    const handleRemoveFromCart = (producto) => {
        setProductosSeleccionados(
            productosSeleccionados.filter(p => p.IDPRODUCTO !== producto.IDPRODUCTO)
        );
    };

    const handleClearCart = () => {
        setProductosSeleccionados([]);
        setFechaLimite(new Date().toISOString().split('T')[0]);
    };

    const handleConfirmPrestamos = async () => {
        if (!solicitanteSeleccionado || productosSeleccionados.length === 0 || !fechaLimite) {
            onError('Por favor, complete todos los campos necesarios');
            return;
        }

        try {
            setLoading(true);

            // Paso 1: Crear la solicitud
            const solicitudData = {
                IDENTIFICACION: solicitanteSeleccionado.identificacion,
                FECHA_REGISTRO: new Date().toISOString().split('T')[0],
                ESTADO: 'pendiente'
            };

            const solicitudCreada = await crearSolicitud(solicitudData);

            // Paso 2: Agregar productos a la solicitud
            await Promise.all(productosSeleccionados.map(producto =>
                agregarProductoASolicitud({
                    PRODUCTO_ID: producto.IDPRODUCTO,
                    SOLICITUD_ID: solicitudCreada.IDSOLICITUD || solicitudCreada.id
                })
            ));

            // Paso 3: Crear el préstamo
            const prestamoData = {
                IDSOLICITUD: solicitudCreada.IDSOLICITUD || solicitudCreada.id,
                FECHA_REGISTRO: new Date().toISOString().split('T')[0],
                FECHA_LIMITE: fechaLimite
            };

            await crearPrestamo(prestamoData);

            // Limpiar y notificar éxito
            handleClearCart();
            setSolicitanteSeleccionado(null);
            onPrestamoCompleted();

        } catch (error) {
            console.error('Error al crear préstamos:', error);
            onError('Error al registrar los préstamos: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="prestamo-container">
            <div className="prestamo-grid">
                <SelectedItemsChips 
                    solicitanteSeleccionado={solicitanteSeleccionado}
                    productosSeleccionados={productosSeleccionados}
                    fechaLimite={fechaLimite}
                    onFechaLimiteChange={setFechaLimite}
                    onConfirm={handleConfirmPrestamos}
                    onClear={handleClearCart}
                    onRemoveSolicitante={() => setSolicitanteSeleccionado(null)}
                    onRemoveProduct={handleRemoveFromCart}
                    loading={loading}
                />
                <div className="selectores-container">
                    <div className="selector-solicitantes-wrapper">
                        <SelectorSolicitantes
                            solicitantes={solicitantes}
                            onSelectSolicitante={setSolicitanteSeleccionado}
                            solicitanteSeleccionado={solicitanteSeleccionado}
                        />
                    </div>
                    <div className="selector-productos-wrapper">
                        <SelectorProductos
                            productos={productos}
                            tiposProducto={tiposProducto}
                            onAddToCart={handleAddToCart}
                            selectedProducts={productosSeleccionados}
                            onRemoveProduct={handleRemoveFromCart}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PrestamoWorkflow;
