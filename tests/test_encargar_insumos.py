import pytest
from sqlalchemy import text

from Main import app as flask_app
from models import db


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def test_encargar_insumos_requiere_db():
    _require_db()
    assert True


def test_encargar_insumos_post_sin_lineas_json_redirige():
    _require_db()
    flask_app.config["LOGIN_DISABLED"] = True

    client = flask_app.test_client()
    resp = client.post("/encargar_insumos", data={}, follow_redirects=False)

    assert resp.status_code == 302
    assert "/encargar_insumos" in resp.headers.get("Location", "")


def test_encargar_insumos_post_json_invalido_redirige():
    _require_db()
    flask_app.config["LOGIN_DISABLED"] = True

    client = flask_app.test_client()
    resp = client.post(
        "/encargar_insumos",
        data={"lineas_json": "{no_es_json}"},
        follow_redirects=False,
    )

    assert resp.status_code == 302
    assert "/encargar_insumos" in resp.headers.get("Location", "")


def test_encargar_insumos_post_lista_vacia_redirige():
    _require_db()
    flask_app.config["LOGIN_DISABLED"] = True

    client = flask_app.test_client()
    resp = client.post(
        "/encargar_insumos",
        data={"lineas_json": "[]"},
        follow_redirects=False,
    )

    assert resp.status_code == 302
    assert "/encargar_insumos" in resp.headers.get("Location", "")


def test_encargar_insumos_post_lineas_invalidas_redirige():
    _require_db()
    flask_app.config["LOGIN_DISABLED"] = True

    client = flask_app.test_client()
    resp = client.post(
        "/encargar_insumos",
        data={
            "lineas_json": '[{"insumo_id": null, "proveedor_id": null, "sucursal_id": null, "cantidad": "0"}]'
        },
        follow_redirects=False,
    )

    assert resp.status_code == 302
    assert "/encargar_insumos" in resp.headers.get("Location", "")