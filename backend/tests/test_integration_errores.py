"""
Errores internos del servidor (hallazgo H-09).

Un error no controlado debe llegar al panel como JSON con el detalle y con
las cabeceras CORS; antes el navegador lo mostraba como "no se pudo conectar".
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.integration


@app.get("/_prueba_error_interno", include_in_schema=False)
def _ruta_que_falla():
    raise RuntimeError("fallo simulado")


def test_error_interno_responde_json_con_cors():
    cliente = TestClient(app, raise_server_exceptions=False)
    r = cliente.get("/_prueba_error_interno", headers={"Origin": "http://localhost:5174"})
    assert r.status_code == 500
    assert "fallo simulado" in r.json()["detail"]
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5174"


def test_cors_acepta_cualquier_puerto_de_localhost():
    cliente = TestClient(app)
    r = cliente.options(
        "/clients/",
        headers={"Origin": "http://127.0.0.1:5175", "Access-Control-Request-Method": "GET"},
    )
    assert r.headers.get("access-control-allow-origin") == "http://127.0.0.1:5175"
