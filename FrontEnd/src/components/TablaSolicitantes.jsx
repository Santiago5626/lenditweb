import React, { useState, useEffect } from 'react';
import '../styles/components/TablaSolicitantes.css';
import TablaSolicitantesTable from './TablaSolicitantesTable';
import EditarModal from './EditarModal';
import RegistrarModal from './RegistrarModal';
import ImportarSolicitantesModal from './ImportarSolicitantesModal';
import PaginationControls from './PaginationControls';
import { obtenerSolicitantes, eliminarSolicitante } from '../api/peticiones';

const TablaSolicitantes = () => {
  const [solicitantes, setSolicitantes] = useState([]);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showRegistrarModal, setShowRegistrarModal] = useState(false);
  const [showImportarModal, setShowImportarModal] = useState(false);
  const [selectedSolicitante, setSelectedSolicitante] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const itemsPerPage = 10;

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

      <TablaSolicitantesTable
        solicitantes={currentItems}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <PaginationControls
        currentPage={currentPage}
        totalItems={filteredSolicitantes.length}
        itemsPerPage={itemsPerPage}
        onPageChange={setCurrentPage}
      />

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
