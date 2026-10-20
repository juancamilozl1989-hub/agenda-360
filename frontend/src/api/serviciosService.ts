import axiosClient from "./axiosClient";
import { obtenerBarberiaPrincipal } from "./barberiasService";
import type { Servicio, ServicioForm } from "./tipos";

// El cuerpo es idéntico para crear y actualizar, así que se arma una sola vez.
// El servicio pertenece a la barbería; si el formulario no trae una,
// se usa la barbería principal.
const cuerpo = async (f: ServicioForm) => ({
  nombre: f.nombre,
  categoria: f.categoria,
  descripcion: f.descripcion,
  precio: f.precio,
  duracion: f.duracion,
  estado: f.estado,
  barbershop_id: f.barbershop_id || (await obtenerBarberiaPrincipal()).id,
});

export async function listarServicios(): Promise<Servicio[]> {
  const { data } = await axiosClient.get<Servicio[]>("/services/");
  return data;
}

export async function crearServicio(form: ServicioForm): Promise<Servicio> {
  const { data } = await axiosClient.post<Servicio>(
    "/services/",
    await cuerpo(form)
  );
  return data;
}

export async function actualizarServicio(
  form: ServicioForm
): Promise<Servicio> {
  const { data } = await axiosClient.put<Servicio>(
    `/services/${form.id}`,
    await cuerpo(form)
  );
  return data;
}

export async function eliminarServicio(id: number): Promise<void> {
  await axiosClient.delete(`/services/${id}`);
}
