import axiosClient from "./axiosClient";
import type { Barbero, BarberoForm } from "./tipos";

export async function listarBarberos(): Promise<Barbero[]> {
  const { data } = await axiosClient.get<Barbero[]>("/barbers/");
  return data;
}

export async function crearBarbero(
  form: BarberoForm,
  barbershopId: number
): Promise<Barbero> {
  const { data } = await axiosClient.post<Barbero>("/barbers/", {
    nombre: form.nombre,
    telefono: form.telefono,
    especialidad: form.especialidad,
    estado: form.estado,
    barbershop_id: barbershopId,
  });
  return data;
}

export async function actualizarBarbero(
  form: BarberoForm,
  barbershopId: number
): Promise<Barbero> {
  const { data } = await axiosClient.put<Barbero>(`/barbers/${form.id}`, {
    nombre: form.nombre,
    telefono: form.telefono,
    especialidad: form.especialidad,
    estado: form.estado,
    barbershop_id: barbershopId,
  });
  return data;
}

export async function eliminarBarbero(id: number): Promise<void> {
  await axiosClient.delete(`/barbers/${id}`);
}
