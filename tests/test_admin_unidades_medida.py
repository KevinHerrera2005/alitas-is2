import os
import pytest
from sqlalchemy import text

os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")

from Main import app as flask_app
from models import db


def _importar_modelo():
    try:
        from models.unidades_medida_model import Unidades_medida
        return Unidades_medida
    except Exception:
        return Unidades_medida


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def _crear_unidad(nombre, abreviatura, tipo):
    Unidades_medida = _importar_modelo()
    unidad = Unidades_medida(Nombre=nombre, abreviatura=abreviatura, Tipo=tipo)
    db.session.add(unidad)
    db.session.flush()
    return unidad


@pytest.mark.parametrize(
    "nombre, abreviatura, tipo",
    [
        (None, "kg", 1),
        ("Kilogramo", None, 1),
        ("Kilogramo", "kg", None),
    ],
)
def test_unidades_medida_campos_obligatorios_fallan(nombre, abreviatura, tipo):
    _require_db()
    with flask_app.app_context():
        with pytest.raises(Exception):
            _crear_unidad(nombre, abreviatura, tipo)
        db.session.rollback()


def test_unidades_medida_nombre_mayor_a_50_falla():
    _require_db()
    with flask_app.app_context():
        with pytest.raises(Exception):
            _crear_unidad("a" * 51, "kg", 1)
        db.session.rollback()


def test_unidades_medida_abreviatura_mayor_a_10_falla():
    _require_db()
    with flask_app.app_context():
        with pytest.raises(Exception):
            _crear_unidad("Kilogramo", "a" * 11, 1)
        db.session.rollback()


def test_unidades_medida_valida_inserta():
    _require_db()
    with flask_app.app_context():
        unidad = _crear_unidad("Kilogramo", "kg", 1)
        assert unidad is not None
        db.session.rollback()