import pytest

from models.admin_puesto_view import validar_nombre_puesto
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

@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "ab",
        "a" * 41,
        "aaab",
        "Holaaa",
    ],
)
def test_nombre_puesto_invalido_devuelve_none(raw):
    _require_db()
    salida = validar_nombre_puesto(raw)
    assert salida is None


@pytest.mark.parametrize(
    "raw",
    [
        "ABC",
        "Puesto Uno",
        "ab" * 20,
        "  Puesto   Con   Espacios  ",
    ],
)
def test_nombre_puesto_valido_devuelve_string(raw):
    _require_db()
    salida = validar_nombre_puesto(raw)
    assert salida is not None