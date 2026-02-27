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
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")
import pytest
from models.crear_recetas import (
    evitar_valores_nulos,
    validar_insumo_existe,
    validar_categoria_existe,
    validar_cantidad_usada,
)


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "12345",
        "Holaaa",
        "aaa",
    ],
)
def test_nombre_invalido(raw):
    _require_db()
    salida = evitar_valores_nulos(raw)
    assert not salida


@pytest.mark.parametrize(
    "raw",
    [
        "  Pupusas  ",
        "Pizza",
        "Tacos",
    ],
)
def test_nombre_valido(raw):
    _require_db()
    salida = evitar_valores_nulos(raw)
    assert salida
    assert salida == salida.strip()


@pytest.mark.parametrize(
    "raw",
    [
        -1,
        0,
        99999999,
    ],
)
def test_agregar_insumo_inexistente(raw):
    _require_db()
    salida = validar_insumo_existe(raw)
    assert not salida


@pytest.mark.parametrize(
    "raw",
    [
        -1,
        0,
        99999999,
    ],
)
def test_categoria_inexistente(raw):
    _require_db()
    salida = validar_categoria_existe(raw)
    assert not salida


@pytest.mark.parametrize(
    "val",
    [
        0,
        -1,
        -0.5,
        100000,
        999999,
    ],
)
def test_cantidad_invalida(val):
    _require_db()
    salida = validar_cantidad_usada(val)
    assert not salida


@pytest.mark.parametrize(
    "val",
    [
        1,
        5,
        10,
    ],
)
def test_cantidad_valida(val):
    _require_db()
    salida = validar_cantidad_usada(val)
    assert salida == val