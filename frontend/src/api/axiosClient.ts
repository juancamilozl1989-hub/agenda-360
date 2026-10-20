import axios from "axios";

// Cliente HTTP centralizado para consumir el backend de Agenda 360.
// Toda petición a la API debe pasar por aquí para heredar
// automáticamente la URL base y el token de autenticación.
const axiosClient = axios.create({
  // "/api" pasa por el proxy de Vite (vite.config.ts) hacia FastAPI
  baseURL: import.meta.env.VITE_API_URL || "/api",
});

// ==========================================================
// Interceptor de petición
// ==========================================================
// Adjunta el token JWT guardado (si existe) a cada request,
// para no tener que hacerlo manualmente en cada llamada.
axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("agenda360_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// ==========================================================
// Interceptor de respuesta
// ==========================================================
// Si el backend responde 401 (token vencido o inválido),
// se limpia la sesión local y se redirige al login.
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("agenda360_token");
      localStorage.removeItem("agenda360_user");

      if (window.location.pathname !== "/") {
        window.location.href = "/";
      }
    }

    return Promise.reject(error);
  }
);

export default axiosClient;
