import os
import pytest
from sqlalchemy import text
from wtforms.validators import ValidationError

os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")

from Main import app as flask_app
from models import db
from models.tusdirecciones import validar_descripcion_direccion


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def _texto_300_sin_3_iguales():
    base = "AB"
    s = base * 150
    return s[:300]


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "aaa",
        "bbb",
        "111",
        "a" * 301,
    ],
)
def test_validar_descripcion_direccion_invalido(raw):
    _require_db()
    with pytest.raises(ValidationError):
        validar_descripcion_direccion(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "Casa 1, colonia Kennedy",
        "Apartamento 2B",
        "Frente al parque central",
        _texto_300_sin_3_iguales(),
        "  Calle principal, casa azul  ",
    ],
)
def test_validar_descripcion_direccion_valido(raw):
    _require_db()
    out = validar_descripcion_direccion(raw)
    assert out is not None