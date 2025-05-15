import React, { useRef, useState } from "react";
import Sidebar from "../components/Sidebar";
import ResumenTarjetas from "../components/ResumenTarjetas";
import TablaResumenEstado from "../components/TablaResumenEstado";
import TablaSolicitantes from "../components/TablaSolicitantes";

import { importarSolicitantes } from "../api/peticiones";
import "./inicio.css";

const Inicio = () => {
  const fileInputRef = useRef(null);
  const [importStatus, setImportStatus] = useState(null);

  const handleImportClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.xlsx')) {
      alert('Por favor, seleccione un archivo Excel (.xlsx)');
      return;
    }

    try {
      setImportStatus('Importando...');
      const result = await importarSolicitantes(file);
      
      if (result.errores && result.errores.length > 0) {
        alert(`Importación completada con errores:\n${result.errores.join('\n')}`);
      } else {
        alert(result.message);
      }
      
      // Recargar la página para mostrar los nuevos datos
      window.location.reload();
    } catch (error) {
      alert('Error al importar: ' + error.message);
    } finally {
      setImportStatus(null);
      event.target.value = ''; // Limpiar el input
    }
  };

  return (
    <div className="page-container">
      <Sidebar />
      <main className="main-content">
        <div className="import-section" style={{ marginBottom: '20px', padding: '0 20px' }}>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".xlsx"
            style={{ display: 'none' }}
          />
          <button
            onClick={handleImportClick}
            className="btn btn-primary"
            disabled={!!importStatus}
            style={{
              padding: '8px 16px',
              borderRadius: '4px',
              backgroundColor: '#00304D',
              color: 'white',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            {importStatus || 'Importar Solicitantes desde Excel'}
          </button>
          <a 
            href="/plantilla-solicitantes.xlsx" 
            download 
            style={{
              marginLeft: '10px',
              color: '#00304D',
              textDecoration: 'underline',
              cursor: 'pointer'
            }}
          >
            Descargar Plantilla
          </a>
        </div>
        <div className="top-components">
          <div className="resumen-wrapper">
            <ResumenTarjetas />
          </div>
        </div>
        <TablaSolicitantes />
      </main>
    </div>
  );
};

export default Inicio;
