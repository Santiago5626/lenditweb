import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import TablaPrestamos from '../components/TablaPrestamos';
import PrestamoWorkflow from '../components/PrestamoWorkflow';
import LoadingSpinner from '../components/LoadingSpinner';
import AlertMessage from '../components/AlertMessage';
import PageHeader from '../components/PageHeader';
import { useCirculacionData } from '../hooks/useCirculacionData';
import { devolverPrestamo, prolongarPrestamo } from '../api/peticiones';
import '../styles/pages/inicio.css';
import '../styles/pages/Circulacion.css';

const Circulacion = () => {
  const [modoPrestamoActivo, setModoPrestamoActivo] = useState(false);
  const {
    prestamos,
    solicitantes,
    productos,
    tiposProducto,
    loading,
    error,
    recargarDatos,
    setError
  } = useCirculacionData();

  const handleDevolver = async (idPrestamo) => {
    try {
      setError(null);
      await devolverPrestamo(idPrestamo);
      recargarDatos();
    } catch (error) {
      console.error('Error al devolver préstamo:', error);
      setError(error.message || 'Error al devolver el préstamo');
    }
  };

  const handleProlongar = async (idPrestamo, dias) => {
    try {
      setError(null);
      await prolongarPrestamo(idPrestamo, dias);
      recargarDatos();
    } catch (error) {
      console.error('Error al prolongar préstamo:', error);
      setError(error.message || 'Error al prolongar el préstamo');
    }
  };

  const actionButton = (
    <button
      className="btn btn-primary"
      onClick={() => setModoPrestamoActivo(!modoPrestamoActivo)}
    >
      <i className="material-symbols-outlined">
        {modoPrestamoActivo ? 'close' : 'add_circle'}
      </i>
      {modoPrestamoActivo ? 'Cancelar Préstamo' : 'Nuevo Préstamo'}
    </button>
  );

  if (loading) {
    return (
      <div className="page-container">
        <Sidebar />
        <main className="main-content">
          <LoadingSpinner message="Cargando datos..." />
        </main>
      </div>
    );
  }

  return (
    <div className="page-container">
      <Sidebar />
      <main className="main-content">
        <PageHeader
          actionButton={actionButton}
        />

        <AlertMessage message={error} />

        {modoPrestamoActivo ? (
          <PrestamoWorkflow
            solicitantes={solicitantes}
            productos={productos}
            tiposProducto={tiposProducto}
            onPrestamoCompleted={() => {
              setModoPrestamoActivo(false);
              recargarDatos();
            }}
            onError={setError}
          />
        ) : (
          <TablaPrestamos
            prestamos={prestamos}
            solicitantes={solicitantes}
            productos={productos}
            onDevolver={handleDevolver}
            onProlongar={handleProlongar}
          />
        )}
      </main>
    </div>
  );
};

export default Circulacion;
