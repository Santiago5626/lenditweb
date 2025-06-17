const API_BASE_URL = "http://localhost:8000";

// Tiempo de inactividad antes de cerrar sesión (en minutos)
const INACTIVITY_TIMEOUT = 30;
let inactivityTimer;
let lastActivity = Date.now();

// Función para reiniciar el temporizador de inactividad
function resetInactivityTimer() {
  lastActivity = Date.now();
  clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(logout, INACTIVITY_TIMEOUT * 60 * 1000);
}

// Función para actualizar el token si hay actividad reciente
async function refreshTokenIfNeeded() {
  const token = getToken();
  if (!token) return false;

  const timeSinceLastActivity = Date.now() - lastActivity;
  // Si ha habido actividad en los últimos 5 minutos, refrescar el token
  if (timeSinceLastActivity < 5 * 60 * 1000) {
    try {
      const response = await fetch(`${API_BASE_URL}/usuario/refresh-token`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.token) {
          localStorage.setItem("token", data.token);
          resetInactivityTimer();
          return true;
        }
      }
    } catch (error) {
      console.error("Error al refrescar el token:", error);
    }
  }
  return false;
}

// Configurar listeners para actividad del usuario
function setupActivityListeners() {
  const events = ['mousedown', 'keydown', 'scroll', 'touchstart'];
  events.forEach(event => {
    document.addEventListener(event, () => {
      resetInactivityTimer();
      refreshTokenIfNeeded();
    });
  });
}

export async function login(nombre, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/usuario/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nombre,
        password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Error en el inicio de sesión");
    }

    // Guardar el token y datos del usuario en localStorage
    if (data.success) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));

      // Configurar listeners de actividad y temporizador
      setupActivityListeners();
      resetInactivityTimer();
    }

    return data;
  } catch (error) {
    console.error("Error en login:", error);
    throw error;
  }
}

export function logout() {
  clearTimeout(inactivityTimer);
  localStorage.removeItem("token");
  localStorage.removeItem("user");

  // Verificar si estamos en la página de login antes de redirigir
  if (window.location.pathname !== "/" && window.location.pathname !== "/login") {
    window.location.href = "/";
  }
}

export function isAuthenticated() {
  const token = localStorage.getItem("token");
  return !!token;
}

// Función para obtener el token actual
export function getToken() {
  return localStorage.getItem("token");
}

// Función para obtener los datos del usuario actual
export function getCurrentUser() {
  const userStr = localStorage.getItem("user");
  return userStr ? JSON.parse(userStr) : null;
}

// Función para verificar si el token ha expirado o es inválido
export async function verifyToken() {
  const token = getToken();
  if (!token) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/usuario/verify-token`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) {
      logout();
      return false;
    }

    return true;
  } catch (error) {
    console.error("Error al verificar el token:", error);
    return false;
  }
}

// Función para inicializar el sistema de refresh token al cargar la aplicación
export function initializeAuth() {
  if (isAuthenticated()) {
    setupActivityListeners();
    resetInactivityTimer();
  }
}

// Función para refrescar manualmente el token
export async function refreshToken() {
  const token = getToken();
  if (!token) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/usuario/refresh-token`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      if (data.token) {
        localStorage.setItem("token", data.token);
        resetInactivityTimer();
        return true;
      }
    }
    return false;
  } catch (error) {
    console.error("Error al refrescar el token:", error);
    return false;
  }
}
