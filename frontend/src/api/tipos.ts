// Tipos que reflejan exactamente lo que responde la API de Agenda 360
// (ver backend/app/schemas). Mantenerlos en un solo lugar evita que cada
// pantalla defina su propia versión de los datos.

export type Estado = "Activo" | "Inactivo";

export interface BarberiaSimple {
  id: number;
  nombre: string;
}

export interface Barberia extends BarberiaSimple {
  direccion: string;
  telefono: string;
  email: string;
  estado: string;
}

export interface Cliente {
  id: number;
  nombre: string;
  telefono: string;
  email: string;
  estado: string;
  barbershop: BarberiaSimple;
}

export interface Barbero {
  id: number;
  nombre: string;
  telefono: string;
  especialidad: string;
  estado: string;
  barbershop: BarberiaSimple;
}

export interface BarberoSimple {
  id: number;
  nombre: string;
}

export interface Servicio {
  id: number;
  nombre: string;
  categoria: string;
  descripcion: string;
  precio: number;
  duracion: number;
  estado: string;
  // Los servicios son el catálogo de la barbería: cualquier barbero
  // activo puede atender cualquier servicio activo.
  barbershop: BarberiaSimple;
}

export type EstadoCita =
  | "Pendiente"
  | "Confirmada"
  | "Cancelada"
  | "Completada";

export interface Cita {
  id: number;
  fecha: string; // AAAA-MM-DD
  hora: string; // HH:MM:SS
  estado: EstadoCita;
  client: Cliente;
  barber: BarberoSimple;
  service: Servicio;
}

// ---------- Datos que se envían a la API ----------

export interface ClienteForm {
  id: number;
  nombre: string;
  telefono: string;
  email: string;
  estado: string;
}

export interface BarberoForm {
  id: number;
  nombre: string;
  especialidad: string;
  telefono: string;
  estado: string;
}

export interface ServicioForm {
  id: number;
  nombre: string;
  categoria: string;
  descripcion: string;
  duracion: number;
  precio: number;
  estado: string;
  // 0 = se usa la barbería principal al guardar
  barbershop_id: number;
}

export interface CitaForm {
  id: number;
  fecha: string;
  hora: string;
  estado: EstadoCita;
  client_id: number;
  barber_id: number;
  service_id: number;
}

// ---------- Horarios de atención de los barberos ----------

export interface Horario {
  id: number;
  dia_semana: string; // "Lunes" ... "Domingo"
  hora_inicio: string; // HH:MM:SS
  hora_fin: string; // HH:MM:SS
  barber: BarberoSimple;
}

export interface HorarioForm {
  id: number;
  dia_semana: string;
  hora_inicio: string; // HH:MM
  hora_fin: string; // HH:MM
  barber_id: number;
}

export const DIAS_SEMANA = [
  "Lunes",
  "Martes",
  "Miércoles",
  "Jueves",
  "Viernes",
  "Sábado",
  "Domingo",
];

// ---------- Disponibilidad (GET /availability/) ----------

export interface HoraDisponible {
  hora: string; // HH:MM:SS
  barberos: BarberoSimple[];
}

export interface Disponibilidad {
  fecha: string;
  dia_semana: string;
  servicio: { id: number; nombre: string; duracion: number; precio: number };
  disponibles: HoraDisponible[];
}
