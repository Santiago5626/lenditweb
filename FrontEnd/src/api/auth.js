export async function login(nombre, password) {
  try {
    const response = await fetch("http://127.0.0.1:8000/usuario/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ nombre, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Error en el login");
    }

    return data; // aquí puedes devolver el token u otros datos
  } catch (error) {
    throw error;
  }
}
