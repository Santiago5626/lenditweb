import React, { useState, useMemo } from 'react';
import '../styles/components/TablaPrestamos.css';
import '../styles/global-inputs.css';
import ProlongarPrestamoModal from './ProlongarPrestamoModal';

const TablaPrestamos = ({ prestamos, solicitantes, productos, onDevolver, onProlongar }) => {
  const [prestamoParaProlongar, setPrestamoParaProlongar] = useState(null);
  const [filtroSolicitante, setFiltroSolicitante] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');

  const obtenerNombreSolicitante = (solicitud) => {
    if (!solicitud || !solicitud.IDENTIFICACION) return 'No disponible';
    const solicitante = solicitantes.find(s => s.identificacion === solicitud.IDENTIFICACION);
    if (solicitante) {
      return `${solicitante.primer_nombre} ${solicitante.segundo_nombre || ''} ${solicitante.primer_apellido} ${solicitante.segundo_apellido || ''}`.trim();
    }
    return 'No encontrado';
  };

  // Filtrar y ordenar préstamos basado en los filtros
  const prestamosFiltrados = useMemo(() => {
    return prestamos
      .filter(prestamo => {
        const solicitud = prestamo.solicitud || {};
        const nombreSolicitante = obtenerNombreSolicitante(solicitud).toLowerCase();
        const estado = solicitud.ESTADO?.toLowerCase() || '';

        const cumpleFiltroSolicitante = !filtroSolicitante ||
          nombreSolicitante.includes(filtroSolicitante.toLowerCase()) ||
          solicitud.IDENTIFICACION?.includes(filtroSolicitante);

        const cumpleFiltroEstado = !filtroEstado || estado === filtroEstado.toLowerCase();

        return cumpleFiltroSolicitante && cumpleFiltroEstado;
      })
      .sort((a, b) => {
        // Ordenar por fecha de registro descendente (más reciente primero)
        const fechaA = new Date(a.FECHA_REGISTRO);
        const fechaB = new Date(b.FECHA_REGISTRO);
        return fechaB - fechaA;
      });
  }, [prestamos, filtroSolicitante, filtroEstado, solicitantes]);

  // Obtener estados únicos para el filtro
  const estadosDisponibles = useMemo(() => {
    const estados = prestamos.map(p => p.solicitud?.ESTADO).filter(Boolean);
    return [...new Set(estados)];
  }, [prestamos]);

  const obtenerProductosSolicitud = (solicitud) => {
    if (!solicitud || !solicitud.productos_solicitud) return [];
    return solicitud.productos_solicitud.map(ps => {
      // Usar los datos del producto que ahora vienen del backend
      if (ps.NOMBRE && ps.CODIGO_INTERNO) {
        return `${ps.NOMBRE} (${ps.CODIGO_INTERNO})`;
      }
      // Fallback al método anterior si no están disponibles los nuevos campos
      const producto = productos.find(p => p.IDPRODUCTO === ps.PRODUCTO_ID);
      return producto ? `${producto.NOMBRE} (${producto.CODIGO_INTERNO})` : 'Producto no encontrado';
    });
  };

  const formatearFecha = (fecha) => {
    // Si la fecha viene como string (formato YYYY-MM-DD), la parseamos correctamente
    const fechaStr = typeof fecha === 'string' ? fecha : fecha.toISOString().split('T')[0];
    const fechaPrestamo = new Date(fechaStr + 'T00:00:00');

    const hoy = new Date();
    const hoySolo = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());

    // Calcular mañana
    const manana = new Date(hoySolo);
    manana.setDate(manana.getDate() + 1);

    // Comparar usando el tiempo en milisegundos
    const fechaPrestamoTime = fechaPrestamo.getTime();
    const hoyTime = hoySolo.getTime();
    const mananaTime = manana.getTime();

    if (fechaPrestamoTime === hoyTime) {
      return 'Hoy';
    } else if (fechaPrestamoTime === mananaTime) {
      return 'Mañana';
    }

    return fechaPrestamo.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const esAprendiz = (solicitud) => {
    if (!solicitud || !solicitud.IDENTIFICACION) return false;
    const solicitante = solicitantes.find(s => s.identificacion === solicitud.IDENTIFICACION);
    return solicitante?.rol?.toLowerCase() === 'aprendiz';
  };

  const handleProlongarClick = (prestamo) => {
    setPrestamoParaProlongar(prestamo);
  };

  const handleConfirmarProlongacion = (dias) => {
    if (prestamoParaProlongar && onProlongar) {
      onProlongar(prestamoParaProlongar.IDPRESTAMO, dias);
    }
    setPrestamoParaProlongar(null);
  };

  return (
    <div className="tabla-prestamos">
      {/* Filtros */}
      <div className="filtros-prestamos">
        <div className="row mb-3">
          <div className="col-md-6">
            <div className="input-group">
              <span className="input-group-text">
                <i className="material-symbols-outlined">search</i>
              </span>
              <input
                type="text"
                className="input-standard"
                placeholder="Buscar por solicitante o identificación..."
                value={filtroSolicitante}
                onChange={(e) => setFiltroSolicitante(e.target.value)}
              />
            </div>
          </div>
          <div className="col-md-4">
            <select
              className="select-standard"
              value={filtroEstado}
              onChange={(e) => setFiltroEstado(e.target.value)}
            >
              <option value="">Todos los estados</option>
              {estadosDisponibles.map(estado => (
                <option key={estado} value={estado}>
                  {estado.charAt(0).toUpperCase() + estado.slice(1)}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-2">
            <button
              className="btn-clear"
              onClick={() => {
                setFiltroSolicitante('');
                setFiltroEstado('');
              }}
            >
              Limpiar Todo
            </button>
          </div>
        </div>
      </div>

      <table className="table table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>Solicitante</th>
            <th>Producto</th>
            <th>Fecha Préstamo</th>
            <th>Fecha Límite</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {prestamosFiltrados.length === 0 ? (
            <tr>
              <td colSpan="7" className="text-center py-4">
                <div className="d-flex flex-column align-items-center">
                  <i className="material-symbols-outlined mb-2" style={{ fontSize: '48px', color: '#6c757d' }}>
                    search_off
                  </i>
                  <p className="mb-0 text-muted">
                    {prestamos.length === 0
                      ? 'No hay préstamos registrados'
                      : 'No se encontraron préstamos con los filtros aplicados'
                    }
                  </p>
                </div>
              </td>
            </tr>
          ) : (
            prestamosFiltrados.map((prestamo) => {
              const solicitud = prestamo.solicitud || {};
              const productos = obtenerProductosSolicitud(solicitud);
              const estadoActivo = solicitud.ESTADO === 'pendiente' || solicitud.ESTADO === 'aprobado';

              return (
                <tr
                  key={prestamo.IDPRESTAMO}
                  className={estadoActivo ? 'prestamo-activo' : 'prestamo-finalizado'}
                >
                  <td>{prestamo.IDPRESTAMO}</td>
                  <td>{obtenerNombreSolicitante(solicitud)}</td>
                  <td>
                    {productos.length > 0 ? (
                      <ul className="productos-lista">
                        {productos.map((producto, index) => (
                          <li key={index}>{producto}</li>
                        ))}
                      </ul>
                    ) : (
                      'No hay productos'
                    )}
                  </td>
                  <td>{formatearFecha(prestamo.FECHA_REGISTRO)}</td>
                  <td>{formatearFecha(prestamo.FECHA_LIMITE)}</td>
                  <td>
                    <span className={`estado-badge ${solicitud.ESTADO?.toLowerCase() || 'desconocido'}`}>
                      {solicitud.ESTADO || 'Desconocido'}
                    </span>
                  </td>
                  <td>
                    {estadoActivo && (
                      <div className="d-flex flex-column gap-2">
                        <button
                          className="btn btn-outline-success btn-sm"
                          onClick={() => onDevolver(prestamo.IDPRESTAMO)}
                          title="Devolver préstamo"
                        >
                          <i className="material-symbols-outlined">assignment_return</i>
                          Devolver
                        </button>
                        <button
                          className="btn btn-outline-warning btn-sm"
                          onClick={() => handleProlongarClick(prestamo)}
                          title={prestamo.FECHA_PROLONGACION
                            ? `Préstamo ya prolongado el ${formatearFecha(prestamo.FECHA_PROLONGACION)}`
                            : esAprendiz(solicitud)
                              ? "Prolongar préstamo por 1 día (Aprendiz)"
                              : "Prolongar préstamo"}
                          disabled={prestamo.FECHA_PROLONGACION}
                        >
                          <i className="material-symbols-outlined">schedule</i>
                          Prolongar
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>

      {/* Modal de prolongación */}
      <ProlongarPrestamoModal
        show={!!prestamoParaProlongar}
        onHide={() => setPrestamoParaProlongar(null)}
        onConfirm={handleConfirmarProlongacion}
        esAprendiz={prestamoParaProlongar ? esAprendiz(prestamoParaProlongar.solicitud) : false}
      />
    </div>
  );
};

export default TablaPrestamos;
