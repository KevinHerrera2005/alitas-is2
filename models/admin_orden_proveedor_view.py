from flask import redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import SelectField, FloatField

from models import db
from models.ordenes_proveedores_model import (
    OrdenesProveedores,
    OrdenesProveedoresDetalle,
)
from models.proveedores_model import Proveedor
from models.empleado_model import Empleado
from models.sucursal_model import Sucursal
from models.insumo_model import Insumo
from models.unidades_medida_model import Unidades_medida


class SecureModelView(ModelView):
    """Vista base: solo empleados autenticados pueden entrar al admin."""

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def inaccessible_callback(self, name, **kwargs):
        flash("Debes iniciar sesión como empleado para acceder al panel administrativo.", "warning")
        return redirect(url_for("login"))


class OrdenesProveedoresAdmin(SecureModelView):
    """Admin para la tabla Ordenes_Proveedores."""

    column_list = (
        "ID_Orden_Proveedor",
        "Fecha_Inicio",
        "Fecha_Estimada",
        "Fecha_Entregado",
        "Estado",
        "proveedor",
        "empleado",
        "sucursal",
        "Comentarios",
    )

    column_labels = {
        "ID_Orden_Proveedor": "ID",
        "Fecha_Inicio": "Fecha inicio",
        "Fecha_Estimada": "Fecha estimada",
        "Fecha_Entregado": "Fecha entregado",
        "Estado": "Estado",
        "proveedor": "Proveedor",
        "empleado": "Encargado",
        "sucursal": "Sucursal",
        "Comentarios": "Comentarios",
    }

    form_columns = (
        "ID_Proveedor",
        "ID_Empleado_Encargado",
        "ID_Sucursal",
        "Fecha_Inicio",
        "Fecha_Estimada",
        "Fecha_Entregado",
        "Estado",
        "Comentarios",
    )

    form_overrides = {
        "Estado": SelectField,
    }

    def _cargar_choices(self, form):
        form.Estado.choices = [
            ("0", "Pendiente"),
            ("1", "Enviada"),
            ("2", "Entregada"),
            ("3", "Cancelada"),
        ]
        form.ID_Proveedor.choices = [
            (p.ID_Proveedor, p.Nombre_Proveedor) for p in Proveedor.query.all()
        ]
        form.ID_Empleado_Encargado.choices = [
            (e.ID_Empleado, e.Nombre) for e in Empleado.query.all()
        ]
        form.ID_Sucursal.choices = [
            (s.ID_sucursal, s.Descripcion) for s in Sucursal.query.all()
        ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._cargar_choices(form)
        form.Estado.data = "0"
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._cargar_choices(form)
        if obj is not None:
            form.Estado.data = str(obj.Estado)
        return form


class OrdenesProveedoresDetalleAdmin(SecureModelView):
    """Admin para la tabla Ordenes_Proveedores_Detalle."""

    column_list = (
        "ID_Detalle",
        "orden",
        "insumo",
        "unidad",
        "Cantidad_Solicitada",
        "Cantidad_Recibida",
    )

    column_labels = {
        "ID_Detalle": "ID",
        "orden": "Orden",
        "insumo": "Insumo",
        "unidad": "Unidad",
        "Cantidad_Solicitada": "Cant. solicitada",
        "Cantidad_Recibida": "Cant. recibida",
    }

    form_columns = (
        "ID_Orden_Proveedor",
        "ID_Insumo",
        "ID_Unidad",
        "Cantidad_Solicitada",
        "Cantidad_Recibida",
    )

    form_overrides = {
        "Cantidad_Solicitada": FloatField,
        "Cantidad_Recibida": FloatField,
    }

    def _cargar_choices(self, form):
        form.ID_Orden_Proveedor.choices = [
            (o.ID_Orden_Proveedor, f"#{o.ID_Orden_Proveedor}")
            for o in OrdenesProveedores.query.all()
        ]
        form.ID_Insumo.choices = [
            (i.ID_Insumo, i.Nombre_insumo) for i in Insumo.query.all()
        ]
        form.ID_Unidad.choices = [
            (u.ID_Unidad, u.Nombre) for u in Unidades_medida.query.all()
        ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._cargar_choices(form)
        return form

    def on_form_prefill(self, form, id):
        self._cargar_choices(form)
