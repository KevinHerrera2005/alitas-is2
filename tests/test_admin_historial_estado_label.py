import pytest
from models.admin_historial_ordenes_proveedores_view import HistorialOrdenesProveedoresAdmin

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
def _instancia_sin_init():
    return HistorialOrdenesProveedoresAdmin.__new__(HistorialOrdenesProveedoresAdmin)


@pytest.mark.parametrize(
    "raw, esperado",
    [
        (0, "Pendiente"),
        (1, "Enviada"),
        (2, "Entregada"),
        (3, "Cancelada"),
        ("0", "Pendiente"),
        ("2", "Entregada"),
    ],
)
def test_estado_label_valores_conocidos(raw, esperado):
    _require_db()
    admin = _instancia_sin_init()
    salida = admin._estado_label(raw)
    assert salida == esperado


@pytest.mark.parametrize(
    "raw, esperado",
    [
        (99, "99"),
        ("7", "7"),
        (None, "None"),
    ],
)
def test_estado_label_valores_desconocidos(raw, esperado):
    _require_db()
    admin = _instancia_sin_init()
    salida = admin._estado_label(raw)
    assert salida == esperado