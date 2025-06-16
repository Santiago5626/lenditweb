import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import TablaPrestamos from '../components/TablaPrestamos';
import SelectorSolicitantes from '../components/SelectorSolicitantes';
import SelectorProductos from '../components/SelectorProductos';
import CarritoPrestamos from '../components/CarritoPrestamos';
import { fetchPrestamos, fetchSolicitantes, fetchProductos, fetchTiposProducto, crearPrestamo } from '../api/peticiones';
import '../styles/pages/inicio.css';
import '../styles/pages/Circulacion.css';

const CirculacionNueva = () => {
  // Estados para datos
  const [prestamos, setPrestamos] = useState([]);
  const [solicitantes, setSolicitantes] = useState([]);
  const [productos, setProductos] = useState([]);
  const [tiposProducto, setTiposProducto] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para el proceso de préstamo
  const [solicitanteSeleccionado, setSolicitanteSeleccionado] = useState(null);
  const [productosSeleccionados, setProductosSeleccionados] = useState([]);
  const [fechaLimite, setFechaLimite] = useState('');
  const [modoPrestamoActivo, setModoPrestamoActivo] = useState(false);

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      const [prestamosData, solicitantesData, productosData, tiposData] = await Promise.all([
        fetchPrestamos(),
        fetchSolicitantes(),
        fetchProductos(),
        fetchTiposProducto()
      ]);
      setPrestamos(prestamosData);
      setSolicitantes(solicitantesData);
      setProductos(productosData);
      setTiposProducto(tiposData);
      setError(null);
    } catch (error) {
      console.error('Error al cargar datos:', error);
      setError('Error al cargar los datos necesarios');
    } finally {
      setLoading(false);
    }
  };

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
    setFechaLimite('');
  };

  const handleConfirmPrestamos = async () => {
    if (!solicitanteSeleccionado || productosSeleccionados.length === 0 || !fechaLimite) {
      setError('Por favor, complete todos los campos necesarios');
      return;
    }

    try {
      setLoading(true);
      // Crear préstamos para cada producto seleccionado
      await Promise.all(productosSeleccionados.map(producto => 
        crearPrestamo({
          IDENTIFICACION_SOLICITANTE: solicitanteSeleccionado.identificacion,
          IDPRODUCTO: producto.IDPRODUCTO,
          FECHA_LIMITE: fechaLimite
        })
      ));

      // Limpiar selecciones y recargar datos
      handleClearCart();
      setSolicitanteSeleccionado(null);
      setModoPrestamoActivo(false);
      await cargarDatos();
      setError(null);
    } catch (error) {
      console.error('Error al crear préstamos:', error);
      setError('Error al registrar los préstamos');
    } finally {
      setLoading(false);
    }
  };

  const handleDevolver = async (idPrestamo) => {
    // TODO: Implementar la devolución de préstamos
    console.log('Devolver préstamo:', idPrestamo);
  };

  if (loading) {
    return (
      <div className="page-container">
        <Sidebar />
        <main className="main-content">
          <div className="loading-container">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Cargando...</span>
            </div>
            <p>Cargando datos...</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="page-container">
      <Sidebar />
      <main className="main-content">
          <button
            className="btn btn-primary"
            onClick={() => setModoPrestamoActivo(!modoPrestamoActivo)}
          >
            <i className="material-symbols-outlined">
              {modoPrestamoActivo ? 'close' : 'add_circle'}
            </i>
            {modoPrestamoActivo ? 'Cancelar Préstamo' : 'Nuevo Préstamo'}
          </button>

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        {modoPrestamoActivo ? (
          <div className="prestamo-container">
            <div className="prestamo-grid">
              <div className="selector-section">
                <SelectorSolicitantes
                  solicitantes={solicitantes}
                  onSelectSolicitante={setSolicitanteSeleccionado}
                  solicitanteSeleccionado={solicitanteSeleccionado}
                />
              </div>
              <div className="carrito-section">
                <CarritoPrestamos
                  items={productosSeleccionados}
                  solicitanteSeleccionado={solicitanteSeleccionado}
                  onRemoveItem={handleRemoveFromCart}
                  onClear={handleClearCart}
                  onConfirm={handleConfirmPrestamos}
                  fechaLimite={fechaLimite}
                  onFechaLimiteChange={setFechaLimite}
                />
              </div>
              <div className="productos-section">
                <SelectorProductos
                  productos={productos}
                  tiposProducto={tiposProducto}
                  onAddToCart={handleAddToCart}
                />
              </div>
            </div>
          </div>
        ) : (
          <TablaPrestamos
            prestamos={prestamos}
            solicitantes={solicitantes}
            productos={productos}
            onDevolver={handleDevolver}
          />
        )}
      </main>
    </div>
  );
};

export default CirculacionNueva;
