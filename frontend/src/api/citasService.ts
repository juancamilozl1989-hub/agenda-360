import axiosClient from "./axiosClient";
import type { Cita, CitaForm } from "./tipos";

export async function listarCitas(): Promise<Cita[]> {
  const { data } = await axiosClient.get<Cita[]>("/appointments/");
  return data;
}

export async function crearCita(form: CitaForm): Promise<Cita> {
  const { data } = await axiosClient.post<Cita>("/appointments/", {
    fecha: form.fecha,
    hora: form.hora,
    client_id: form.client_id,
    barber_id: form.barber_id,
    service_id: form.service_id,
  });
  return data;
}

export async function actualizarCita(form: CitaForm): Promise<Cita> {
  const { data } = await axiosClient.put<Cita>(`/appointments/${form.id}`, {
    fecha: form.fecha,
    hora: form.hora,
    estado: form.estado,
    client_id: form.client_id,
    barber_id: form.barber_id,
    service_id: form.service_id,
  });
  return data;
}

export async function eliminarCita(id: number): Promise<void> {
  await axiosClient.delete(`/appointments/${id}`);
}
