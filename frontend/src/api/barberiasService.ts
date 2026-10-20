import axiosClient from "./axiosClient";
import type { Barberia } from "./tipos";

export async function listarBarberias(): Promise<Barberia[]> {
  const { data } = await axiosClient.get<Barberia[]>("/barbershops/");
  return data;
}

// Agenda 360 se está usando en esta fase para una sola barbería.
// Para no obligar al administrador a crearla a mano por Swagger,
// se toma la primera existente o, si la base está vacía, se crea una
// por defecto la primera vez que se entra al sistema.
let barberiaEnCache: Barberia | null = null;

export async function obtenerBarberiaPrincipal(): Promise<Barberia> {
  if (barberiaEnCache) return barberiaEnCache;

  const barberias = await listarBarberias();

  if (barberias.length > 0) {
    barberiaEnCache = barberias[0];
    return barberiaEnCache;
  }

  const { data } = await axiosClient.post<Barberia>("/barbershops/", {
    nombre: "Agenda 360 Barbería",
    direccion: "Por definir",
    telefono: "0000000000",
    email: "contacto@agenda360.com",
  });

  barberiaEnCache = data;
  return data;
}
