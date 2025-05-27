import React, { useState } from "react";
import "./RegistrarModal.css";
import { importarSolicitantes } from "../api/peticiones";

const ImportarSolicitantesModal = ({ show, onClose, onImportComplete }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState({
    total: 0,
    success: 0,
    errors: [],
    completed: false
  });

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") {
      setFile(selectedFile);
    } else {
      alert("Por favor seleccione un archivo Excel (.xlsx)");
    }
  };

  const handleDownloadTemplate = () => {
    const link = document.createElement('a');
    link.href = '/plantilla-solicitantes.xlsx';
    link.download = 'plantilla-solicitantes.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Por favor seleccione un archivo Excel");
      return;
    }

    try {
      setLoading(true);
      setProgress({
        total: 0,
        success: 0,
        errors: [],
        completed: false
      });

      const response = await importarSolicitantes(file);

      if (response.errores && response.errores.length > 0) {
        // Extraer el número de la cadena "Se encontraron X errores durante la importación"
        const totalErrors = response.errores.length;
        setProgress({
          total: totalErrors,
          success: 0,
          errors: response.errores,
          completed: true
        });
      } else {
        // Extraer el número de la cadena "Se importaron X solicitantes exitosamente"
        const successCount = parseInt(response.detail.match(/\d+/)[0], 10);
        setProgress({
          total: successCount,
          success: successCount,
          errors: [],
          completed: true
        });
      }

      if (!response.errores || response.errores.length === 0) {
        setTimeout(() => {
          onImportComplete();
          onClose();
        }, 2000);
      }
    } catch (error) {
      alert("Error al importar: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  if (!show) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Importar Solicitantes</h2>
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>

        <div className="import-section">
          <div className="alert alert-info mb-3">
            <strong>Requisitos del formato:</strong>
            <ul>
              <li>Número de teléfono: 10 dígitos empezando con 3 (ej: 3126066594)</li>
              <li>Tipo de rol: debe ser exactamente 'aprendiz', 'contratista', 'funcionario' o 'instructor' (sin puntos ni mayúsculas)</li>
              <li>Para aprendices: 'Número de ficha' y 'Programa de formación' son obligatorios</li>
              <li>Correo electrónico: debe ser un correo válido</li>
            </ul>
          </div>

          <button
            className="btn btn-secondary mb-3"
            onClick={handleDownloadTemplate}
          >
            Descargar Plantilla
          </button>

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <input
                type="file"
                accept=".xlsx"
                onChange={handleFileChange}
                className="form-control"
                disabled={loading}
              />
            </div>

            {loading && (
              <div className="progress mb-3">
                <div
                  className="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  style={{ width: "100%" }}
                >
                  Importando...
                </div>
              </div>
            )}

            {progress.completed && (
              <div className="results-section">
                <div className="alert alert-info">
                  <strong>Resultados de la importación:</strong>
                  <br />
                  Total procesados: {progress.total}
                  <br />
                  Importados exitosamente: {progress.success}
                  <br />
                  Errores encontrados: {progress.errors.length}
                </div>

                {progress.errors.length > 0 && (
                  <div className="alert alert-danger">
                    <strong>Errores:</strong>
                    <ul>
                      {progress.errors.map((error, index) => (
                        <li key={index}>{error}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary"
              disabled={!file || loading}
            >
              {loading ? "Importando..." : "Importar"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ImportarSolicitantesModal;
