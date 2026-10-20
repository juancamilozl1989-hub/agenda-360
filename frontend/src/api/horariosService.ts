import axiosClient from "./axiosClient";
import type { Horario, HorarioForm } from "./tipos";

const cuerpo = (f: HorarioForm) => ({
  dia_semana: f.dia_semana,
  hora_inicio: f.hora_inicio,
  hora_fin: f.hora_fin,
  barber_id: f.barber_id,
});

export async function listarHorarios(): Promise<Horario[]> {
  const { data } = await axiosClient.get<Horario[]>("/schedules/");
  return data;
}

export async function crearHorario(form: HorarioForm): Promise<Horario> {
  const { data } = await axiosClient.post<Horario>("/schedules/", cuerpo(form));
  return data;
}

export async function actualizarHorario(form: HorarioForm): Promise<Horario> {
  const { data } = await axiosClient.put<Horario>(
    `/schedules/${form.id}`,
    cuerpo(form)
  );
  return data;
}

export async function eliminarHorario(id: number): Promise<void> {
  await axiosClient.delete(`/schedules/${id}`);
}
