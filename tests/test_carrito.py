import os
import pytest
from sqlalchemy import text
from Main import app as flask_app
from models import db
os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")


from models.carrito_routes import (
    _limite_cantidad,
    _cliente_valido,
    _in_re_valido,
    _repartidor_misma_sucursal,
    _hay_repartidor_disponible,
)


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")



@pytest.mark.parametrize(
    "cantidad_a_agregar",
    [
        "dwqdsaqd",
        21,
        -2,
        None,
        32132131232231231213231231231
    ],
)
def test_carrito_no_negativos_no_nulos_no_superar_limite(cantidad_a_agregar):
    _require_db()
    salida = _limite_cantidad(0, cantidad_a_agregar)
    assert salida is False



def test_carrito_no_agarra_insumos_que_no_existen():
    _require_db()
    insumos=None
    salida = _in_re_valido(insumos)
    assert salida is False


def test_carrito_sin_cliente_asignado():
    _require_db()
    raw = None
    salida = _cliente_valido(raw)
    assert salida is False


def test_carrito_usuario_none_es_invalido():
    _require_db()
    raw = None
    salida = _cliente_valido(raw)
    assert salida is False


def test_carrito_no_hay_repartidor_disponible():
    _require_db()
    raw = None
    salida = _hay_repartidor_disponible(raw)
    assert salida is False


def test_carrito_repartidor_sucursal_diferente_a_cliente():
    _require_db()
    id_sucursal_cliente = 1
    id_sucursal_repartidor = 2
    salida = _repartidor_misma_sucursal(id_sucursal_cliente, id_sucursal_repartidor)
    assert salida is False