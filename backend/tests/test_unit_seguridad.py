"""Pruebas unitarias del módulo de seguridad (hash de contraseñas y JWT)."""
import pytest
from fastapi import HTTPException
from jose import jwt

from app.core import config
from app.core.security import (
    crear_access_token,
    obtener_password_hash,
    verificar_password,
    verificar_token,
)

pytestmark = pytest.mark.unit


def test_hash_no_guarda_la_contrasena_en_texto_plano():
    hash_generado = obtener_password_hash("MiClave123")
    assert hash_generado != "MiClave123"
    assert hash_generado.startswith("$2")  # prefijo propio de bcrypt


def test_verificar_password_correcta():
    hash_generado = obtener_password_hash("MiClave123")
    assert verificar_password("MiClave123", hash_generado) is True


def test_verificar_password_incorrecta():
    hash_generado = obtener_password_hash("MiClave123")
    assert verificar_password("otraClave", hash_generado) is False


def test_dos_hashes_de_la_misma_clave_son_distintos():
    # bcrypt agrega una sal aleatoria en cada hash
    assert obtener_password_hash("abc12345") != obtener_password_hash("abc12345")


def test_token_contiene_el_usuario_y_expiracion():
    token = crear_access_token({"sub": "admin@agenda360.com"})
    datos = verificar_token(token)
    assert datos["sub"] == "admin@agenda360.com"
    assert "exp" in datos


def test_token_manipulado_es_rechazado():
    token = crear_access_token({"sub": "admin@agenda360.com"})
    with pytest.raises(HTTPException) as error:
        verificar_token(token + "x")
    assert error.value.status_code == 401


def test_token_firmado_con_otra_clave_es_rechazado():
    falso = jwt.encode({"sub": "intruso"}, "otra-clave", algorithm=config.ALGORITHM)
    with pytest.raises(HTTPException) as error:
        verificar_token(falso)
    assert error.value.status_code == 401
