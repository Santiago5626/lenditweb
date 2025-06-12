import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import RegistrarPrestamoModal from '../components/RegistrarPrestamoModal';
import { fetchPrestamos, fetchSolicitantes } from '../api/peticiones';
import '../styles/pages/inicio.css';

const Circulacion = () => {
  const [prestamos, setPrestamos] = useState([]);
  const [solicitantes, setSolicitantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      const [prestamosData, solicitantesData] = await Promise.all([
        fetchPrestamos(),
        fetchSolicitantes()
      ]);
      setPrestamos(prestamosData);
      setSolicitantes(solicitantesData);
    } catch (error) {
      console.error('Error al cargar datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const cargarPrestamos = async () => {
    await cargarDatos();
  };

  const obtenerNombreSolicitante = (identificacion) => {
    const solicitante = solicitantes.find(s => s.identificacion === identificacion);
    if (solicitante) {
      return `${solicitante.primer_nombre} ${solicitante.primer_apellido}`;
    }
    return identificacion; // Fallback to ID if name not found
  };

  const handlePrestamoCreado = () => {
    cargarPrestamos();
  };

  if (loading) {
    return <div>Cargando préstamos...</div>;
  }

  return (
    <div className="page-container">
      <Sidebar />
      <main className="main-content">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
          <h1>CIRCULACIÓN - PRÉSTAMOS</h1>
          <button
            onClick={() => setShowModal(true)}
            style={{
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer"
            }}
          >
            Nuevo Préstamo
          </button>
        </div>

        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", backgroundColor: "white" }}>
            <thead>
              <tr style={{ backgroundColor: "#f8f9fa" }}>
                <th style={{ padding: "12px", border: "1px solid #dee2e6" }}>ID</th>
                <th style={{ padding: "12px", border: "1px solid #dee2e6" }}>Solicitante</th>
                <th style={{ padding: "12px", border: "1px solid #dee2e6" }}>ID Producto</th>
                <th style={{ padding: "12px", border: "1px solid #dee2e6" }}>Fecha Devolución</th>
                <th style={{ padding: "12px", border: "1px solid #dee2e6" }}>Estado</th>
              </tr>
            </thead>
            <tbody>
              {prestamos.map((prestamo) => (
                <tr key={prestamo.id || prestamo.IDPRESTAMO} style={{ borderBottom: "1px solid #dee2e6" }}>
                  <td style={{ padding: "12px", border: "1px solid #dee2e6" }}>
                    {prestamo.id || prestamo.IDPRESTAMO}
                  </td>
                  <td style={{ padding: "12px", border: "1px solid #dee2e6" }}>
                    {obtenerNombreSolicitante(prestamo.identificacionSolicitante || prestamo.IDENTIFICACION_SOLICITANTE)}
                  </td>
                  <td style={{ padding: "12px", border: "1px solid #dee2e6" }}>
                    {prestamo.idProducto || prestamo.IDPRODUCTO}
                  </td>
                  <td style={{ padding: "12px", border: "1px solid #dee2e6" }}>
                    {prestamo.fechaFinal || prestamo.FECHA_FINAL}
                  </td>
                  <td style={{ padding: "12px", border: "1px solid #dee2e6" }}>
                    <span style={{
                      padding: "5px 10px",
                      borderRadius: "15px",
                      backgroundColor: (prestamo.estado === 'activo' || prestamo.estado === 1) ? "#28a745" : "#dc3545",
                      color: "white"
                    }}>
                      {(prestamo.estado === 'activo' || prestamo.estado === 1) ? "Activo" : "Finalizado"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <RegistrarPrestamoModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          onPrestamoCreado={handlePrestamoCreado}
        />
      </main>
    </div>
  );
};

export default Circulacion;
