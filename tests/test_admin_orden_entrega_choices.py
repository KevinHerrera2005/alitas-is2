import pytest
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

class _Field:
    def __init__(self):
        self.choices = []
        self.data = None


class _Form:
    def __init__(self):
        self.estado = _Field()


class _Obj:
    def __init__(self, estado):
        self.estado = estado


def _admin_sin_init():
    from models.admin_orden_entrega_view import OrdenEntregaAdmin
    return OrdenEntregaAdmin.__new__(OrdenEntregaAdmin)


@pytest.mark.parametrize(
    "estado_inicial, es_repartidor, esperado",
    [
        (0, False, ["0", "4", "1"]),
        (0, True, ["0", "4"]),
        (1, True, ["1", "4", "2"]),
        (2, True, ["2", "4", "3"]),
        (1, False, ["1", "4"]),
        (3, True, ["3"]),
        (4, False, ["4"]),
    ],
)
def test_cargar_choices_estado(estado_inicial, es_repartidor, esperado, monkeypatch):
    _require_db()
    admin = _admin_sin_init()

    monkeypatch.setattr(admin, "_es_repartidor", lambda: es_repartidor, raising=True)

    form = _Form()
    obj = _Obj(estado_inicial)

    admin._cargar_choices_estado(form, obj=obj)

    valores = [v for v, _ in form.estado.choices]
    assert valores == esperado


@pytest.mark.parametrize(
    "estado, esperado",
    [
        (99, "99"),
        ("X", "X"),
    ],
)
def test_estado_label_valores_desconocidos(estado, esperado):
    _require_db()
    admin = _admin_sin_init()

    class M:
        pass

    m = M()
    m.estado = estado

    salida = admin._estado_label(m)
    assert salida == esperado