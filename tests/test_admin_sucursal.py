import os
from types import SimpleNamespace

import pytest
from sqlalchemy import text

os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")

from Main import app as flask_app
from models import db
from models.admin_sucursal_view import SucursalAdmin


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def _view():
    v = SucursalAdmin.__new__(SucursalAdmin)
    v.session = db.session
    return v


def _form(descripcion, direccion, estado=None):
    f = SimpleNamespace(
        Descripcion=SimpleNamespace(data=descripcion),
        DireccionTexto=SimpleNamespace(data=direccion),
    )
    if estado is not None:
        f.estado = SimpleNamespace(data=estado)
    return f


def _model(id_direccion=None, estado=1):
    return SimpleNamespace(Descripcion=None, ID_Direccion=id_direccion, estado=estado)


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_sucursal_descripcion_invalida(raw):
    _require_db()
    with flask_app.app_context():
        view = _view()
        form = _form(raw, "Direccion valida")
        model = _model()

        with pytest.raises(ValueError):
            view.on_model_change(form, model, True)

        db.session.rollback()


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_sucursal_direccion_invalida(raw):
    _require_db()
    with flask_app.app_context():
        view = _view()
        form = _form("Sucursal valida", raw)
        model = _model()

        with pytest.raises(ValueError):
            view.on_model_change(form, model, True)

        db.session.rollback()


def test_sucursal_normaliza_espacios_y_crea_direccion():
    _require_db()
    with flask_app.app_context():
        view = _view()
        form = _form("  suc   principal  ", "  Direccion   principal  ")
        model = _model()

        view.on_model_change(form, model, True)

        assert model.Descripcion == "suc principal"
        assert model.estado == 1
        assert isinstance(model.ID_Direccion, int)

        db.session.rollback()


def test_sucursal_editar_estado_y_actualiza_direccion():
    _require_db()
    with flask_app.app_context():
        view = _view()

        form_create = _form("Sucursal", "Direccion original")
        model = _model()

        view.on_model_change(form_create, model, True)

        assert isinstance(model.ID_Direccion, int)
        assert model.estado == 1

        form_edit_0 = _form("Sucursal", "Direccion editada", estado="0")
        view.on_model_change(form_edit_0, model, False)
        assert model.estado == 0

        form_edit_1 = _form("Sucursal", "Direccion editada 2", estado="1")
        view.on_model_change(form_edit_1, model, False)
        assert model.estado == 1

        db.session.rollback()