from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import SelectField

from models.Acciones_model import Acciones
from models.permisos_mixin import PermisosAdminMixin


class AccionesAdmin(PermisosAdminMixin, ModelView):
    can_delete = False
    can_view_details = False
    accion_buscar = "buscar"
    accion_crear = "crear"
    accion_editar = "editar"
    accion_eliminar = "eliminar"
    accion_exportar_pdf = "exportar pdf"
    accion_exportar_excel = "exportar excel"

    column_list = ("Nombre", "estado")
    column_labels = {
        "Nombre": "Nombre de la acción",
        "estado": "Estado",
    }
    column_searchable_list = ("Nombre",)
    column_default_sort = ("ID_Accion", True)

    form_columns = ("Nombre", "estado")

    form_overrides = {
        "estado": SelectField,
    }

    form_args = {
        "estado": {
            "label": "Estado",
            "choices": [("1", "Activo"), ("0", "Inactivo")],
            "coerce": str,
        }
    }

    form_widget_args = {
        "Nombre": {
            "data-validacion": "nombre",
            "id": "accion_nombre",
        },
        "estado": {
            "id": "accion_estado",
        },
    }

    def is_visible(self):
        return False

    def on_model_change(self, form, model, is_created):
        model.Nombre = (form.Nombre.data or "").strip()
        model.estado = 1 if str(form.estado.data).strip() == "1" else 0

    def create_form(self, obj=None):
        form = super().create_form(obj)
        if hasattr(form, "estado"):
            form.estado.data = "1"
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if hasattr(form, "estado") and obj is not None:
            form.estado.data = "1" if obj.estado == 1 else "0"
        return form

