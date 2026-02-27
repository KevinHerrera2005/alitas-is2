import os
import importlib
import uuid
import pytest
from sqlalchemy import text
import pytest
from wtforms.validators import ValidationError

from models.factura_routes import validar_metodo_pago

pytestmark = pytest.mark.filterwarnings(
    "ignore:The Query.get\\(\\) method is considered legacy.*:sqlalchemy.exc.LegacyAPIWarning"
)
os.environ["SKIP_DB_INIT"] = "1"
os.environ["SKIP_BOOTSTRAP"] = "0"

for k in list(importlib.sys.modules.keys()):
    if k == "Main" or k.startswith("Main."):
        del importlib.sys.modules[k]

main_module = importlib.import_module("Main")
flask_app = main_module.app

from models import db
from models.direccion_model import Direccion
from models.sucursal_model import Sucursal
from models.empleado_model import Empleado, Puesto


def _ensure_login(app):
    if "login" in app.view_functions:
        return

    @app.route("/login", endpoint="login")
    def login():
        return "OK", 200


_ensure_login(flask_app)


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["LOGIN_DISABLED"] = True
    return flask_app.test_client()


def _crear_sucursal_prueba():
    d = Direccion(Descripcion="Direccion Test Facturar")
    db.session.add(d)
    db.session.commit()

    s = Sucursal(Descripcion="Sucursal Test Facturar", ID_Direccion=d.ID_Direccion, estado=1)
    db.session.add(s)
    db.session.commit()

    return s.ID_sucursal, d.ID_Direccion


def _puesto_existe(id_puesto):
    return db.session.get(Puesto, id_puesto) is not None


def _crear_empleado_prueba(id_sucursal, id_puesto):
    u = uuid.uuid4().hex[:12]
    e = Empleado(
        Nombre="Test",
        Apellido="Empleado",
        Username=f"test_{id_puesto}_{u}",
        Password="x",
        Telefono="99999999",
        Email=None,
        ID_Puesto=id_puesto,
        ID_sucursal=id_sucursal,
        estado=1,
    )
    db.session.add(e)
    db.session.commit()
    return e.ID_Empleado


def _borrar_empleado(id_empleado):
    if not id_empleado:
        return
    obj = db.session.get(Empleado, id_empleado)
    if obj:
        db.session.delete(obj)
        db.session.commit()


def _borrar_sucursal_y_direccion(id_sucursal, id_direccion):
    s = db.session.get(Sucursal, id_sucursal)
    if s:
        db.session.delete(s)
        db.session.commit()

    d = db.session.get(Direccion, id_direccion)
    if d:
        db.session.delete(d)
        db.session.commit()


def test_checkout_redirige_a_login_si_no_hay_cliente_id(client):
    _require_db()
    resp = client.get("/carrito/checkout", follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert "/login" in (resp.headers.get("Location") or "")


@pytest.mark.parametrize(
    "raw_cliente_id",
    [
        None,
        "",
        "   ",
        "123",
        0,
        -1,
    ],
)
def test_checkout_no_debe_con_cliente_id_todo_raro(client, raw_cliente_id):
    _require_db()

    with client.session_transaction() as s:
        if raw_cliente_id is None:
            s.pop("cliente_id", None)
        else:
            s["cliente_id"] = raw_cliente_id

    resp = client.get("/carrito/checkout", follow_redirects=False)
    assert resp.status_code in (200, 301, 302, 400)


def test_checkout_cliente_id_string_revienta(client):
    _require_db()

    with client.session_transaction() as s:
        s["cliente_id"] = "X"

    with pytest.raises(Exception):
        client.get("/carrito/checkout", follow_redirects=False)


def test_facturar_redirige_a_checkout_si_falta_sucursal_en_sesion(client):
    _require_db()

    with client.session_transaction() as s:
        s["cliente_id"] = 1
        s.pop("checkout_sucursal_id", None)

    resp = client.get("/facturar", follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert "/carrito/checkout" in (resp.headers.get("Location") or "")


@pytest.mark.parametrize(
    "raw_sucursal_id",
    [
        None,
        "",
        "  ",
        "X",
        "12X",
        0,
        -5,
    ],
)
def test_facturar_redirige_a_checkout_si_sucursal_invalida_en_sesion(client, raw_sucursal_id):
    _require_db()

    with client.session_transaction() as s:
        s["cliente_id"] = 1
        if raw_sucursal_id is None:
            s.pop("checkout_sucursal_id", None)
        else:
            s["checkout_sucursal_id"] = raw_sucursal_id

    resp = client.get("/facturar", follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert "/carrito/checkout" in (resp.headers.get("Location") or "")


def test_facturar_redirige_a_checkout_si_sucursal_id_no_existe(client):
    _require_db()

    with client.session_transaction() as s:
        s["cliente_id"] = 1
        s["checkout_sucursal_id"] = 99999999

    resp = client.get("/facturar", follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert "/carrito/checkout" in (resp.headers.get("Location") or "")


def test_facturar_redirige_a_checkout_si_no_hay_cajero_en_sucursal(client):
    _require_db()

    with flask_app.app_context():
        if not _puesto_existe(13):
            pytest.fail("No existe Puesto ID=13 (cajero) en la BD.")

        id_sucursal, id_direccion = _crear_sucursal_prueba()

        try:
            with client.session_transaction() as s:
                s["cliente_id"] = 1
                s["checkout_sucursal_id"] = id_sucursal

            resp = client.get("/facturar", follow_redirects=False)
            assert resp.status_code in (301, 302)
            assert "/carrito/checkout" in (resp.headers.get("Location") or "")
        finally:
            _borrar_sucursal_y_direccion(id_sucursal, id_direccion)


def test_facturar_redirige_a_checkout_si_no_hay_repartidor_en_sucursal(client):
    _require_db()

    with flask_app.app_context():
        if not _puesto_existe(13):
            pytest.fail("No existe Puesto ID=13 (cajero) en la BD.")
        if not _puesto_existe(4):
            pytest.fail("No existe Puesto ID=4 (repartidor) en la BD.")

        id_sucursal, id_direccion = _crear_sucursal_prueba()
        id_empleado_cajero = None

        try:
            id_empleado_cajero = _crear_empleado_prueba(id_sucursal, 13)

            with client.session_transaction() as s:
                s["cliente_id"] = 1
                s["checkout_sucursal_id"] = id_sucursal

            resp = client.get("/facturar", follow_redirects=False)
            assert resp.status_code in (301, 302)
            assert "/carrito/checkout" in (resp.headers.get("Location") or "")
        finally:
            _borrar_empleado(id_empleado_cajero)
            _borrar_sucursal_y_direccion(id_sucursal, id_direccion)




@pytest.mark.parametrize(
    "raw,es_valido",
    [
        (None, False),
        ("", False),
        ("   ", False),
        ("1", True),
    ],
)
def test_validar_metodo_pago(raw, es_valido):
    if es_valido:
        out = validar_metodo_pago(raw)
        assert out is not None
    else:
        with pytest.raises(ValidationError):
            validar_metodo_pago(raw)