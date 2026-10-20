# Fecha y hora
from datetime import date, datetime, time

# Excepciones de FastAPI
from fastapi import HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Modelos
from app.models.appointment_model import Appointment
from app.models.barber_model import Barber
from app.models.service_model import Service

# Repository
from app.repositories import appointment_repository

# Schemas
from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentStatus,
    AppointmentUpdate,
)

# Utilidades de agenda
from app.utils.agenda import (
    INTERVALO_MINUTOS,
    dia_de_la_semana,
    se_cruzan,
    sumar_minutos,
)


# ==========================================
# Hora actual
# ==========================================
def ahora() -> datetime:
    """
    Fecha y hora actual del servidor.

    Está en una función aparte para que las pruebas
    puedan simular la hora sin depender del reloj real.
    """

    return datetime.now()


# ==========================================
# Regla: la cita no puede quedar en el pasado
# ==========================================
def validar_fecha_y_hora(fecha: date, hora: time):
    """
    Rechaza citas en días anteriores a hoy y, si la cita
    es para hoy, en una hora que ya pasó.
    """

    momento_actual = ahora()

    if fecha < momento_actual.date():
        raise HTTPException(
            status_code=400,
            detail="No se pueden registrar citas en fechas pasadas."
        )

    # Antes solo se comparaba la fecha, por lo que se aceptaba
    # una cita para hoy a las 9:00 a. m. aunque ya fuera de noche.
    if datetime.combine(fecha, hora) < momento_actual:
        raise HTTPException(
            status_code=400,
            detail="No se pueden registrar citas en una hora que ya pasó."
        )


# ==========================================
# Regla: barbero y servicio deben estar activos
# ==========================================
def validar_activos(barbero: Barber, servicio: Service):
    """
    Un barbero inactivo no recibe citas y un servicio
    inactivo no se puede agendar.
    """

    if barbero.estado != "Activo":
        raise HTTPException(
            status_code=400,
            detail="El barbero no está activo y no puede recibir citas."
        )

    if servicio.estado != "Activo":
        raise HTTPException(
            status_code=400,
            detail="El servicio seleccionado no está activo."
        )


# ==========================================
# Regla: la cita debe caer dentro del horario del barbero
# ==========================================
def validar_horario_del_barbero(
    barbero: Barber,
    fecha: date,
    hora: time,
    duracion: int,
    db: Session
):
    """
    La cita completa (desde la hora de inicio hasta que termina
    el servicio) debe quedar dentro de alguno de los bloques de
    atención que el barbero tiene habilitados ese día.
    """

    dia = dia_de_la_semana(fecha)
    horarios = appointment_repository.obtener_horarios_del_dia(
        barbero.id,
        dia,
        db
    )

    # "los lunes", "los sábados", "los domingos"
    dias = dia.lower() if dia.lower().endswith("s") else dia.lower() + "s"

    if not horarios:
        raise HTTPException(
            status_code=400,
            detail=f"El barbero {barbero.nombre} no atiende los {dias}."
        )

    fin = sumar_minutos(hora, duracion)

    for horario in horarios:
        if fin is not None and horario.hora_inicio <= hora and fin <= horario.hora_fin:
            return

    bloques = ", ".join(
        f"{h.hora_inicio.strftime('%H:%M')} a {h.hora_fin.strftime('%H:%M')}"
        for h in horarios
    )
    raise HTTPException(
        status_code=400,
        detail=(
            f"La cita queda fuera del horario de {barbero.nombre}. "
            f"Los {dias} atiende de {bloques}."
        )
    )


# ==========================================
# Regla: la cita no puede cruzarse con otra del mismo barbero
# ==========================================
def validar_sin_cruces(
    barber_id: int,
    fecha: date,
    hora: time,
    duracion: int,
    db: Session,
    excluir_id: int | None = None
):
    """
    Compara la cita con las demás citas activas del barbero ese
    día teniendo en cuenta la DURACIÓN de cada servicio. Antes solo
    se rechazaba la misma hora exacta, de modo que una cita a las
    9:30 se aceptaba aunque otra de 50 minutos empezara a las 9:00.
    """

    fin = sumar_minutos(hora, duracion)

    citas = appointment_repository.obtener_citas_activas_del_barbero(
        barber_id,
        fecha,
        db,
        excluir_id
    )

    for otra in citas:
        fin_otra = sumar_minutos(otra.hora, otra.service.duracion)
        if fin is None or fin_otra is None or se_cruzan(hora, fin, otra.hora, fin_otra):
            raise HTTPException(
                status_code=400,
                detail=(
                    "El barbero ya tiene una cita programada que se cruza con ese "
                    f"horario ({otra.hora.strftime('%H:%M')} - {otra.service.nombre})."
                )
            )


# ==========================================
# Buscar cliente, barbero y servicio (404 si no existen)
# ==========================================
def _obtener_participantes(client_id: int, barber_id: int, service_id: int, db: Session):
    cliente = appointment_repository.obtener_cliente(client_id, db)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    barbero = appointment_repository.obtener_barbero(barber_id, db)
    if barbero is None:
        raise HTTPException(status_code=404, detail="Barbero no encontrado")

    servicio = appointment_repository.obtener_servicio(service_id, db)
    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    return cliente, barbero, servicio


# ==========================================
# Crear una cita
# ==========================================
def crear_cita(
    datos: AppointmentCreate,
    db: Session
):
    """
    Contiene la lógica de negocio para registrar una cita.

    Reglas, en este orden:
    1. La fecha y la hora no pueden haber pasado.
    2. Cliente, barbero y servicio deben existir (404).
    3. Barbero y servicio deben estar activos.
    4. La cita debe caer dentro del horario del barbero ese día.
    5. No puede cruzarse con otra cita activa del barbero.

    Cualquier barbero puede atender cualquier servicio: los
    servicios son el catálogo de la barbería.
    """

    # 1. No permitir citas en fechas u horas pasadas
    validar_fecha_y_hora(datos.fecha, datos.hora)

    # 2. Cliente, barbero y servicio deben existir
    _, barbero, servicio = _obtener_participantes(
        datos.client_id,
        datos.barber_id,
        datos.service_id,
        db
    )

    # 3. Barbero y servicio activos
    validar_activos(barbero, servicio)

    # 4. Dentro del horario habilitado del barbero
    validar_horario_del_barbero(
        barbero,
        datos.fecha,
        datos.hora,
        servicio.duracion,
        db
    )

    # 5. Sin cruces con otras citas del barbero
    validar_sin_cruces(
        barbero.id,
        datos.fecha,
        datos.hora,
        servicio.duracion,
        db
    )

    # Crear objeto
    cita = Appointment(
        fecha=datos.fecha,
        hora=datos.hora,
        client_id=datos.client_id,
        barber_id=datos.barber_id,
        service_id=datos.service_id
    )

    # Guardar mediante Repository
    return appointment_repository.guardar_cita(
        cita,
        db
    )


# ==========================================
# Actualizar una cita
# ==========================================
def actualizar_cita(
    appointment_id: int,
    datos: AppointmentUpdate,
    db: Session
):
    """
    Actualiza una cita aplicando las mismas reglas que al crearla,
    pero solo cuando tiene sentido:

    - La fecha/hora pasada solo se valida si la fecha o la hora
      cambian; así se puede marcar como "Completada" una cita de
      esta mañana aunque su hora ya haya pasado.
    - Si la cita queda "Cancelada" no se valida la agenda, porque
      deja de ocupar el horario.
    - El horario del barbero y los estados activos se validan si
      cambia la fecha, la hora, el barbero o el servicio.
    - Los cruces se validan siempre que la cita quede activa; así
      no se puede reactivar una cita cancelada si otra persona ya
      tomó ese horario (hallazgo H-01).
    """

    cita = appointment_repository.obtener_cita(appointment_id, db)

    if cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    cambia_momento = datos.fecha != cita.fecha or datos.hora != cita.hora
    cambia_agenda = (
        cambia_momento
        or datos.barber_id != cita.barber_id
        or datos.service_id != cita.service_id
    )

    if cambia_momento:
        validar_fecha_y_hora(datos.fecha, datos.hora)

    _, barbero, servicio = _obtener_participantes(
        datos.client_id,
        datos.barber_id,
        datos.service_id,
        db
    )

    if datos.estado != AppointmentStatus.CANCELADA:
        if cambia_agenda:
            validar_activos(barbero, servicio)
            validar_horario_del_barbero(
                barbero,
                datos.fecha,
                datos.hora,
                servicio.duracion,
                db
            )

        validar_sin_cruces(
            barbero.id,
            datos.fecha,
            datos.hora,
            servicio.duracion,
            db,
            excluir_id=appointment_id
        )

    cita.fecha = datos.fecha
    cita.hora = datos.hora
    cita.estado = datos.estado.value
    cita.client_id = datos.client_id
    cita.barber_id = datos.barber_id
    cita.service_id = datos.service_id

    db.commit()
    db.refresh(cita)

    return cita


# ==========================================
# Disponibilidad de la agenda
# ==========================================
def calcular_disponibilidad(
    fecha: date,
    service_id: int,
    db: Session,
    barber_id: int | None = None
):
    """
    Devuelve las horas en las que se puede agendar un servicio en una
    fecha. Es la base del bot de WhatsApp: el cliente elige entre las
    horas que devuelve esta función y la cita se crea con crear_cita,
    que vuelve a aplicar todas las reglas.

    - Si se indica barber_id, solo se revisa ese barbero.
    - Si no, se revisan todos los barberos activos y, para cada hora,
      se indica qué barberos están libres ("me da igual con quién").

    Las horas se ofrecen cada INTERVALO_MINUTOS desde el inicio de
    cada bloque de atención, siempre que el servicio completo quepa
    en el bloque, no se cruce con otra cita y no haya pasado.
    """

    momento_actual = ahora()

    if fecha < momento_actual.date():
        raise HTTPException(
            status_code=400,
            detail="No se puede consultar disponibilidad en fechas pasadas."
        )

    servicio = appointment_repository.obtener_servicio(service_id, db)
    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    if servicio.estado != "Activo":
        raise HTTPException(
            status_code=400,
            detail="El servicio seleccionado no está activo."
        )

    if barber_id is not None:
        barbero = appointment_repository.obtener_barbero(barber_id, db)
        if barbero is None:
            raise HTTPException(status_code=404, detail="Barbero no encontrado")
        barberos = [barbero] if barbero.estado == "Activo" else []
    else:
        barberos = appointment_repository.obtener_barberos_activos(db)

    dia = dia_de_la_semana(fecha)
    duracion = servicio.duracion

    # hora -> lista de barberos libres a esa hora
    disponibles: dict[time, list[Barber]] = {}

    for barbero in barberos:
        horarios = appointment_repository.obtener_horarios_del_dia(barbero.id, dia, db)
        citas = appointment_repository.obtener_citas_activas_del_barbero(
            barbero.id, fecha, db
        )
        ocupados = [
            (c.hora, sumar_minutos(c.hora, c.service.duracion) or time.max)
            for c in citas
        ]

        for horario in horarios:
            inicio = horario.hora_inicio

            while True:
                fin = sumar_minutos(inicio, duracion)
                if fin is None or fin > horario.hora_fin:
                    break

                ya_paso = datetime.combine(fecha, inicio) < momento_actual
                cruza = any(se_cruzan(inicio, fin, a, b) for a, b in ocupados)

                if not ya_paso and not cruza:
                    disponibles.setdefault(inicio, [])
                    if barbero not in disponibles[inicio]:
                        disponibles[inicio].append(barbero)

                siguiente = sumar_minutos(inicio, INTERVALO_MINUTOS)
                if siguiente is None:
                    break
                inicio = siguiente

    return {
        "fecha": fecha,
        "dia_semana": dia,
        "servicio": servicio,
        "disponibles": [
            {"hora": hora, "barberos": disponibles[hora]}
            for hora in sorted(disponibles)
        ],
    }


# ==========================================
# Obtener todas las citas
# ==========================================
def obtener_citas(
    db: Session
):
    """
    Obtener todas las citas.
    """

    return db.query(Appointment).all()


# ==========================================
# Obtener una cita por ID
# ==========================================
def obtener_cita(
    appointment_id: int,
    db: Session
):
    """
    Obtener una cita específica.
    """

    cita = appointment_repository.obtener_cita(appointment_id, db)

    if cita is None:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    return cita
