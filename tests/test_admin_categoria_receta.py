import os
import pytest
from sqlalchemy import text

os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")

from Main import app as flask_app
from models import db

from models.admin_categoria_receta_view import (
    _normalizar_texto,
    validar_nombre_categoria_receta,
    validar_descripcion_categoria_receta,
)


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def test_nombre_categoria_receta_normalizar_none():
    _require_db()
    raw = None
    salida = _normalizar_texto(raw)
    assert not salida


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "  ",
        "ab",
        "a" * 61,
    ],
)
def test_limite_de_campo_categoria_receta_nombre_invalido(raw):
    _require_db()
    salida = validar_nombre_categoria_receta(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "abc",
        "a" * 60,
        "  Categoria   Receta   Normal  ",
    ],
)
def test_limite_de_campo_categoria_receta_nombre_valido(raw):
    _require_db()
    salida = validar_nombre_categoria_receta(raw)
    assert salida is not None


@pytest.mark.parametrize(
    "raw",
    [
        "a" * 201,
    ],
)
def test_limite_de_campo_categoria_receta_descripcion_invalido(raw):
    _require_db()
    salida = validar_descripcion_categoria_receta(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
    ],
)
def test_limite_de_campo_categoria_receta_descripcion_none_o_vacia_es_valida(raw):
    _require_db()
    salida = validar_descripcion_categoria_receta(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "a",
        "Descripcion corta",
        "a" * 200,
        "  Descripcion   con   espacios   ",
    ],
)
def test_limite_de_campo_categoria_receta_descripcion_valida(raw):
    _require_db()
    salida = validar_descripcion_categoria_receta(raw)
    assert salida is not None