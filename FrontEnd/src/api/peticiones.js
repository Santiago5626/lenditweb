export async function fetchSolicitantes(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok) {
      throw new Error("No se pudieron obtener los datos");
    }

    return data;
  } catch (error) {
    console.error("Error al obtener los datos:", error);
    throw error;
  }
}

export async function agregar(cc, nombre, apellido, email) {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/estudiantes/registrar",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ cc, nombre, apellido, email }),
      }
    );

    const data = await response.json();

    if (response.ok) {
      throw new Error(data.message || "Error en agregar");
    }

    return data;
  } catch (error) {
    throw error;
  }
}

export async function actualizar(cc, nombre, apellido, email) {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/estudiantes/actualizar",
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ cc, nombre, apellido, email }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Error al actualizar");
    }

    return data;
  } catch (error) {
    throw error;
  }
}

export async function eliminar(cc) {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/estudiantes/eliminar",
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ cc }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Error al eliminar");
    }

    return data;
  } catch (error) {
    throw error;
  }
}
