import os
import importlib
import pytest
from sqlalchemy import text

os.environ["SKIP_DB_INIT"] = "1"
os.environ["SKIP_BOOTSTRAP"] = "0"

for k in list(importlib.sys.modules.keys()):
    if k == "Main" or k.startswith("Main."):
        del importlib.sys.modules[k]

main_module = importlib.import_module("Main")
flask_app = main_module.app

from models import db


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


def _buscar_ruta_crear_insumo(app):
    _require_db()
    for rule in app.url_map.iter_rules():
        p = (rule.rule or "").lower()
        if "insumo" in p and ("guardar" in p or "crear" in p or "create" in p or "new" in p):
            if "post" in {m.lower() for m in (rule.methods or set())}:
                return rule.rule
    pytest.fail("No encontré una ruta POST para crear insumo.")


def _post_crear_insumo(client, url, data):
    _require_db()
    return client.post(url, data=data, follow_redirects=False)


@pytest.mark.mssql
def test_crear_insumo_rechaza_nombre_vacio(client):
    _require_db()
    url = _buscar_ruta_crear_insumo(flask_app)

    resp = _post_crear_insumo(
        client,
        url,
        {
            "Nombre_insumo": "   ",
            "precio_lempiras": "10",
            "peso_individual": "1",
            "ID_Unidad": "1",
        },
    )
    assert resp.status_code in (302, 400)


@pytest.mark.mssql
def test_crear_insumo_rechaza_precio_no_numerico(client):
    _require_db()
    url = _buscar_ruta_crear_insumo(flask_app)

    resp = _post_crear_insumo(
        client,
        url,
        {
            "Nombre_insumo": "Insumo Prueba",
            "precio_lempiras": "abc",
            "peso_individual": "1",
            "ID_Unidad": "1",
        },
    )
    assert resp.status_code in (302, 400)


@pytest.mark.mssql
def test_crear_insumo_rechaza_unidad_none(client):
    _require_db()
    url = _buscar_ruta_crear_insumo(flask_app)

    resp = _post_crear_insumo(
        client,
        url,
        {
            "Nombre_insumo": "Insumo Prueba",
            "precio_lempiras": "10",
            "peso_individual": "1",
            "ID_Unidad": "",
        },
    )
    assert resp.status_code in (302, 400)


@pytest.mark.mssql
def test_crear_insumo_ok_redirige(client):
    _require_db()
    url = _buscar_ruta_crear_insumo(flask_app)

    resp = _post_crear_insumo(
        client,
        url,
        {
            "Nombre_insumo": "Insumo Prueba",
            "precio_lempiras": "10",
            "peso_individual": "1",
            "ID_Unidad": "1",
        },
    )
    assert resp.status_code in (301, 302)
    assert (resp.headers.get("Location") or "") != ""