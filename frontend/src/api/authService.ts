import axiosClient from "./axiosClient";

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// ==========================================================
// Iniciar sesión
// ==========================================================
// El backend usa OAuth2PasswordRequestForm, por lo que espera
// los datos como "application/x-www-form-urlencoded" y no como JSON.
export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const response = await axiosClient.post<LoginResponse>(
    "/users/login",
    body
  );

  return response.data;
}

// ==========================================================
// Registrar un nuevo usuario
// ==========================================================
export interface RegisterPayload {
  nombre: string;
  email: string;
  password: string;
}

export async function registrarUsuario(datos: RegisterPayload) {
  const response = await axiosClient.post("/users/", datos);
  return response.data;
}
