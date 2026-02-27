import pytest

from sqlalchemy import text
import os
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
from models.admin_categoria_view import(
    _normalizar_texto,
    validar_nombre_categoria,
    validar_descripcion_categoria,
    validar_tipo_categoria
)



def test_nombre_categoria():
    _require_db()
    raw=None
    salida=_normalizar_texto(raw)
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
def test_limite_de_campo_categoria_nombre_invalido(raw):
    _require_db()
    salida = validar_nombre_categoria(raw, min_len=3, max_len=60)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "abc",
        "a" * 60,
        "  Categoria   Normal  ",
    ],
)
def test_limite_de_campo_categoria_nombre_valido(raw):
    _require_db()
    salida = validar_nombre_categoria(raw, min_len=3, max_len=60)
    assert salida is not None
    
#descripción
@pytest.mark.parametrize(
    "raw",
    [
        "a" * 201,
    ],
)
def test_limite_de_campo_categoria_descripcion_invalido(raw):
    _require_db()
    salida = validar_descripcion_categoria(raw, min_len=0, max_len=200, permitir_none=True)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
    ],
)
def test_limite_de_campo_categoria_descripcion_none_o_vacia_es_valida(raw):
    _require_db()
    salida = validar_descripcion_categoria(raw, min_len=0, max_len=200, permitir_none=True)
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
def test_limite_de_campo_categoria_descripcion_valida(raw):
    _require_db()
    salida = validar_descripcion_categoria(raw, min_len=0, max_len=200, permitir_none=True)
    assert salida is not None
    
#tipo
@pytest.mark.parametrize(
    "raw",
    [
        None,
        "abc",
        0,
        4,
        999,
        -1,
        2.5,
    ],
)
def test_tipo_categoria_no_existe_devuelve_none(raw):
    _require_db()
    salida = validar_tipo_categoria(raw)
    assert salida is None