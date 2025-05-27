const API_BASE_URL = "http://localhost:8000";

// Función auxiliar para obtener el token
const getAuthHeaders = (isMultipart = false) => {
  const token = localStorage.getItem('token');
  if (isMultipart) {
    return {
      'Authorization': token ? `Bearer ${token}` : ''
    };
  }
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
};

export async function importarSolicitantes(file) {
  try {
    console.log('Iniciando importación de archivo:', file.name);
    const formData = new FormData();
    formData.append('file', file);

    const headers = getAuthHeaders(true);
    console.log('Headers de la petición:', headers);

    const response = await fetch(`${API_BASE_URL}/solicitantes/importar-excel`, {
      method: 'POST',
      headers: headers,
      body: formData,
      credentials: 'include'
    });

    console.log('Respuesta del servidor:', response.status, response.statusText);

    let data;
    const textResponse = await response.text();
    try {
      data = JSON.parse(textResponse);
      console.log('Datos recibidos:', data);
    } catch (e) {
      console.error('Error al parsear respuesta:', textResponse);
      throw new Error('Error al procesar la respuesta del servidor');
    }

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      throw new Error(data.detail || data.message || "Error al importar solicitantes");
    }

    return data;
  } catch (error) {
    console.error("Error detallado al importar solicitantes:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

export async function fetchSolicitantes() {
  try {
    console.log('Intentando obtener solicitantes...');
    const response = await fetch(`${API_BASE_URL}/solicitantes/obtener`, {
      method: 'GET',
      headers: getAuthHeaders(),
      credentials: 'include'
    });

    console.log('Respuesta del servidor:', response.status);

    if (!response.ok) {
      if (response.status === 401) {
        // Si no está autorizado, redirigir al login
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error al obtener los datos");
    }

    const data = await response.json();
    console.log('Datos recibidos:', data);

    // Si no hay datos, devolver array vacío
    if (!data) return [];

    // Si la respuesta es un objeto con mensaje de error
    if (data.detail) {
      throw new Error(data.detail);
    }

    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

export async function agregar(solicitanteData) {
  try {
    console.log('Datos a enviar:', solicitanteData);
    const response = await fetch(
      `${API_BASE_URL}/solicitantes/registrar`,
      {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(solicitanteData),
        credentials: 'include'
      }
    );

    const data = await response.json();
    console.log('Respuesta del servidor:', data);

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      throw new Error(data.detail || "Error al agregar solicitante");
    }

    return data;
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

export async function actualizar(solicitanteData) {
  try {
    console.log('Datos a actualizar:', solicitanteData);
    const response = await fetch(
      `${API_BASE_URL}/solicitantes/actualizar`,
      {
        method: "PUT",
        headers: getAuthHeaders(),
        body: JSON.stringify(solicitanteData),
        credentials: 'include'
      }
    );

    const data = await response.json();
    console.log('Respuesta del servidor:', data);

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      throw new Error(data.detail || "Error al actualizar solicitante");
    }

    return data;
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

export async function eliminar(identificacion) {
  try {
    console.log('Intentando eliminar solicitante:', identificacion);
    const response = await fetch(
      `${API_BASE_URL}/solicitantes/eliminar`,
      {
        method: "DELETE",
        headers: getAuthHeaders(),
        body: JSON.stringify({ identificacion }),
        credentials: 'include'
      }
    );

    const data = await response.json();
    console.log('Respuesta del servidor:', data);

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      throw new Error(data.detail || "Error al eliminar solicitante");
    }

    return data;
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

// Función auxiliar para verificar el estado del servidor
export async function checkServerStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/solicitantes/obtener`, {
      method: 'GET',
      headers: getAuthHeaders(),
      credentials: 'include'
    });
    return response.ok;
  } catch (error) {
    console.error("Error al verificar el estado del servidor:", error);
    return false;
  }
}

// Funciones para productos
export async function fetchProductos() {
  try {
    console.log('Intentando obtener productos...');
    const response = await fetch(`${API_BASE_URL}/productos/`, {
      method: 'GET',
      headers: getAuthHeaders(),
      credentials: 'include'
    });

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error al obtener los productos");
    }

    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

export async function agregarProducto(productoData) {
  try {
    console.log('Datos del producto a enviar:', productoData);
    const response = await fetch(
      `${API_BASE_URL}/productos/`,
      {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(productoData),
        credentials: 'include'
      }
    );

    const data = await response.json();
    console.log('Respuesta del servidor:', data);

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      throw new Error(data.detail || "Error al agregar producto");
    }

    return data;
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

export async function actualizarProducto(productoData) {
  try {
    console.log('Datos del producto a actualizar:', productoData);
    const response = await fetch(
      `${API_BASE_URL}/productos/${productoData.codigoInterno}`,
      {
        method: "PUT",
        headers: getAuthHeaders(),
        body: JSON.stringify(productoData),
        credentials: 'include'
      }
    );

    const data = await response.json();
    console.log('Respuesta del servidor:', data);

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      throw new Error(data.detail || "Error al actualizar producto");
    }

    return data;
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}

export async function getContadores() {
  try {
    const response = await fetch(`${API_BASE_URL}/productos/contadores`, {
      method: 'GET',
      headers: getAuthHeaders(),
      credentials: 'include'
    });

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error al obtener los contadores");
    }

    return await response.json();
  } catch (error) {
    console.error("Error al obtener contadores:", error);
    throw error;
  }
}

export async function eliminarProducto(codigoInterno) {
  try {
    console.log('Intentando eliminar producto:', codigoInterno);
    const response = await fetch(
      `${API_BASE_URL}/productos/${codigoInterno}`,
      {
        method: "DELETE",
        headers: getAuthHeaders(),
        credentials: 'include'
      }
    );

    const data = await response.json();
    console.log('Respuesta del servidor:', data);

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }
      throw new Error(data.detail || "Error al eliminar producto");
    }

    return data;
  } catch (error) {
    console.error("Error detallado:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    throw error;
  }
}
