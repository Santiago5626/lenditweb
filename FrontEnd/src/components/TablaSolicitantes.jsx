  import React, { useState, useEffect } from 'react';
import '../styles/components/TablaSolicitantes.css';
import TablaSolicitantesTable from './TablaSolicitantesTable';
import EditarModal from './EditarModal';
import RegistrarModal from './RegistrarModal';
import ImportarSolicitantesModal from './ImportarSolicitantesModal';
import { obtenerSolicitantes, eliminarSolicitante } from '../api/peticiones';

const TablaSolicitantes = () => {
  const [solicitantes, setSolicitantes] = useState([]);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showRegistrarModal, setShowRegistrarModal] = useState(false);
  const [showImportarModal, setShowImportarModal] = useState(false);
  const [selectedSolicitante, setSelectedSolicitante] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [itemsPerPage, setItemsPerPage] = useState(10);

  useEffect(() => {
    fetchSolicitantes();
  }, []);

  const fetchSolicitantes = async () => {
    try {
      const data = await obtenerSolicitantes();
      setSolicitantes(data);
    } catch (error) {
      console.error('Error al obtener solicitantes:', error);
    }
  };

  const handleEdit = (solicitante) => {
    setSelectedSolicitante(solicitante);
    setShowEditModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este solicitante?')) {
      try {
        await eliminarSolicitante(id);
        fetchSolicitantes();
      } catch (error) {
        console.error('Error al eliminar solicitante:', error);
      }
    }
  };

  const handleCloseModal = () => {
    setShowEditModal(false);
    setShowRegistrarModal(false);
    setShowImportarModal(false);
    setSelectedSolicitante(null);
    fetchSolicitantes();
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1);
  };

  const filteredSolicitantes = solicitantes.filter(solicitante =>
    Object.values(solicitante).some(value =>
      value?.toString().toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredSolicitantes.slice(indexOfFirstItem, indexOfLastItem);

  return (
    <div className="tabla-solicitantes-container">
      <div className="tabla-header">
        <div className="search-container">
          <input
            type="text"
            placeholder="Buscar..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
        </div>
        <div className="buttons-container">
          <button onClick={() => setShowRegistrarModal(true)} className="btn-registrar">
            Registrar Solicitante
          </button>
          <button onClick={() => setShowImportarModal(true)} className="btn-importar">
            Importar Excel
          </button>
        </div>
      </div>

      {/* Controles superiores de paginación */}
      {filteredSolicitantes.length > 0 && (
        <div className="pagination-top-controls">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <div className="pagination-info">
              <small className="text-muted">
                Mostrando {((currentPage - 1) * itemsPerPage) + 1} - {Math.min(currentPage * itemsPerPage, filteredSolicitantes.length)} de {filteredSolicitantes.length} registros
              </small>
            </div>
            <div className="items-per-page">
              <label className="me-2">
                <small>Mostrar:</small>
              </label>
              <select
                className="form-select form-select-sm d-inline-block w-auto"
                value={itemsPerPage}
                onChange={(e) => {
                  const value = Number(e.target.value);
                  setItemsPerPage(value);
                  setCurrentPage(1);
                }}
              >
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
              <small className="ms-2">por página</small>
            </div>
          </div>
        </div>
      )}

      <div className="table-section">
        {solicitantes.length === 0 ? (
          <div className="alert alert-info">
            No hay solicitantes registrados
          </div>
        ) : (
          <>
            <TablaSolicitantesTable
              solicitantes={currentItems}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />

            {/* Controles inferiores de navegación */}
            {Math.ceil(filteredSolicitantes.length / itemsPerPage) > 1 && (
              <div className="pagination-bottom d-flex justify-content-center mt-4">
                <nav aria-label="Paginación de solicitantes">
                  <ul className="pagination pagination-sm">
                    {/* Botón Anterior */}
                    <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                      <button
                        className="page-link"
                        onClick={() => setCurrentPage(currentPage - 1)}
                        disabled={currentPage === 1}
                        aria-label="Página anterior"
                      >
                        &laquo;
                      </button>
                    </li>

                    {/* Números de página */}
                    {(() => {
                      const pages = [];
                      const totalPages = Math.ceil(filteredSolicitantes.length / itemsPerPage);
                      const maxVisiblePages = 5;
                      let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
                      let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

                      // Ajustar el inicio si estamos cerca del final
                      if (endPage - startPage + 1 < maxVisiblePages) {
                        startPage = Math.max(1, endPage - maxVisiblePages + 1);
                      }

                      // Primera página si no está visible
                      if (startPage > 1) {
                        pages.push(
                          <li key={1} className="page-item">
                            <button className="page-link" onClick={() => setCurrentPage(1)}>
                              1
                            </button>
                          </li>
                        );
                        if (startPage > 2) {
                          pages.push(
                            <li key="ellipsis1" className="page-item disabled">
                              <span className="page-link">...</span>
                            </li>
                          );
                        }
                      }

                      // Páginas visibles
                      for (let i = startPage; i <= endPage; i++) {
                        pages.push(
                          <li key={i} className={`page-item ${currentPage === i ? 'active' : ''}`}>
                            <button
                              className="page-link"
                              onClick={() => setCurrentPage(i)}
                              aria-label={`Página ${i}`}
                              aria-current={currentPage === i ? 'page' : undefined}
                            >
                              {i}
                            </button>
                          </li>
                        );
                      }

                      // Última página si no está visible
                      if (endPage < totalPages) {
                        if (endPage < totalPages - 1) {
                          pages.push(
                            <li key="ellipsis2" className="page-item disabled">
                              <span className="page-link">...</span>
                            </li>
                          );
                        }
                        pages.push(
                          <li key={totalPages} className="page-item">
                            <button className="page-link" onClick={() => setCurrentPage(totalPages)}>
                              {totalPages}
                            </button>
                          </li>
                        );
                      }

                      return pages;
                    })()}

                    {/* Botón Siguiente */}
                    <li className={`page-item ${currentPage === Math.ceil(filteredSolicitantes.length / itemsPerPage) ? 'disabled' : ''}`}>
                      <button
                        className="page-link"
                        onClick={() => setCurrentPage(currentPage + 1)}
                        disabled={currentPage === Math.ceil(filteredSolicitantes.length / itemsPerPage)}
                        aria-label="Página siguiente"
                      >
                        &raquo;
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            )}
          </>
        )}
      </div>

      {showEditModal && (
        <EditarModal
          show={showEditModal}
          handleClose={handleCloseModal}
          solicitante={selectedSolicitante}
        />
      )}

      {showRegistrarModal && (
        <RegistrarModal
          show={showRegistrarModal}
          handleClose={handleCloseModal}
        />
      )}

      {showImportarModal && (
        <ImportarSolicitantesModal
          show={showImportarModal}
          handleClose={handleCloseModal}
        />
      )}
    </div>
  );
};

export default TablaSolicitantes;
