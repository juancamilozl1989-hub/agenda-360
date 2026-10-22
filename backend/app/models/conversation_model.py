# Tipos de datos SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String, Text

# Clase base
from app.core.base import Base


class Conversation(Base):
    """
    Estado de la conversación de un cliente con el bot de WhatsApp.

    Guarda en qué paso va cada número de teléfono y lo que ha
    elegido hasta el momento (servicio, barbero, fecha...).
    """

    __tablename__ = "conversations"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Número de WhatsApp con indicativo (por ejemplo 573001234567)
    telefono = Column(String(20), nullable=False, unique=True, index=True)

    # Paso actual del flujo: menu, nombre, servicio, barbero, fecha, hora...
    paso = Column(String(30), nullable=False, default="menu")

    # Datos elegidos hasta ahora, guardados como JSON
    datos = Column(Text, nullable=False, default="{}")

    # Último mensaje procesado (WhatsApp puede reenviar el mismo)
    ultimo_mensaje_id = Column(String(120), nullable=True)

    # Fecha y hora del último mensaje
    actualizado = Column(DateTime, nullable=True)
