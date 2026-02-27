import pytest
from wtforms.validators import ValidationError
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
from models.usuario_cliente_routes import (
    validar_nombre_persona,
    validar_apellido_persona,
    validar_telefono_hn,
)


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "  ",
        "ab",
        "a" * 41,
        "aaa",
        "Juan3",
        "Juan@",
        "Jo#se",
        "A__",
        "123",
    ],
)
def test_validar_nombre_persona_invalido(raw):
    _require_db()
    with pytest.raises(ValidationError):
        validar_nombre_persona(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "Juan",
        "José",
        "María Fernanda",
        "Ana",
        "AB" * 20,
    ],
)
def test_validar_nombre_persona_valido(raw):
    _require_db()
    out = validar_nombre_persona(raw)
    assert out is not None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "  ",
        "ab",
        "a" * 41,
        "aaa",
        "Perez3",
        "Perez@",
        "Lo#pez",
        "A__",
        "123",
    ],
)
def test_validar_apellido_persona_invalido(raw):
    _require_db()
    with pytest.raises(ValidationError):
        validar_apellido_persona(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "Perez",
        "López",
        "De la Cruz",
        "AB" * 20,
    ],
)
def test_validar_apellido_persona_valido(raw):
    _require_db()
    out = validar_apellido_persona(raw)
    assert out is not None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "  ",
        "1234567",
        "123456789",
        "12a45678",
        "22345678",
        "02345678",
        "63345678",
    ],
)
def test_validar_telefono_hn_invalido(raw):
    _require_db()
    with pytest.raises(ValidationError):
        validar_telefono_hn(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "32345678",
        "72345678",
        "82345678",
        "92345678",
    ],
)
def test_validar_telefono_hn_valido(raw):
    
    out = validar_telefono_hn(raw)
    assert out is not None