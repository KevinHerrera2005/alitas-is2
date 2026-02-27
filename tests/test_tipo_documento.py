import pytest
from sqlalchemy import text

from Main import app as flask_app
from models import db
from models.tipo_documento_model import TipoDocumento
from models.admin_tipo_documento_view import (
    validar_tipo_documento,
    validar_descripcion_documento,
    validar_numero_documento,
)


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


@pytest.mark.parametrize(
    "raw,esperado",
    [
        ("1", 1),
        (1, 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
    ],
)
def test_validar_tipo_documento_valido(raw, esperado):
    _require_db()
    assert validar_tipo_documento(raw) == esperado


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "0",
        "5",
        "dni",
        -1,
        2.5,
    ],
)
def test_validar_tipo_documento_invalido(raw):
    _require_db()
    assert validar_tipo_documento(raw) is None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "  ",
        "aa",
        "doc@@",
        "a" * 100,
        "pizaaa",
    ],
)
def test_validar_descripcion_documento_invalida(raw):
    _require_db()
    assert validar_descripcion_documento(raw) is None


def test_validar_descripcion_documento_valida():
    _require_db()
    assert validar_descripcion_documento("Documento válido") == "Documento válido"


@pytest.mark.parametrize(
    "tipo,numero_ok,numero_bad",
    [
        (1, "0801199901234"[:13], "123"),
        (2, "08011999012345"[:14], "ABC"),
        (3, "A1234567", "@@@"),
        (4, "OTRO123", ""),
    ],
)
def test_validar_numero_documento_por_tipo(tipo, numero_ok, numero_bad):
    _require_db()
    assert validar_numero_documento(numero_ok, tipo) is not None
    assert validar_numero_documento(numero_bad, tipo) is None


def test_tipo_documento_registros_deben_existir_en_bd():
    _require_db()
    with flask_app.app_context():
        total = TipoDocumento.query.count()
        assert total > 0
