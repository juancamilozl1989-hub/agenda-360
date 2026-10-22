"""
Motor de conversación del bot de WhatsApp.

El bot guía al cliente con menús numerados:
  1. Agendar una cita (servicio -> barbero -> fecha -> hora -> confirmar)
  2. Ver sus próximas citas
  3. Cancelar una cita

No tiene reglas propias: consulta la disponibilidad y registra la cita
con las mismas funciones que usa el panel (appointment_service), así que
el horario del barbero, la duración del servicio y los cruces se validan
igual en ambos canales.

procesar_mensaje() recibe el texto del cliente y devuelve la lista de
respuestas; quien lo llama se encarga de enviarlas por WhatsApp.
"""
import json
import re
from datetime import date, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.appointment_model import Appointment
from app.models.barber_model import Barber
from app.models.barbershop_model import Barbershop
from app.models.client_model import Client
from app.models.conversation_model import Conversation
from app.models.service_model import Service
from app.schemas.appointment_schema import AppointmentCreate
from app.services import appointment_service
from app.utils.agenda import DIAS_SEMANA

# Cuántas horas se muestran como máximo en un mensaje
MAX_HORAS = 12

# Cuántos días con espacio se ofrecen y hasta dónde se buscan
DIAS_A_OFRECER = 7
DIAS_A_BUSCAR = 14

# Después de este tiempo sin mensajes la conversación vuelve a empezar
MINUTOS_INACTIVIDAD = 60

# Palabras que llevan al menú principal en cualquier momento
PALABRAS_MENU = {"hola", "menu", "menú", "inicio", "buenas", "buenos dias", "buenos días",
                 "buenas tardes", "buenas noches", "salir", "cancelar todo"}

ESTADOS_ACTIVOS = ("Pendiente", "Confirmada")


# ==========================================================
# Utilidades de formato
# ==========================================================
def _digitos(texto: str) -> str:
    return re.sub(r"\D", "", texto or "")


def telefono_local(telefono_whatsapp: str) -> str:
    """'573001234567' -> '3001234567' (los últimos 10 dígitos)."""
    d = _digitos(telefono_whatsapp)
    return d[-10:] if len(d) > 10 else d


def _moneda(valor: float) -> str:
    return "$ " + f"{int(valor):,}".replace(",", ".")


def _fecha_corta(f: date) -> str:
    """date(2026, 10, 26) -> 'lunes 26/10'."""
    return f"{DIAS_SEMANA[f.weekday()].lower()} {f.day:02d}/{f.month:02d}"


def _hora(h) -> str:
    return h.strftime("%H:%M")


# ==========================================================
# Acceso a datos
# ==========================================================
def buscar_cliente(telefono_whatsapp: str, db: Session) -> Client | None:
    """
    Busca al cliente por su número. En el panel los teléfonos se guardan
    sin indicativo (3001234567) y WhatsApp los envía con él (573001234567),
    por eso se comparan los últimos 10 dígitos.
    """
    local = telefono_local(telefono_whatsapp)
    if len(local) < 7:
        return None
    for cliente in db.query(Client).all():
        if _digitos(cliente.telefono).endswith(local):
            return cliente
    return None


def _barberia_principal(db: Session) -> Barbershop | None:
    return db.query(Barbershop).order_by(Barbershop.id).first()


def _conversacion(telefono: str, db: Session) -> Conversation:
    conv = db.query(Conversation).filter(Conversation.telefono == telefono).first()
    if conv is None:
        conv = Conversation(telefono=telefono, paso="menu", datos="{}")
        db.add(conv)
        db.commit()
        db.refresh(conv)
    return conv


def _guardar(conv: Conversation, paso: str, datos: dict, db: Session):
    conv.paso = paso
    conv.datos = json.dumps(datos)
    conv.actualizado = appointment_service.ahora()
    db.commit()


def _proximas_citas(cliente: Client, db: Session) -> list[Appointment]:
    """Citas pendientes o confirmadas que todavía no han pasado."""
    momento = appointment_service.ahora()
    citas = db.query(Appointment).filter(
        Appointment.client_id == cliente.id,
        Appointment.estado.in_(ESTADOS_ACTIVOS),
        Appointment.fecha >= momento.date(),
    ).all()
    citas = [c for c in citas if datetime.combine(c.fecha, c.hora) >= momento]
    return sorted(citas, key=lambda c: (c.fecha, c.hora))


def _visitas_completadas(cliente: Client, db: Session) -> int:
    return db.query(Appointment).filter(
        Appointment.client_id == cliente.id,
        Appointment.estado == "Completada",
    ).count()


# ==========================================================
# Mensajes de cada paso
# ==========================================================
def _texto_menu(db: Session, nombre: str | None = None) -> str:
    barberia = _barberia_principal(db)
    nombre_barberia = barberia.nombre if barberia else "Agenda 360"
    saludo = f"¡Hola, {nombre}! 👋" if nombre else "¡Hola! 👋"
    return (
        f"{saludo} Soy el asistente de citas de *{nombre_barberia}*.\n"
        "¿Qué quieres hacer?\n\n"
        "1. Agendar una cita\n"
        "2. Ver mis próximas citas\n"
        "3. Cancelar una cita\n\n"
        "Responde con el número de la opción. Escribe *menú* en cualquier momento para volver aquí."
    )


def _pedir_servicio(conv, datos, db) -> list[str]:
    servicios = db.query(Service).filter(Service.estado == "Activo").order_by(Service.nombre).all()
    if not servicios:
        _guardar(conv, "menu", {}, db)
        return ["Por ahora no hay servicios disponibles para agendar. Intenta más tarde, por favor."]

    datos["opciones"] = [s.id for s in servicios]
    _guardar(conv, "servicio", datos, db)
    lineas = [f"{i}. {s.nombre} · {s.duracion} min · {_moneda(s.precio)}"
              for i, s in enumerate(servicios, start=1)]
    return ["¿Qué servicio quieres?\n\n" + "\n".join(lineas)]


def _pedir_barbero(conv, datos, db) -> list[str]:
    barberos = db.query(Barber).filter(Barber.estado == "Activo").order_by(Barber.nombre).all()
    if not barberos:
        _guardar(conv, "menu", {}, db)
        return ["Por ahora no hay barberos disponibles. Intenta más tarde, por favor."]

    # La opción 1 es "cualquier barbero" (se guarda como 0)
    datos["opciones"] = [0] + [b.id for b in barberos]
    _guardar(conv, "barbero", datos, db)
    lineas = ["1. Cualquier barbero disponible"] + [
        f"{i}. {b.nombre}" for i, b in enumerate(barberos, start=2)
    ]
    return ["¿Con qué barbero quieres tu cita?\n\n" + "\n".join(lineas)]


def _horas_libres(fecha: date, datos: dict, db) -> list[dict]:
    """Horas libres de un día para el servicio y el barbero elegidos."""
    try:
        disponibilidad = appointment_service.calcular_disponibilidad(
            fecha, datos["service_id"], db, datos.get("barber_id") or None
        )
    except HTTPException:
        return []
    return disponibilidad["disponibles"]


def _pedir_fecha(conv, datos, db, aviso: str | None = None) -> list[str]:
    """
    Ofrece solo los días que tienen al menos una hora libre para el
    servicio y el barbero elegidos (se revisan las próximas dos semanas).
    """
    hoy = appointment_service.ahora().date()
    dias = []
    for i in range(DIAS_A_BUSCAR):
        fecha = hoy + timedelta(days=i)
        libres = len(_horas_libres(fecha, datos, db))
        if libres:
            dias.append((fecha, libres))
        if len(dias) == DIAS_A_OFRECER:
            break

    if not dias:
        _guardar(conv, "menu", {}, db)
        return [
            f"😕 No hay horas libres en los próximos {DIAS_A_BUSCAR} días con esa elección. "
            "Escribe *menú* para intentarlo con otro barbero o servicio."
        ]

    datos["opciones"] = [f.isoformat() for f, _ in dias]
    _guardar(conv, "fecha", datos, db)

    lineas = []
    for i, (f, libres) in enumerate(dias, start=1):
        if f == hoy:
            prefijo = "Hoy, "
        elif f == hoy + timedelta(days=1):
            prefijo = "Mañana, "
        else:
            prefijo = ""
        lineas.append(f"{i}. {prefijo}{_fecha_corta(f)} ({libres} {'hora libre' if libres == 1 else 'horas libres'})")

    texto = "¿Para qué día? Te muestro solo los días con espacio:\n\n" + "\n".join(lineas)
    return [f"{aviso}\n\n{texto}" if aviso else texto]


def _pedir_hora(conv, datos, db, pagina: int = 0) -> list[str]:
    """Consulta la disponibilidad real y ofrece las horas libres por páginas."""
    fecha = date.fromisoformat(datos["fecha"])
    horas = _horas_libres(fecha, datos, db)

    if not horas:
        return _pedir_fecha(
            conv, datos, db,
            aviso=f"😕 Ya no quedan horas libres el {_fecha_corta(fecha)}. Elige otro día, por favor.",
        )

    inicio = pagina * MAX_HORAS
    if inicio >= len(horas):
        inicio, pagina = 0, 0
    mostradas = horas[inicio:inicio + MAX_HORAS]
    hay_mas = inicio + MAX_HORAS < len(horas)

    # Para cada hora se guarda el barbero que la atendería (el primero libre)
    datos["opciones"] = [[_hora(h["hora"]), h["barberos"][0].id] for h in mostradas]
    if hay_mas:
        datos["opciones"].append("mas")
    datos["pagina"] = pagina
    _guardar(conv, "hora", datos, db)

    lineas = [f"{i}. {_hora(h['hora'])}" for i, h in enumerate(mostradas, start=1)]
    if hay_mas:
        lineas.append(f"{len(mostradas) + 1}. Ver más horas ➡️")
    texto = f"Estas son las horas libres del {_fecha_corta(fecha)}:\n\n" + "\n".join(lineas)
    texto += "\n\nResponde *0* para elegir otro día."
    return [texto]


def _pedir_confirmacion(conv, datos, db) -> list[str]:
    servicio = db.get(Service, datos["service_id"])
    barbero = db.get(Barber, datos["barber_asignado"])
    fecha = date.fromisoformat(datos["fecha"])
    _guardar(conv, "confirmar", datos, db)
    return [
        "Confirma tu cita, por favor:\n\n"
        f"✂️ Servicio: {servicio.nombre} ({_moneda(servicio.precio)})\n"
        f"💈 Barbero: {barbero.nombre}\n"
        f"📅 Día: {_fecha_corta(fecha)}\n"
        f"🕒 Hora: {datos['hora']}\n\n"
        "1. Confirmar\n"
        "2. No agendar"
    ]


def _mis_citas(cliente: Client | None, db) -> str:
    if cliente is None:
        return "Todavía no tienes citas registradas con este número."

    citas = _proximas_citas(cliente, db)
    visitas = _visitas_completadas(cliente, db)

    if not citas:
        texto = "No tienes citas próximas."
    else:
        lineas = [
            f"• {_fecha_corta(c.fecha)} a las {_hora(c.hora)}: {c.service.nombre} "
            f"con {c.barber.nombre} ({c.estado})"
            for c in citas
        ]
        texto = "Tus próximas citas:\n\n" + "\n".join(lineas)

    if visitas:
        texto += f"\n\n⭐ Llevas {visitas} {'visita' if visitas == 1 else 'visitas'} con nosotros. ¡Gracias por volver!"
    return texto


def _pedir_cita_a_cancelar(conv, cliente, db) -> list[str]:
    citas = _proximas_citas(cliente, db) if cliente else []
    if not citas:
        _guardar(conv, "menu", {}, db)
        return ["No tienes citas próximas para cancelar."]

    _guardar(conv, "cancelar", {"opciones": [c.id for c in citas]}, db)
    lineas = [
        f"{i}. {_fecha_corta(c.fecha)} a las {_hora(c.hora)}: {c.service.nombre} con {c.barber.nombre}"
        for i, c in enumerate(citas, start=1)
    ]
    return ["¿Cuál cita quieres cancelar?\n\n" + "\n".join(lineas) + "\n\nResponde *0* para no cancelar ninguna."]


# ==========================================================
# Punto de entrada
# ==========================================================
def _elegir(texto: str, opciones: list):
    """Devuelve la opción elegida por número (1, 2, 3...) o None."""
    if not texto.isdigit():
        return None
    n = int(texto)
    if 1 <= n <= len(opciones):
        return opciones[n - 1]
    return None


def procesar_mensaje(telefono: str, texto: str, db: Session,
                     nombre_perfil: str | None = None) -> list[str]:
    """
    Procesa un mensaje del cliente y devuelve las respuestas del bot.
    """
    conv = _conversacion(telefono, db)
    datos = json.loads(conv.datos or "{}")
    entrada = (texto or "").strip()
    entrada_min = entrada.lower()
    cliente = buscar_cliente(telefono, db)
    nombre = cliente.nombre.split()[0] if cliente else (nombre_perfil or None)

    # Si pasó mucho tiempo desde el último mensaje, se empieza de nuevo
    if conv.actualizado and conv.paso != "menu":
        inactivo = appointment_service.ahora() - conv.actualizado
        if inactivo > timedelta(minutes=MINUTOS_INACTIVIDAD):
            conv.paso, datos = "menu", {}

    # Palabras para volver al menú en cualquier momento
    if entrada_min in PALABRAS_MENU or not entrada:
        _guardar(conv, "menu", {}, db)
        return [_texto_menu(db, nombre)]

    paso = conv.paso
    opciones = datos.get("opciones", [])

    # ---------- Menú principal ----------
    if paso == "menu":
        if entrada == "1":
            if cliente is None:
                _guardar(conv, "nombre", {}, db)
                return ["Para agendarte necesito tu nombre y apellido, por favor:"]
            return _pedir_servicio(conv, {}, db)
        if entrada == "2":
            return [_mis_citas(cliente, db)]
        if entrada == "3":
            return _pedir_cita_a_cancelar(conv, cliente, db)
        return [_texto_menu(db, nombre)]

    # ---------- Registro del cliente nuevo ----------
    if paso == "nombre":
        if len(entrada) < 3 or entrada.isdigit():
            return ["Escríbeme tu nombre y apellido, por favor."]
        barberia = _barberia_principal(db)
        if barberia is None:
            _guardar(conv, "menu", {}, db)
            return ["La barbería todavía no está configurada. Intenta más tarde, por favor."]
        cliente = Client(
            nombre=entrada.title(),
            telefono=telefono_local(telefono),
            email="",
            estado="Activo",
            barbershop_id=barberia.id,
        )
        db.add(cliente)
        db.commit()
        respuestas = [f"¡Mucho gusto, {cliente.nombre.split()[0]}! Ya quedaste registrado."]
        return respuestas + _pedir_servicio(conv, {}, db)

    # ---------- Agendar ----------
    if paso == "servicio":
        elegido = _elegir(entrada, opciones)
        if elegido is None:
            return ["Responde con el número del servicio, por favor."]
        return _pedir_barbero(conv, {"service_id": elegido}, db)

    if paso == "barbero":
        elegido = _elegir(entrada, opciones)
        if elegido is None:
            return ["Responde con el número del barbero, por favor."]
        datos["barber_id"] = elegido  # 0 = cualquier barbero
        return _pedir_fecha(conv, datos, db)

    if paso == "fecha":
        elegido = _elegir(entrada, opciones)
        if elegido is None:
            return ["Responde con el número del día, por favor."]
        datos["fecha"] = elegido
        return _pedir_hora(conv, datos, db)

    if paso == "hora":
        if entrada == "0":
            return _pedir_fecha(conv, datos, db)
        elegido = _elegir(entrada, opciones)
        if elegido is None:
            return ["Responde con el número de la hora, o *0* para elegir otro día."]
        if elegido == "mas":
            return _pedir_hora(conv, datos, db, datos.get("pagina", 0) + 1)
        datos["hora"], datos["barber_asignado"] = elegido
        return _pedir_confirmacion(conv, datos, db)

    if paso == "confirmar":
        if entrada == "2":
            _guardar(conv, "menu", {}, db)
            return ["Listo, no agendé nada. Escribe *menú* cuando quieras volver a empezar."]
        if entrada != "1":
            return ["Responde *1* para confirmar o *2* para no agendar."]
        try:
            cita = appointment_service.crear_cita(
                AppointmentCreate(
                    fecha=datos["fecha"],
                    hora=datos["hora"],
                    client_id=cliente.id,
                    barber_id=datos["barber_asignado"],
                    service_id=datos["service_id"],
                ),
                db,
            )
        except HTTPException as error:
            # Por ejemplo, alguien tomó esa hora mientras el cliente confirmaba
            return [f"⚠️ {error.detail}"] + _pedir_hora(conv, datos, db)

        _guardar(conv, "menu", {}, db)
        visitas = _visitas_completadas(cliente, db)
        mensaje = (
            "✅ ¡Listo! Tu cita quedó agendada:\n\n"
            f"{cita.service.nombre} con {cita.barber.nombre}\n"
            f"{_fecha_corta(cita.fecha)} a las {_hora(cita.hora)}\n\n"
            "Si necesitas cancelarla, escribe *menú* y elige la opción 3."
        )
        if visitas:
            mensaje += f"\n\n⭐ Será tu visita número {visitas + 1} con nosotros. ¡Gracias por la confianza!"
        return [mensaje]

    # ---------- Cancelar ----------
    if paso == "cancelar":
        if entrada == "0":
            _guardar(conv, "menu", {}, db)
            return ["Listo, no cancelé ninguna cita."]
        elegido = _elegir(entrada, opciones)
        if elegido is None:
            return ["Responde con el número de la cita, o *0* para no cancelar ninguna."]
        cita = db.get(Appointment, elegido)
        if cita is None or cliente is None or cita.client_id != cliente.id:
            _guardar(conv, "menu", {}, db)
            return ["No encontré esa cita. Escribe *menú* para volver a empezar."]
        cita.estado = "Cancelada"
        _guardar(conv, "menu", {}, db)
        return [
            f"Tu cita del {_fecha_corta(cita.fecha)} a las {_hora(cita.hora)} quedó cancelada. "
            "Si quieres, puedes agendar otra escribiendo *menú*."
        ]

    # Paso desconocido: se vuelve al menú
    _guardar(conv, "menu", {}, db)
    return [_texto_menu(db, nombre)]
