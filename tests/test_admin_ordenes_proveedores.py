import pytest
from sqlalchemy import text

from Main import app as flask_app
from models import db
from models.ordenes_proveedores_model import OrdenesProveedores, OrdenesProveedoresDetalle


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def _col(model, name):
    return model.__table__.columns[name]


def test_ordenes_proveedores_requiere_db():
    _require_db()
    assert True


def test_ordenes_proveedores_tabla_y_campos_basicos():
    _require_db()
    assert OrdenesProveedores.__tablename__ == "Ordenes_Proveedores"

    assert _col(OrdenesProveedores, "ID_Orden_Proveedor").primary_key is True

    assert _col(OrdenesProveedores, "ID_Proveedor").nullable is False
    assert _col(OrdenesProveedores, "ID_Empleado_Encargado").nullable is False
    assert _col(OrdenesProveedores, "ID_Sucursal").nullable is False

    assert _col(OrdenesProveedores, "Fecha_Inicio").nullable is False
    assert _col(OrdenesProveedores, "Fecha_Estimada").nullable is True
    assert _col(OrdenesProveedores, "Fecha_Entregado").nullable is True

    assert _col(OrdenesProveedores, "Estado").nullable is False

    assert _col(OrdenesProveedores, "Numero_Factura").nullable is True
    assert _col(OrdenesProveedores, "Numero_Factura").type.length == 14

    assert _col(OrdenesProveedores, "Comentarios").nullable is True
    assert _col(OrdenesProveedores, "Comentarios").type.length == 255


def test_ordenes_proveedores_defaults():
    _require_db()
    fecha_inicio = _col(OrdenesProveedores, "Fecha_Inicio").default
    estado = _col(OrdenesProveedores, "Estado").default

    assert fecha_inicio is not None
    assert estado is not None


def test_ordenes_proveedores_relationships_existen():
    _require_db()
    rels = set(OrdenesProveedores.__mapper__.relationships.keys())
    assert "proveedor" in rels
    assert "empleado" in rels
    assert "sucursal" in rels
    assert "detalles" in rels


def test_detalle_tabla_y_campos_basicos():
    _require_db()
    assert OrdenesProveedoresDetalle.__tablename__ == "Ordenes_Proveedores_Detalle"

    assert _col(OrdenesProveedoresDetalle, "ID_Detalle").primary_key is True

    assert _col(OrdenesProveedoresDetalle, "ID_Orden_Proveedor").nullable is False
    assert _col(OrdenesProveedoresDetalle, "ID_Insumo").nullable is False
    assert _col(OrdenesProveedoresDetalle, "ID_Unidad").nullable is False
    assert _col(OrdenesProveedoresDetalle, "ID_Unidad_Recibida").nullable is True

    assert _col(OrdenesProveedoresDetalle, "Cantidad_Solicitada").nullable is False
    assert _col(OrdenesProveedoresDetalle, "Cantidad_Recibida").nullable is True


def test_detalle_relationships_existen():
    _require_db()
    rels = set(OrdenesProveedoresDetalle.__mapper__.relationships.keys())
    assert "orden" in rels
    assert "insumo" in rels
    assert "unidad" in rels
    assert "unidad_recibida" in rels


def test_repr_basico():
    _require_db()
    o = OrdenesProveedores(ID_Orden_Proveedor=123)
    d = OrdenesProveedoresDetalle(ID_Detalle=456)
    assert "123" in repr(o)
    assert "456" in repr(d)