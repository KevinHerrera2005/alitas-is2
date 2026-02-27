import pytest
from sqlalchemy import text
import os
from Main import app as flask_app
import pytest
from sqlalchemy import text
from models import db
from models.crear_recetas import (
    evitar_valores_nulos,
    validar_cantidad_usada,
    validar_insumo_existe,
    validar_categoria_existe,
)
os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")

def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def test_nombre_nulo_o_espacios():
    _require_db()
    assert evitar_valores_nulos(None) is None
    assert evitar_valores_nulos("") is None
    assert evitar_valores_nulos("   ") is None


def test_nombre_solo_numeros():
    _require_db()
    assert evitar_valores_nulos("12345") is None


def test_nombre_con_tres_letras_iguales():
    _require_db()
    assert evitar_valores_nulos("pizaaa") is None


def test_nombre_valido_devuelve_limpio():
    _require_db()
    out = evitar_valores_nulos("  Pizza Suprema  ")
    assert out == "Pizza Suprema"


def test_agregar_insumo_inexistente():
    _require_db()
    out = validar_insumo_existe(99999999)
    assert out is False


def test_categoria_inexistente():
    _require_db()
    out = validar_categoria_existe(99999999)
    assert out is False


@pytest.mark.parametrize("raw", [0, -1, -0.5, 100000, 999999])
def test_cantidad_invalida(raw):
    _require_db()
    out = validar_cantidad_usada(raw)
    assert out is None


def test_cantidad_valida():
    _require_db()
    out = validar_cantidad_usada(10)
    assert out == 10.0