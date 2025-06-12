import React, { useState, useRef, useEffect } from "react";
import "../styles/components/RegistrarModal.css";
import { importarSolicitantes } from "../api/peticiones";

const ImportarSolicitantesModal = ({ show, onClose, onImportComplete }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cancelled, setCancelled] = useState(false);
  const abortControllerRef = useRef(null);
  const fileInputRef = useRef(null);
  const [progress, setProgress] = useState({
    total: 0,
    processed: 0,
    success: 0,
    errors: [],
    completed: false,
    currentRow: 0,
    parcial: false
  });
  const [showErrorDetails, setShowErrorDetails] = useState(false);

  // Resetear el estado cuando el modal se abre
  useEffect(() => {
    if (show) {
      // Resetear todos los estados cuando se abre el modal
      setFile(null);
      setLoading(false);
      setCancelled(false);
      setShowErrorDetails(false);
      setProgress({
        total: 0,
        processed: 0,
        success: 0,
        errors: [],
        completed: false,
        currentRow: 0,
        parcial: false
      });

      // Limpiar el input de archivo
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

      // Cancelar cualquier operación en curso
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
        abortControllerRef.current = null;
      }
    }
  }, [show]);

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

  const handleCancel = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setCancelled(true);
    setLoading(false);
    setProgress(prev => ({
      ...prev,
      completed: true,
      errors: [...prev.errors, "Importación cancelada por el usuario"]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Por favor seleccione un archivo Excel");
      return;
    }

    try {
      setLoading(true);
      setCancelled(false);
      abortControllerRef.current = new AbortController();

      setProgress({
        total: 0,
        success: 0,
        errors: [],
        completed: false,
        parcial: false
      });

      const response = await importarSolicitantes(file, abortControllerRef.current.signal);

      if (cancelled) {
        return;
      }

      // Actualizar progreso con los datos del servidor
      if (response.columnas_disponibles) {
        // Error en el formato del archivo
        setProgress({
          total: 0,
          processed: 0,
          success: 0,
          errors: [
            `Error en el formato del archivo:`,
            `Columnas requeridas: ${response.columnas_requeridas.join(', ')}`,
            `Columnas encontradas: ${response.columnas_disponibles.join(', ')}`
          ],
          completed: true,
          currentRow: 0,
          parcial: false
        });
      } else {
        // Procesar la respuesta normal
        const errores = response.errores || [];

        setProgress({
          total: response.total_procesados || 0,
          processed: response.total_procesados || 0,
          success: response.exitosos || 0,
          errors: errores,
          completed: true,
          currentRow: response.total_procesados || 0,
          parcial: response.parcial || false
        });
      }

      // Solo cerrar automáticamente si no hay errores
      if (response.exitosos > 0 && (!response.errores || response.errores.length === 0)) {
        setTimeout(() => {
          onImportComplete();
          onClose();
        }, 2000);
      } else if (response.exitosos > 0) {
        // Si hay importaciones exitosas, actualizar la tabla
        onImportComplete();
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('Importación cancelada');
        return;
      }

      // Intentar extraer los errores detallados de la respuesta
      let errorData = null;
      let errorMessages = [];

      try {
        // Intentar parsear la respuesta JSON completa
        errorData = JSON.parse(error.message);

        if (errorData.errores && Array.isArray(errorData.errores)) {
          // Si hay errores específicos, usarlos
          errorMessages = errorData.errores;

          // Actualizar el progreso con los datos completos
          setProgress({
            total: errorData.total_procesados || 0,
            processed: errorData.total_procesados || 0,
            success: errorData.exitosos || 0,
            errors: errorMessages,
            completed: true,
            currentRow: errorData.total_procesados || 0,
            parcial: errorData.parcial || false
          });

          // Si hay importaciones exitosas, actualizar la tabla
          if (errorData.exitosos > 0) {
            onImportComplete();
          }

          return; // Salir aquí para evitar el setProgress de abajo
        } else if (errorData.detail) {
          errorMessages = [errorData.detail];
        } else {
          errorMessages = [error.message];
        }
      } catch {
        // Si no se puede parsear, usar el mensaje de error original
        errorMessages = [error.message];
      }

      setProgress(prev => ({
        ...prev,
        completed: true,
        errors: errorMessages
      }));
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
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
            <strong>Validaciones:</strong>
            <ul>
              <li>Número de teléfono: 10 dígitos empezando con 3 (ej: 3126066594)</li>
              <li>Tipo de rol: debe ser exactamente 'aprendiz', 'contratista', 'funcionario' o 'instructor' (sin puntos ni mayúsculas)</li>
              <li>Para aprendices: 'Número de ficha' y 'Programa de formación' son obligatorios</li>
              <li>Correo electrónico: opcional, pero si se proporciona debe ser un correo válido con formato usuario@dominio</li>
              <li>No se permiten correos duplicados</li>
              <li>No se permiten identificaciones duplicadas</li>
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
                ref={fileInputRef}
                type="file"
                accept=".xlsx"
                onChange={handleFileChange}
                className="form-control"
                disabled={loading}
              />
            </div>

            {loading && (
              <div className="mb-3">
                <div className="progress">
                  <div
                    className="progress-bar progress-bar-striped progress-bar-animated"
                    role="progressbar"
                    style={{ width: "100%" }}
                  >
                    {cancelled ? 'Cancelando...' : 'Procesando archivo...'}
                  </div>
                </div>
                <div className="mt-2 text-center">
                  <small>
                    {cancelled
                      ? 'Cancelando importación...'
                      : 'Importando solicitantes, por favor espere...'}
                  </small>
                </div>
                <div className="mt-2 text-center">
                  <button
                    type="button"
                    className="btn btn-danger btn-sm"
                    onClick={handleCancel}
                    disabled={cancelled}
                  >
                    {cancelled ? 'Cancelando...' : 'Cancelar Importación'}
                  </button>
                </div>
              </div>
            )}

            {progress.completed && (
              <div className="results-section">
                <div className={`alert ${progress.success > 0 ? (progress.parcial ? 'alert-warning' : 'alert-success') : 'alert-danger'}`}>
                  <strong>Resultados de la importación:</strong>
                  <br />
                  Total procesados: {progress.total}
                  <br />
                  Importados exitosamente: {progress.success}
                  <br />
                  Errores encontrados: {progress.errors.length}
                  {progress.parcial && (
                    <>
                      <br />
                      <strong>⚠️ Importación parcial: algunos registros no pudieron ser importados</strong>
                    </>
                  )}
                </div>

                {progress.errors.length > 0 && (
                  <div className="alert alert-danger">
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <strong>Errores encontrados:</strong>
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => setShowErrorDetails(!showErrorDetails)}
                      >
                        {showErrorDetails ? 'Ocultar detalles' : 'Ver detalles de errores'}
                      </button>
                    </div>

                    {showErrorDetails && (
                      <div style={{ maxHeight: '300px', overflowY: 'auto', backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '4px' }}>
                        <ul style={{ marginBottom: 0, fontSize: '0.9em', paddingLeft: '20px' }}>
                          {progress.errors.map((error, index) => {
                            // Extraer el número de fila si existe
                            const rowMatch = error.match(/Fila (\d+):/);
                            const rowNumber = rowMatch ? rowMatch[1] : null;

                            // Extraer el mensaje principal y dividir múltiples errores
                            const message = error.replace(/^(Fila \d+: )?/, '');
                            const multipleErrors = message.split('; ');

                            return (
                              <li key={index} style={{
                                marginBottom: '12px',
                                wordBreak: 'break-word',
                                borderBottom: '1px solid #dee2e6',
                                paddingBottom: '10px'
                              }}>
                                {rowNumber && (
                                  <div style={{ marginBottom: '6px' }}>
                                    <strong style={{ color: '#dc3545', fontSize: '1em' }}>Fila {rowNumber}:</strong>
                                  </div>
                                )}
                                {multipleErrors.length > 1 ? (
                                  <ul style={{ marginLeft: '15px', marginBottom: 0, paddingLeft: '15px' }}>
                                    {multipleErrors.map((singleError, errorIndex) => (
                                      <li key={errorIndex} style={{
                                        marginBottom: '4px',
                                        color: '#6c757d',
                                        listStyleType: 'disc'
                                      }}>
                                        {singleError.trim()}
                                      </li>
                                    ))}
                                  </ul>
                                ) : (
                                  <span style={{ color: '#6c757d', marginLeft: rowNumber ? '15px' : '0' }}>
                                    {message}
                                  </span>
                                )}
                              </li>
                            );
                          })}
                        </ul>
                      </div>
                    )}

                    {!showErrorDetails && (
                      <p className="mb-0">
                        Se encontraron {progress.errors.length} error(es). Use el botón "Ver detalles de errores" para más información.
                      </p>
                    )}
                  </div>
                )}

                {progress.success > 0 && (
                  <div className="alert alert-success">
                    <strong>✅ {progress.success} solicitantes fueron importados exitosamente</strong>
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
