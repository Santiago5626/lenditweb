import React, { useState, useEffect } from "react";
import { fetchProductos, agregarProducto, actualizarProducto, eliminarProducto, fetchTiposProducto } from "../api/peticiones";
import RegistrarProductoModal from "./RegistrarProductoModal";
import EditarProductoModal from "./EditarProductoModal";
import "../styles/components/TablaInventario.css";

const TablaInventario = () => {
  const [productos, setProductos] = useState([]);
  const [tiposProducto, setTiposProducto] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [filtroCodigo, setFiltroCodigo] = useState("");
  const [filtroTipo, setFiltroTipo] = useState("");

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

  return (
    <div className="container">
      <div className="controls-section">
        <div className="filters">
          <input
            type="text"
            className="form-control"
            placeholder="Filtrar por Código/Serial"
            value={filtroCodigo}
            onChange={(e) => setFiltroCodigo(e.target.value)}
          />
          <select
            className="form-control"
            value={filtroTipo}
            onChange={(e) => setFiltroTipo(e.target.value)}
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
        </div>
      </div>

      <div className="table-section">
        {productos.length === 0 ? (
          <div className="alert alert-info">
            No hay productos registrados
          </div>
        ) : (
          <table className="table table-bordered table-hover">
            <thead className="thead-light">
              <tr>
                <th>Seleccionar</th>
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
              {filtrarProductos().map((product) => (
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
    </div>
  );
};

export default TablaInventario;
