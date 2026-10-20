"""
Sincronización mínima del esquema de la base de datos.

Base.metadata.create_all() crea las tablas que no existen, pero NO agrega
columnas nuevas a tablas que ya existían. Si un modelo gana una columna
(por ejemplo "estado" en clientes) después de haber creado la tabla, las
consultas fallan con "column ... does not exist".

sincronizar_columnas() revisa cada tabla de los modelos y agrega, con
ALTER TABLE, las columnas que falten. Solo AGREGA columnas.

migrar_servicios_a_barberia() es un cambio puntual de diseño: los
servicios pasaron de pertenecer a un barbero (barber_id) a pertenecer a
la barbería (barbershop_id). Copia la barbería de cada barbero a sus
servicios y luego elimina la columna barber_id, que ya no se usa.
"""
import logging

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from app.core.base import Base

logger = logging.getLogger("agenda360")


def _valor_sql(valor) -> str:
    """Convierte un valor por defecto de Python en un literal SQL."""
    if isinstance(valor, bool):
        return "TRUE" if valor else "FALSE"
    if isinstance(valor, (int, float)):
        return str(valor)
    return "'" + str(valor).replace("'", "''") + "'"


def migrar_servicios_a_barberia(engine: Engine) -> bool:
    """
    Pasa los servicios existentes de barber_id a barbershop_id.
    Se ejecuta solo si la tabla services todavía tiene barber_id.
    Debe correr DESPUÉS de sincronizar_columnas, que crea barbershop_id.
    Devuelve True si hizo la migración.
    """

    inspector = inspect(engine)

    if "services" not in inspector.get_table_names():
        return False

    columnas = {c["name"] for c in inspector.get_columns("services")}

    if "barber_id" not in columnas:
        return False

    with engine.begin() as conexion:
        # 1. Cada servicio toma la barbería de su antiguo barbero
        conexion.execute(text(
            "UPDATE services SET barbershop_id = ("
            " SELECT barbers.barbershop_id FROM barbers"
            " WHERE barbers.id = services.barber_id"
            ") WHERE barbershop_id IS NULL"
        ))

        # 2. Si alguno quedó sin barbería (barbero borrado), se le asigna la primera
        conexion.execute(text(
            "UPDATE services SET barbershop_id = ("
            " SELECT MIN(id) FROM barbershops"
            ") WHERE barbershop_id IS NULL"
        ))

        # 3. Se elimina la columna antigua (en PostgreSQL también su llave foránea)
        conexion.execute(text("ALTER TABLE services DROP COLUMN barber_id"))

        # 4. En PostgreSQL se exige que todo servicio tenga barbería
        #    y se crea la llave foránea hacia barbershops
        if engine.dialect.name == "postgresql":
            conexion.execute(text(
                "ALTER TABLE services ALTER COLUMN barbershop_id SET NOT NULL"
            ))
            conexion.execute(text(
                "ALTER TABLE services ADD CONSTRAINT services_barbershop_id_fkey "
                "FOREIGN KEY (barbershop_id) REFERENCES barbershops (id)"
            ))

    logger.warning("Servicios migrados: ahora pertenecen a la barbería (barber_id eliminado).")
    return True


def sincronizar_columnas(engine: Engine) -> list[str]:
    """
    Agrega a la base de datos las columnas que existen en los modelos
    pero no en las tablas. Devuelve la lista de columnas agregadas.
    """
    inspector = inspect(engine)
    tablas_existentes = set(inspector.get_table_names())
    agregadas: list[str] = []

    with engine.begin() as conexion:
        for tabla in Base.metadata.sorted_tables:
            if tabla.name not in tablas_existentes:
                continue  # create_all ya se encarga de las tablas nuevas

            columnas_bd = {c["name"] for c in inspector.get_columns(tabla.name)}

            for columna in tabla.columns:
                if columna.name in columnas_bd:
                    continue

                tipo = columna.type.compile(dialect=engine.dialect)
                sentencia = f'ALTER TABLE "{tabla.name}" ADD COLUMN "{columna.name}" {tipo}'

                # Si el modelo define un valor por defecto simple, se usa para
                # rellenar las filas existentes y así poder exigir NOT NULL.
                defecto = columna.default
                if defecto is not None and getattr(defecto, "is_scalar", False):
                    sentencia += f" DEFAULT {_valor_sql(defecto.arg)}"
                    if not columna.nullable:
                        sentencia += " NOT NULL"

                conexion.execute(text(sentencia))
                agregadas.append(f"{tabla.name}.{columna.name}")
                logger.warning("Columna agregada a la base de datos: %s.%s", tabla.name, columna.name)

    return agregadas
