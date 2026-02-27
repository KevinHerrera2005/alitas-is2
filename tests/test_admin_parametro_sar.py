import pytest
import os
import pytest
from sqlalchemy import text
from Main import app as flask_app
from models import db
os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")

def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e)._name_}: {e}")
from models.admin_parametro_sar_view import (
    validar_parametro_nombre,
    validar_parametro_valor,
)


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "ab",
        "a" * 41,
        "abc123",
        "123",
        "aaab",
        "Holaaa",
    ],
)
def test_parametro_nombre_invalido_devuelve_none(raw):
    _require_db()
    salida = validar_parametro_nombre(raw, min_len=3, max_len=40)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "ABC",
        "Parametro SAR",
        "Parametro Con Espacios",
        "AbCdEf",
    ],
)
def test_parametro_nombre_valido_devuelve_string(raw):
    _require_db()
    salida = validar_parametro_nombre(raw, min_len=3, max_len=40)
    assert salida is not None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "dsadsa",
        "12a3",
        "-5",
        "0",
        0,
        -1,
    ],
)
def test_parametro_valor_invalido_devuelve_none(raw):
    _require_db()
    salida = validar_parametro_valor(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "1",
        "10",
        25,
        "  99  ",
    ],
)
def test_parametro_valor_valido_devuelve_int(raw):
    _require_db()
    salida = validar_parametro_valor(raw)
    assert salida is not None
    assert isinstance(salida, int)
    assert salida > 0