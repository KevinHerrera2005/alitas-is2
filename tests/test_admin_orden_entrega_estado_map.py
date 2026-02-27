import pytest
from wtforms.validators import ValidationError
from models.admin_orden_entrega_view import OrdenEntregaAdmin
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
    def __init__(self, data):
        self.data = data


class _Form:
    def __init__(self, estado, motivo=""):
        self.estado = _Field(estado)
        self.Motivo_Cancelacion = _Field(motivo)


class _Model:
    def __init__(self, estado):
        self.estado = estado
        self.Motivo_Cancelacion = None


def _instancia_sin_init():
    admin = OrdenEntregaAdmin.__new__(OrdenEntregaAdmin)
    admin._guardar_historial_si_aplica = lambda model, anterior, nuevo, motivo: None
    return admin


@pytest.mark.parametrize(
    "estado_actual, estado_nuevo",
    [
        (0, 3),
        (3, 1),
        (1, 3),
        (1, "dsadwqdq"),
    ],
)
def test_no_permite_saltos_invalidos_de_estado(estado_actual, estado_nuevo):
    _require_db()
    admin = _instancia_sin_init()
    admin._es_repartidor = lambda: False

    form = _Form(estado_nuevo)
    model = _Model(estado_actual)

    with pytest.raises(ValidationError):
        admin.on_model_change(form, model, False)

    assert model.estado == estado_actual


def test_no_permite_cancelar_orden_ya_entregada():
    _require_db()
    admin = _instancia_sin_init()
    admin._es_repartidor = lambda: False

    form = _Form(4, "Cancelada por error")
    model = _Model(3)

    with pytest.raises(ValidationError):
        admin.on_model_change(form, model, False)

    assert model.estado == 3