const API_BASE_URL = "http://localhost:8000";

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
    }

    return data;
  } catch (error) {
    console.error("Error en login:", error);
    throw error;
  }
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "/login";
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
