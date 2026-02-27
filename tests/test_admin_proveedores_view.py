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
from models.admin_proveedores_view import (
    validar_estado_proveedor,
    validar_email_proveedor,
    validar_telefono_proveedor,
    validar_nombre_proveedor,
    validar_insumos_ids_seleccionados,
)


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "2",
        2,
        "activo",
        -1,
        99,
    ],
)
def test_estado_invalido_o_none_devuelve_none(raw):
    _require_db()
    salida = validar_estado_proveedor(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "0",
        "1",
        0,
        1,
        " 1 ",
        " 0 ",
    ],
)
def test_estado_valido_devuelve_0_o_1(raw):
    _require_db()
    salida = validar_estado_proveedor(raw)
    assert salida in (0, 1)


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "a@b.c",
        "a@b",
        "abcdef",
        "a" * 61 + "@x.com",
        "sin_arroba.com",
        "a@sinpunto",
    ],
)
def test_email_invalido_devuelve_none(raw):
    _require_db()
    salida = validar_email_proveedor(raw, min_len=6, max_len=60)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "abcde@f.com",
        "correo@dominio.com",
        "a" * 50 + "@x.com",
        "  correo@dominio.com  ",
    ],
)
def test_email_valido_devuelve_string(raw):
    _require_db()
    salida = validar_email_proveedor(raw)
    assert salida is not None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "123",
        "123456789",
        "22345678",
        "62345678",
        "03456789",
        "7ABC5678",
        "8123-567",
    ],
)
def test_telefono_invalido_devuelve_none(raw):
    _require_db()
    salida = validar_telefono_proveedor(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "31234567",
        "71234567",
        "81234567",
        "91234567",
        "  81234567  ",
    ],
)
def test_telefono_valido_devuelve_string(raw):
    _require_db()
    salida = validar_telefono_proveedor(raw)
    assert salida is not None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "ab",
        "a" * 41,
        "aaab",
        "xxxx",
        "Holaaa",
    ],
)
def test_nombre_proveedor_invalido_devuelve_none(raw):
    _require_db()
    salida = validar_nombre_proveedor(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "ABC",
        "Proveedor Uno",
        "ab" * 20,
        "  Proveedor   Con   Espacios  ",
    ],
)
def test_nombre_proveedor_valido_devuelve_string(raw):
    _require_db()
    salida = validar_nombre_proveedor(raw)
    assert salida is not None


def test_insumos_no_existentes_devuelve_none():
    _require_db()
    permitidos = [1, 2, 3]
    raw_ids = [999, 1000]
    salida = validar_insumos_ids_seleccionados(raw_ids, permitidos)
    assert salida is None


def test_insumos_none_devuelve_none():
    _require_db()
    salida = validar_insumos_ids_seleccionados(None, [1, 2, 3])
    assert salida is None


def test_insumos_validos_devuelve_lista():
    _require_db()
    permitidos = [10, 11, 12]
    raw_ids = [10, "11"]
    salida = validar_insumos_ids_seleccionados(raw_ids, permitidos)
    assert salida is not None