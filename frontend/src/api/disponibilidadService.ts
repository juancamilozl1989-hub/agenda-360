import axiosClient from "./axiosClient";
import type { Disponibilidad } from "./tipos";

// Horas libres para un servicio en una fecha. Si no se indica barbero,
// cada hora trae la lista de barberos libres en ese momento.
// Es la misma consulta que usará el bot de WhatsApp.
export async function consultarDisponibilidad(
  fecha: string,
  serviceId: number,
  barberId?: number
): Promise<Disponibilidad> {
  const { data } = await axiosClient.get<Disponibilidad>("/availability/", {
    params: {
      fecha,
      service_id: serviceId,
      ...(barberId ? { barber_id: barberId } : {}),
    },
  });
  return data;
}
