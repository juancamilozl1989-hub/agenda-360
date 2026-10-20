"""
Utilidades de agenda: días de la semana e intervalos de tiempo.

Se usan en las reglas de las citas y en el cálculo de disponibilidad.
"""
import unicodedata
from datetime import date, datetime, time, timedelta

# Nombres de los días tal como se guardan en la tabla de horarios
DIAS_SEMANA = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]

# Cada cuántos minutos se ofrece un turno al calcular disponibilidad
INTERVALO_MINUTOS = 30


def _sin_tildes(texto: str) -> str:
    """'Miércoles' -> 'miercoles'."""
    normalizado = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


def normalizar_dia(texto: str) -> str | None:
    """
    Devuelve el nombre oficial del día ("Miércoles") a partir de lo que
    escriba el usuario ("miercoles", "MIÉRCOLES"...). None si no es un día.
    """
    buscado = _sin_tildes(texto)
    for dia in DIAS_SEMANA:
        if _sin_tildes(dia) == buscado:
            return dia
    return None


def dia_de_la_semana(fecha: date) -> str:
    """Nombre del día de la semana de una fecha (lunes = 0 en Python)."""
    return DIAS_SEMANA[fecha.weekday()]


def sumar_minutos(hora: time, minutos: int) -> time | None:
    """
    Suma minutos a una hora. Devuelve None si el resultado pasa de la
    medianoche, porque una cita no puede terminar al día siguiente.
    """
    base = datetime.combine(date.today(), hora)
    resultado = base + timedelta(minutes=minutos)
    if resultado.date() != base.date():
        return None
    return resultado.time()


def se_cruzan(inicio_a: time, fin_a: time, inicio_b: time, fin_b: time) -> bool:
    """True si los intervalos [inicio_a, fin_a) e [inicio_b, fin_b) se cruzan."""
    return inicio_a < fin_b and inicio_b < fin_a
