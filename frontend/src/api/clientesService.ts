import axiosClient from "./axiosClient";
import type { Cliente, ClienteForm } from "./tipos";

export async function listarClientes(): Promise<Cliente[]> {
  const { data } = await axiosClient.get<Cliente[]>("/clients/");
  return data;
}

export async function crearCliente(
  form: ClienteForm,
  barbershopId: number
): Promise<Cliente> {
  const { data } = await axiosClient.post<Cliente>("/clients/", {
    nombre: form.nombre,
    telefono: form.telefono,
    email: form.email,
    estado: form.estado,
    barbershop_id: barbershopId,
  });
  return data;
}

export async function actualizarCliente(
  form: ClienteForm,
  barbershopId: number
): Promise<Cliente> {
  const { data } = await axiosClient.put<Cliente>(`/clients/${form.id}`, {
    nombre: form.nombre,
    telefono: form.telefono,
    email: form.email,
    estado: form.estado,
    barbershop_id: barbershopId,
  });
  return data;
}

export async function eliminarCliente(id: number): Promise<void> {
  await axiosClient.delete(`/clients/${id}`);
}
