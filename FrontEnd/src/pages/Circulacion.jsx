import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import { fetchSolicitantes } from "../api/peticiones";
const Circulacion = () => {
  const [prestamo, setUsuarios] = useState([]); // Estado para almacenar los usuarios
  const [loading, setLoading] = useState(true); //estado para mostrar el cargando

  useEffect(() => {
    // Función para obtener los usuarios al montar el componente
    const obtenerSolicitantes = async () => {
      try {
        const data = await fetchSolicitantes(
          "http://127.0.0.1:8000/prestamo/obtener"
        );
        setUsuarios(data); // Guardamos los usuarios en el estado
      } catch (error) {
        console.error("Error al obtener los usuarios:", error);
      } finally {
        setLoading(false); // Indicamos que ya se terminó la carga
      }
    };

    obtenerSolicitantes(); // Llamamos a la función
  }, []); // El array vacío asegura que solo se ejecute una vez (al montar el componente)

  if (loading) {
    return <div>Cargando usuarios...</div>; // Muestra un mensaje de carga mientras se obtienen los datos
  }

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        justifyItems: "center",
        textAlign: "center",
      }}
    >
      <Sidebar />
      <main style={{ marginLeft: "180px", padding: "20px", flexGrow: 1 }}>
        <h1>PRESTAMOS</h1>

        <ul>
          {prestamo.length > 0 ? (
            prestamo.map((prestamo) => (
              <li key={prestamo.id}>
                ID: _{prestamo.id} Cedula Estudiante : {prestamo.ccEstudiante}
                ID PRODUCTO :{prestamo.idProducto} FECHA DE ENTREGA{" "}
                {prestamo.fechaFinal} ESTADO {prestamo.estado}
              </li>
            ))
          ) : (
            <li>NO HAY ESTUDIANTES DISPONIBLES</li>
          )}
        </ul>
        <button>AGREGAR</button>

        <button>ELIMINAR</button>
      </main>
    </div>
  );
};

export default Circulacion;
