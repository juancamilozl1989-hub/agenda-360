import axios from "axios";

// Convierte cualquier error de Axios en un texto legible para el usuario.
// FastAPI devuelve los errores de negocio en `detail` (texto) y los de
// validación en `detail` (lista de objetos con `msg`).
export function mensajeError(
  error: unknown,
  porDefecto = "Ocurrió un error inesperado."
): string {
  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return "No se pudo conectar con el servidor. Verifica que el backend esté en ejecución.";
    }

    const detail = error.response.data?.detail;

    if (typeof detail === "string") return detail;

    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((d: { msg?: string }) => d.msg)
        .filter(Boolean)
        .join(". ");
    }
  }

  return porDefecto;
}
