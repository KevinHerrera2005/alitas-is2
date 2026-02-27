import pytest
from sqlalchemy import text
from wtforms.validators import ValidationError

from Main import app as flask_app
from models import db


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


class _Field:
    def __init__(self, data=None):
        self.data = data


class _Form:
    def __init__(self, nombre=None, descripcion=None, tasa=None, categorias_ids=None, activo=None):
        self.Nombre_Impuesto = _Field(nombre)
        self.descripcion = _Field(descripcion)
        self.tasa = _Field(tasa)
        self.categorias_ids = _Field(categorias_ids or [])
        if activo is not None:
            self.activo = _Field(activo)


class _FakeNoAutoflush:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeQuery:
    def __init__(self, first_result=None):
        self._first_result = first_result
    def filter(self, *args, **kwargs):
        return self
    def first(self):
        return self._first_result


class _FakeSession:
    def __init__(self, first_result=None):
        self.no_autoflush = _FakeNoAutoflush()
        self._first_result = first_result
    def query(self, *_):
        return _FakeQuery(first_result=self._first_result)


def _admin_sin_init(fake_session):
    from models.admin_impuestos_view import ImpuestoAdmin
    admin = ImpuestoAdmin.__new__(ImpuestoAdmin)
    admin.session = fake_session
    return admin


def test_validar_campos_falla_si_faltan_obligatorios():
    _require_db()
    admin = _admin_sin_init(_FakeSession(first_result=None))

    class M:
        ID_Impuesto = None

    form = _Form(nombre="", descripcion="x", tasa=10, categorias_ids=[1])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)

    form = _Form(nombre="IVA", descripcion="", tasa=10, categorias_ids=[1])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)

    form = _Form(nombre="IVA", descripcion="desc", tasa=None, categorias_ids=[1])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)


def test_validar_campos_falla_si_tasa_no_numerica_o_fuera_de_rango():
    _require_db()
    admin = _admin_sin_init(_FakeSession(first_result=None))

    class M:
        ID_Impuesto = None

    form = _Form(nombre="IVA", descripcion="desc", tasa="X", categorias_ids=[1])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)

    form = _Form(nombre="IVA", descripcion="desc", tasa=-1, categorias_ids=[1])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)

    form = _Form(nombre="IVA", descripcion="desc", tasa=1001, categorias_ids=[1])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)


def test_validar_campos_falla_si_no_hay_categorias():
    _require_db()
    admin = _admin_sin_init(_FakeSession(first_result=None))

    class M:
        ID_Impuesto = None

    form = _Form(nombre="IVA", descripcion="desc", tasa=15, categorias_ids=[])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)


def test_validar_campos_falla_si_nombre_duplicado():
    _require_db()
    admin = _admin_sin_init(_FakeSession(first_result=object()))

    class M:
        ID_Impuesto = None

    form = _Form(nombre="IVA", descripcion="desc", tasa=15, categorias_ids=[1])
    with pytest.raises(ValidationError):
        admin._validar_campos(form, M(), is_created=True)


def test_validar_campos_asigna_valores_y_categoria_principal():
    _require_db()
    admin = _admin_sin_init(_FakeSession(first_result=None))

    class M:
        ID_Impuesto = None
        Nombre_Impuesto = None
        descripcion = None
        tasa = None
        activo = None
        ID_Categoria = None

    m = M()
    form = _Form(nombre="  IVA  ", descripcion="  General  ", tasa="15", categorias_ids=[9, 10], activo="1")
    admin._validar_campos(form, m, is_created=False)

    assert m.Nombre_Impuesto == "IVA"
    assert m.descripcion == "General"
    assert m.tasa == 15.0
    assert m.activo == 1
    assert m.ID_Categoria == 9
