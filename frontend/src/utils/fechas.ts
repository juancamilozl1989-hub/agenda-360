// Utilidades de fechas para la agenda y el dashboard.
// Las fechas de la API vienen como "AAAA-MM-DD"; se trabajan siempre como
// texto en hora local para evitar el desfase de zona horaria que produce
// `new Date("2026-10-17")` (que se interpreta en UTC).

const dos = (n: number) => String(n).padStart(2, "0");

export const aTexto = (d: Date): string =>
  `${d.getFullYear()}-${dos(d.getMonth() + 1)}-${dos(d.getDate())}`;

export const hoyTexto = (): string => aTexto(new Date());

export const desdeTexto = (f: string): Date => {
  const [y, m, d] = f.split("-").map(Number);
  return new Date(y, m - 1, d);
};

export const sumarDias = (f: string, dias: number): string => {
  const d = desdeTexto(f);
  d.setDate(d.getDate() + dias);
  return aTexto(d);
};

// Lunes de la semana a la que pertenece la fecha
export const inicioSemana = (f: string): string => {
  const d = desdeTexto(f);
  const dia = (d.getDay() + 6) % 7; // lunes = 0
  d.setDate(d.getDate() - dia);
  return aTexto(d);
};

export const mismoMes = (a: string, b: string): boolean =>
  a.slice(0, 7) === b.slice(0, 7);

export const DIAS_CORTOS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];
