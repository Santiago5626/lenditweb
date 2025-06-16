import { useState, useEffect } from 'react';
import { fetchPrestamos, fetchSolicitantes, fetchProductos, fetchTiposProducto } from '../api/peticiones';

export const useCirculacionData = () => {
    const [data, setData] = useState({
        prestamos: [],
        solicitantes: [],
        productos: [],
        tiposProducto: []
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const cargarDatos = async () => {
        try {
            setLoading(true);
            const [prestamosData, solicitantesData, productosData, tiposData] = await Promise.all([
                fetchPrestamos(),
                fetchSolicitantes(),
                fetchProductos(),
                fetchTiposProducto()
            ]);

            setData({
                prestamos: prestamosData,
                solicitantes: solicitantesData,
                productos: productosData,
                tiposProducto: tiposData
            });
            setError(null);
        } catch (error) {
            console.error('Error al cargar datos:', error);
            setError('Error al cargar los datos necesarios');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        cargarDatos();
    }, []);

    return {
        ...data,
        loading,
        error,
        recargarDatos: cargarDatos,
        setError
    };
};
