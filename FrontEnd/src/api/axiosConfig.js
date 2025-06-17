import { logout } from './auth';

const API_BASE_URL = "http://localhost:8000";

// Función para crear peticiones con manejo automático de autenticación
const createAuthenticatedFetch = (url, options = {}) => {
  const token = localStorage.getItem('token');
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers
    }
  };

  return fetch(`${API_BASE_URL}${url}`, config)
    .then(async (response) => {
      // Si el error es 401 (Unauthorized) o 403 (Forbidden)
      if (response.status === 401 || response.status === 403) {
        // Cerrar sesión y redirigir al login
        logout();
        throw new Error('Sesión expirada o inválida');
      }
      
      return response;
    })
    .catch((error) => {
      // Si es un error de red o el servidor no responde
      if (!error.response && error.message !== 'Sesión expirada o inválida') {
        throw new Error('Error de conexión con el servidor');
      }
      throw error;
    });
};

// Métodos HTTP simplificados
const apiClient = {
  get: (url, options = {}) => createAuthenticatedFetch(url, { method: 'GET', ...options }),
  post: (url, data, options = {}) => createAuthenticatedFetch(url, { 
    method: 'POST', 
    body: JSON.stringify(data),
    ...options 
  }),
  put: (url, data, options = {}) => createAuthenticatedFetch(url, { 
    method: 'PUT', 
    body: JSON.stringify(data),
    ...options 
  }),
  delete: (url, options = {}) => createAuthenticatedFetch(url, { method: 'DELETE', ...options })
};

export default apiClient;
