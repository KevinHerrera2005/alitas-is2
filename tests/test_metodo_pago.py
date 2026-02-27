import os
import pytest
from sqlalchemy import text
from wtforms.validators import ValidationError

os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")

from Main import app as flask_app
from models import db

from models.metodos_pago_routes import (
    validar_nombre_tarjeta,
    validar_numero_tarjeta,
)


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "ab",
        "a" * 51,
        "aaa",
        "Juan3",
        "Juan@",
        "Jo#se",
        "A__",
        "123",
    ],
)
def test_validar_nombre_tarjeta_invalido(raw):
    _require_db()
    with pytest.raises(ValidationError):
        validar_nombre_tarjeta(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "Juan Perez",
        "José López",
        "Maria Fernanda",
        "De la Cruz",
        "AB" * 20,
    ],
)
def test_validar_nombre_tarjeta_valido(raw):
    _require_db()
    out = validar_nombre_tarjeta(raw)
    assert out is not None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "12a4",
        "123-4",
        "1234abcd",
        "12 3a 45",
        "1",
        "12",
        "123",
        "1" * 20,
    ],
)
def test_validar_numero_tarjeta_invalido(raw):
    _require_db()
    with pytest.raises(ValidationError):
        validar_numero_tarjeta(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "1234",
        "123456789012",
        "4111111111111111",
        "4111 1111 1111 1111",
        "00001234",
    ],
)
def test_validar_numero_tarjeta_valido(raw):
    _require_db()
    out = validar_numero_tarjeta(raw)
    assert out is not None