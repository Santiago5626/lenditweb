import apiClient from './axiosConfig';

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

// Función auxiliar para manejar errores
const handleError = (error) => {
  console.error("Error detallado:", {
    message: error.message,
    stack: error.stack,
    name: error.name
  });
  
  // Si es un error de red o el servidor no responde
  if (!error.response) {
    throw new Error('Error de conexión con el servidor');
  }

  // Si es un error de autenticación, el interceptor ya se encarga de redirigir
  if (error.response && (error.response.status === 401 || error.response.status === 403)) {
    throw new Error('Sesión expirada o inválida');
  }

  // Para otros errores, usar el mensaje del servidor o uno genérico
  const errorMessage = error.response?.data?.detail || error.response?.data?.message || 'Error en la operación';
  throw new Error(errorMessage);
};

export async function importarSolicitantes(file, signal = null) {
  // Declarar timeoutId fuera del try para que esté disponible en finally
  let timeoutId = null;

  try {
    console.log('Iniciando importación de archivo:', file.name, 'Tipo:', file.type, 'Tamaño:', file.size);

    // Validar el archivo antes de enviarlo
    if (!file.name.endsWith('.xlsx')) {
      throw new Error('El archivo debe tener extensión .xlsx');
    }

    if (file.size === 0) {
      throw new Error('El archivo está vacío');
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB
      throw new Error('El archivo es demasiado grande (máximo 10MB)');
    }

    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('token');
    const headers = {
      'Authorization': token ? `Bearer ${token}` : '',
    };
    console.log('Headers de la petición:', headers);
    console.log('FormData creado, enviando petición...');

    // Crear un AbortController para el timeout
    const timeoutController = new AbortController();
    timeoutId = setTimeout(() => timeoutController.abort(), 30000); // 30 segundos de timeout

    // Usar el signal proporcionado o el de timeout
    let finalSignal = timeoutController.signal;

    if (signal) {
      // Si hay un signal de cancelación manual, escuchar ambos
      signal.addEventListener('abort', () => {
        if (timeoutId) clearTimeout(timeoutId);
        timeoutController.abort();
      });
      finalSignal = signal;
    }

    const fetchOptions = {
      method: 'POST',
      headers: headers,
      body: formData,
      credentials: 'include',
      signal: finalSignal
    };

    const response = await fetch(`${API_BASE_URL}/solicitantes/importar-excel`, fetchOptions);
    if (timeoutId) clearTimeout(timeoutId);

    console.log('Respuesta del servidor:', response.status, response.statusText);
    console.log('Headers de respuesta:', Object.fromEntries(response.headers.entries()));

    let data;
    const textResponse = await response.text();
    console.log('Respuesta cruda del servidor:', textResponse);

    try {
      data = JSON.parse(textResponse);
      console.log('Datos parseados:', data);
    } catch (e) {
      console.error('Error al parsear respuesta JSON:', e);
      console.error('Respuesta que no se pudo parsear:', textResponse);
      throw new Error(`Error al procesar la respuesta del servidor: ${textResponse}`);
    }

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }

      // Si hay errores específicos en la respuesta, los usamos directamente
      if (data.errores && Array.isArray(data.errores)) {
        throw new Error(JSON.stringify(data)); // Enviamos toda la respuesta para mantener la estructura
      }

      // Si no hay errores específicos, lanzamos el error general
      console.error('Error del servidor:', response.status, data);
      throw new Error(data.detail || data.message || `Error ${response.status}: ${response.statusText}`);
    }

    return data;
  } catch (error) {
    if (error.name === 'AbortError') {
      if (error.message.includes('timeout')) {
        console.error('=== IMPORTACIÓN CANCELADA POR TIMEOUT ===');
        throw new Error('La importación excedió el tiempo límite de 30 segundos');
      } else {
        console.log('=== IMPORTACIÓN CANCELADA POR USUARIO ===');
        throw error;
      }
    }
    console.error("Error detallado al importar solicitantes:", {
      message: error.message,
      stack: error.stack,
      name: error.name,
      fileName: file?.name,
      fileSize: file?.size,
      fileType: file?.type
    });
    throw error;
  } finally {
    // Limpiar recursos
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  }
}

export async function fetchSolicitantes() {
  try {
    console.log('Intentando obtener solicitantes...');
    const response = await apiClient.get('/solicitantes/obtener');
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
    handleError(error);
  }
}

export async function agregar(solicitanteData) {
  try {
    console.log('Datos a enviar:', solicitanteData);
    const response = await apiClient.post('/solicitantes/registrar', solicitanteData);
    const data = await response.json();
    console.log('Respuesta del servidor:', data);
    return data;
  } catch (error) {
    handleError(error);
  }
}

export async function actualizar(solicitanteData) {
  try {
    console.log('Datos a actualizar:', solicitanteData);
    const response = await apiClient.put('/solicitantes/actualizar', solicitanteData);
    const data = await response.json();
    console.log('Respuesta del servidor:', data);
    return data;
  } catch (error) {
    handleError(error);
  }
}

export async function eliminar(identificacion) {
  try {
    console.log('Intentando eliminar solicitante:', identificacion);
    const response = await apiClient.delete('/solicitantes/eliminar', { 
      body: JSON.stringify({ identificacion }) 
    });
    const data = await response.json();
    console.log('Respuesta del servidor:', data);
    return data;
  } catch (error) {
    handleError(error);
  }
}

export async function eliminarMultiples(identificaciones) {
  try {
    console.log('Intentando eliminar múltiples solicitantes:', identificaciones);
    const response = await fetch(
      `${API_BASE_URL}/solicitantes/eliminar-multiples`,
      {
        method: "DELETE",
        headers: getAuthHeaders(),
        body: JSON.stringify({ identificaciones }),
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
      throw new Error(data.detail || "Error al eliminar solicitantes");
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

// Funciones para tipos de producto
export async function fetchTiposProducto() {
  try {
    const response = await fetch(`${API_BASE_URL}/tipos-producto/`, {
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
      throw new Error(errorData.detail || "Error al obtener los tipos de producto");
    }

    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Error al obtener tipos de producto:", error);
    throw error;
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
    const codigoInterno = productoData.codigoInterno || productoData.CODIGO_INTERNO;
    const response = await fetch(
      `${API_BASE_URL}/productos/${codigoInterno}`,
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

export async function importarProductos(file, signal = null) {
  // Declarar timeoutId fuera del try para que esté disponible en finally
  let timeoutId = null;

  try {
    console.log('Iniciando importación de productos:', file.name, 'Tipo:', file.type, 'Tamaño:', file.size);

    // Validar el archivo antes de enviarlo
    if (!file.name.endsWith('.xlsx')) {
      throw new Error('El archivo debe tener extensión .xlsx');
    }

    if (file.size === 0) {
      throw new Error('El archivo está vacío');
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB
      throw new Error('El archivo es demasiado grande (máximo 10MB)');
    }

    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('token');
    const headers = {
      'Authorization': token ? `Bearer ${token}` : '',
    };
    console.log('Headers de la petición:', headers);
    console.log('FormData creado, enviando petición...');

    // Crear un AbortController para el timeout
    const timeoutController = new AbortController();
    timeoutId = setTimeout(() => timeoutController.abort(), 30000); // 30 segundos de timeout

    // Usar el signal proporcionado o el de timeout
    let finalSignal = timeoutController.signal;

    if (signal) {
      // Si hay un signal de cancelación manual, escuchar ambos
      signal.addEventListener('abort', () => {
        if (timeoutId) clearTimeout(timeoutId);
        timeoutController.abort();
      });
      finalSignal = signal;
    }

    const fetchOptions = {
      method: 'POST',
      headers: headers,
      body: formData,
      credentials: 'include',
      signal: finalSignal
    };

    const response = await fetch(`${API_BASE_URL}/productos/importar-excel`, fetchOptions);
    if (timeoutId) clearTimeout(timeoutId);

    console.log('Respuesta del servidor:', response.status, response.statusText);
    console.log('Headers de respuesta:', Object.fromEntries(response.headers.entries()));

    let data;
    const textResponse = await response.text();
    console.log('Respuesta cruda del servidor:', textResponse);

    try {
      data = JSON.parse(textResponse);
      console.log('Datos parseados:', data);
    } catch (e) {
      console.error('Error al parsear respuesta JSON:', e);
      console.error('Respuesta que no se pudo parsear:', textResponse);
      throw new Error(`Error al procesar la respuesta del servidor: ${textResponse}`);
    }

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Sesión expirada o inválida');
      }

      // Si hay errores específicos en la respuesta, los usamos directamente
      if (data.errores && Array.isArray(data.errores)) {
        throw new Error(JSON.stringify(data)); // Enviamos toda la respuesta para mantener la estructura
      }

      // Si no hay errores específicos, lanzamos el error general
      console.error('Error del servidor:', response.status, data);
      throw new Error(data.detail || data.message || `Error ${response.status}: ${response.statusText}`);
    }

    return data;
  } catch (error) {
    if (error.name === 'AbortError') {
      if (error.message.includes('timeout')) {
        console.error('=== IMPORTACIÓN CANCELADA POR TIMEOUT ===');
        throw new Error('La importación excedió el tiempo límite de 30 segundos');
      } else {
        console.log('=== IMPORTACIÓN CANCELADA POR USUARIO ===');
        throw error;
      }
    }
    console.error("Error detallado al importar productos:", {
      message: error.message,
      stack: error.stack,
      name: error.name,
      fileName: file?.name,
      fileSize: file?.size,
      fileType: file?.type
    });
    throw error;
  } finally {
    // Limpiar recursos
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  }
}

// Funciones para solicitudes y préstamos
export async function fetchSolicitudes() {
  try {
    console.log('Intentando obtener solicitudes...');
    const response = await fetch(`${API_BASE_URL}/solicitudes/obtener`, {
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
      throw new Error(errorData.detail || "Error al obtener las solicitudes");
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

export async function crearSolicitud(solicitudData) {
  try {
    console.log('Datos de la solicitud a enviar:', solicitudData);
    const response = await fetch(
      `${API_BASE_URL}/solicitudes/crear`,
      {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(solicitudData),
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
      throw new Error(data.detail || "Error al crear solicitud");
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

export async function agregarProductoASolicitud(productoSolicitudData) {
  try {
    console.log('Datos del producto-solicitud a enviar:', productoSolicitudData);
    const response = await fetch(
      `${API_BASE_URL}/solicitudes/agregar-producto`,
      {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(productoSolicitudData),
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
      throw new Error(data.detail || "Error al agregar producto a la solicitud");
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

export async function crearPrestamo(prestamoData) {
  try {
    console.log('Datos del préstamo a enviar:', prestamoData);
    const response = await fetch(
      `${API_BASE_URL}/prestamo/crear`,
      {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(prestamoData),
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
      throw new Error(data.detail || "Error al crear préstamo");
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

export async function fetchPrestamos() {
  try {
    console.log('Intentando obtener préstamos...');
    const response = await fetch(`${API_BASE_URL}/prestamo/obtener`, {
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
      throw new Error(errorData.detail || "Error al obtener los préstamos");
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

export async function devolverPrestamo(idPrestamo) {
  try {
    console.log('Intentando devolver préstamo:', idPrestamo);
    const response = await fetch(
      `${API_BASE_URL}/prestamo/${idPrestamo}/devolver`,
      {
        method: "PUT",
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
      throw new Error(data.detail || "Error al devolver el préstamo");
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

export async function actualizarEstadoSolicitud(solicitudData) {
  try {
    console.log('Datos de actualización de solicitud:', solicitudData);
    const response = await fetch(
      `${API_BASE_URL}/solicitudes/actualizar-estado`,
      {
        method: "PUT",
        headers: getAuthHeaders(),
        body: JSON.stringify(solicitudData),
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
      throw new Error(data.detail || "Error al actualizar estado de la solicitud");
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

export async function prolongarPrestamo(idPrestamo, dias = 7) {
  try {
    console.log('Intentando prolongar préstamo:', idPrestamo, 'por', dias, 'días');
    const response = await fetch(
      `${API_BASE_URL}/prestamo/${idPrestamo}/prolongar`,
      {
        method: "PUT",
        headers: getAuthHeaders(),
        body: JSON.stringify({ dias }),
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
      throw new Error(data.detail || "Error al prolongar el préstamo");
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
