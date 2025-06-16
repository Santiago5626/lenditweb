import React, { useState, useEffect } from "react";
import { fetchProductos, agregarProducto, actualizarProducto, eliminarProducto, fetchTiposProducto } from "../api/peticiones";
import RegistrarProductoModal from "./RegistrarProductoModal";
import EditarProductoModal from "./EditarProductoModal";
import ImportarProductosModal from "./ImportarProductosModal";
import PaginationControls from "./PaginationControls";
import "../styles/components/TablaInventario.css";

const TablaInventario = () => {
  const [productos, setProductos] = useState([]);
  const [tiposProducto, setTiposProducto] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [filtroCodigo, setFiltroCodigo] = useState("");
  const [filtroTipo, setFiltroTipo] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [productosData, tiposData] = await Promise.all([
        fetchProductos(),
        fetchTiposProducto()
      ]);
      setProductos(productosData);
      setTiposProducto(tiposData);
      setLoading(false);
    } catch (error) {
      console.error("Error al cargar datos:", error);
      setError(error.message || "Error al cargar los datos");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRegister = async (productoData) => {
    try {
      await agregarProducto(productoData);
      alert("¡Producto agregado exitosamente!");
      setShowModal(false);
      await fetchData();
    } catch (error) {
      console.error("Error al registrar:", error);
      alert("Error al agregar producto: " + error.message);
    }
  };

  const handleEdit = async (productoData) => {
    try {
      await actualizarProducto(productoData);
      alert("¡Producto actualizado exitosamente!");
      setShowEditModal(false);
      await fetchData();
      setSelectedProduct(null);
    } catch (error) {
      console.error("Error al actualizar:", error);
      alert("Error al actualizar producto: " + error.message);
    }
  };

  const handleDelete = async () => {
    if (!selectedProduct) {
      alert("Por favor seleccione un producto para eliminar");
      return;
    }

    if (window.confirm(`¿Está seguro que desea eliminar el producto ${selectedProduct.NOMBRE}?`)) {
      try {
        await eliminarProducto(selectedProduct.CODIGO_INTERNO);
        alert("¡Producto eliminado exitosamente!");
        await fetchData();
        setSelectedProduct(null);
      } catch (error) {
        console.error("Error al eliminar:", error);
        alert("Error al eliminar producto: " + error.message);
      }
    }
  };

  const handleCheckboxChange = (product) => {
    setSelectedProduct(product === selectedProduct ? null : product);
  };

  const handleEditClick = () => {
    if (!selectedProduct) {
      alert("Por favor seleccione un producto para editar");
      return;
    }
    setShowEditModal(true);
  };

  const filtrarProductos = () => {
    return productos.filter(product => {
      const codigoInterno = product.CODIGO_INTERNO || '';
      const placaSena = product.PLACA_SENA || '';
      const serial = product.SERIAL || '';
      const idTipo = product.IDTIPOPRODUCTO;

      const matchCodigo = codigoInterno.toLowerCase().includes(filtroCodigo.toLowerCase()) ||
        placaSena.toLowerCase().includes(filtroCodigo.toLowerCase()) ||
        serial.toLowerCase().includes(filtroCodigo.toLowerCase());
      const matchTipo = filtroTipo === "" || idTipo.toString() === filtroTipo;
      return matchCodigo && matchTipo;
    });
  };

  const getTipoProductoNombre = (idTipo) => {
    const tipo = tiposProducto.find(t => t.IDTIPOPRODUCTO === idTipo);
    return tipo ? tipo.NOMBRE_TIPO_PRODUCTO : 'Desconocido';
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
        <p>Cargando inventario...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container alert alert-danger">
        <h4>Error al cargar los datos</h4>
        <p>{error}</p>
        <button
          className="btn btn-primary mt-3"
          onClick={fetchData}
        >
          Intentar nuevamente
        </button>
      </div>
    );
  }

  const filteredProducts = filtrarProductos();

  return (
    <div className="container">
      <div className="controls-section">
        <div className="filters">
          <input
            type="text"
            className="form-control"
            placeholder="Filtrar por Código/Serial"
            value={filtroCodigo}
            onChange={(e) => {
              setFiltroCodigo(e.target.value);
              setCurrentPage(1);
            }}
          />
          <select
            className="form-control"
            value={filtroTipo}
            onChange={(e) => {
              setFiltroTipo(e.target.value);
              setCurrentPage(1);
            }}
          >
            <option value="">Todos los tipos</option>
            {tiposProducto.map(tipo => (
              <option key={tipo.IDTIPOPRODUCTO} value={tipo.IDTIPOPRODUCTO.toString()}>
                {tipo.NOMBRE_TIPO_PRODUCTO}
              </option>
            ))}
          </select>
        </div>
        <div className="buttons">
          <button
            className="btn btn-outline-danger"
            onClick={handleDelete}
            title="Eliminar producto"
          >
            <span className="material-symbols-outlined">delete</span>
          </button>
          <button
            className="btn btn-outline-primary"
            onClick={handleEditClick}
            title="Editar producto"
          >
            <span className="material-symbols-outlined">edit</span>
          </button>
          <button
            className="btn btn-outline-success"
            onClick={() => setShowModal(true)}
            title="Agregar producto"
          >
            <span className="material-symbols-outlined">laptop_mac</span>
            <span className="material-symbols-outlined add-icon">add</span>
          </button>
          <button
            className="btn btn-outline-info"
            onClick={() => setShowImportModal(true)}
            title="Importar desde Excel"
          >
            <span className="material-symbols-outlined">upload_file</span>
          </button>
        </div>
      </div>

      <div className="table-section">
        {productos.length === 0 ? (
          <div className="alert alert-info">
            No hay productos registrados
          </div>
        ) : (
          <>
            {/* Controles superiores de paginación */}
            <div className="pagination-top-controls">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <div className="pagination-info">
                  <small className="text-muted">
                    Mostrando {((currentPage - 1) * itemsPerPage) + 1} - {Math.min(currentPage * itemsPerPage, filteredProducts.length)} de {filteredProducts.length} registros
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

            <table className="table table-bordered table-hover">
              <thead className="thead-light">
                <tr>
                  <th>Sel.</th>
                  <th>Código Interno</th>
                  <th>PLACA SENA</th>
                  <th>Serial</th>
                  <th>Nombre</th>
                  <th>Marca</th>
                  <th>Tipo</th>
                  <th>Estado</th>
                  <th>Observaciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredProducts
                  .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
                  .map((product) => (
                    <tr
                      key={product.CODIGO_INTERNO}
                      className={selectedProduct === product ? "table-active" : ""}
                    >
                      <td>
                        <input
                          type="checkbox"
                          checked={selectedProduct === product}
                          onChange={() => handleCheckboxChange(product)}
                        />
                      </td>
                      <td>{product.CODIGO_INTERNO}</td>
                      <td>{product.PLACA_SENA || '-'}</td>
                      <td>{product.SERIAL || '-'}</td>
                      <td>{product.NOMBRE}</td>
                      <td>{product.MARCA || '-'}</td>
                      <td>{getTipoProductoNombre(product.IDTIPOPRODUCTO)}</td>
                      <td>{product.ESTADO}</td>
                      <td>{product.OBSERVACIONES || '-'}</td>
                    </tr>
                  ))}
              </tbody>
            </table>

            {/* Controles inferiores de navegación */}
            {Math.ceil(filteredProducts.length / itemsPerPage) > 1 && (
              <div className="pagination-bottom d-flex justify-content-center mt-4">
                <nav aria-label="Paginación de productos">
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
                      const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);
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
                    <li className={`page-item ${currentPage === Math.ceil(filteredProducts.length / itemsPerPage) ? 'disabled' : ''}`}>
                      <button
                        className="page-link"
                        onClick={() => setCurrentPage(currentPage + 1)}
                        disabled={currentPage === Math.ceil(filteredProducts.length / itemsPerPage)}
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

      <RegistrarProductoModal
        show={showModal}
        onClose={() => setShowModal(false)}
        onRegister={handleRegister}
      />

      <EditarProductoModal
        show={showEditModal}
        onClose={() => {
          setShowEditModal(false);
          setSelectedProduct(null);
        }}
        onEdit={handleEdit}
        productData={selectedProduct}
      />

      <ImportarProductosModal
        show={showImportModal}
        onClose={() => setShowImportModal(false)}
        onImportComplete={fetchData}
      />
    </div>
  );
};

export default TablaInventario;
