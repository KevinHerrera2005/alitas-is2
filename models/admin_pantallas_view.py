from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import SelectField
from sqlalchemy import text

from models.Pantallas_model import Pantallas
from models.permisos_mixin import PermisosAdminMixin


class PantallasAdmin(PermisosAdminMixin, ModelView):
    can_delete = False
    can_view_details = True
    accion_buscar = "buscar"
    accion_crear = "crear"
    accion_editar = "editar"
    accion_eliminar = "eliminar"
    accion_exportar_pdf = "exportar pdf"
    accion_exportar_excel = "exportar excel"

    column_list = ("Nombre", "url", "estado")
    column_labels = {
        "Nombre": "Nombre de la pantalla",
        "url": "Endpoint",
        "estado": "Estado",
    }
    column_searchable_list = ("Nombre", "url")
    column_default_sort = ("ID_Pantalla", True)

    form_columns = ("Nombre", "url", "estado")

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
            "id": "pantalla_nombre",
        },
        "url": {
            "id": "pantalla_url",
        },
        "estado": {
            "id": "pantalla_estado",
        },
    }

    def update_model(self, form, model):
        from models import db
        try:
            nuevo_estado = 1 if str(form.estado.data).strip() == "1" else 0
            form.populate_obj(model)
            model.Nombre = (form.Nombre.data or "").strip()
            model.url = (form.url.data or "").strip()
            model.estado = nuevo_estado
            db.session.flush()
            db.session.execute(
                text("UPDATE Pantallas SET estado = :e WHERE ID_Pantalla = :id"),
                {"e": nuevo_estado, "id": model.ID_Pantalla}
            )
            db.session.commit()
            db.session.expire(model)
        except Exception as ex:
            db.session.rollback()
            flash(f"Error al actualizar la pantalla: {ex}", "error")
            return False
        self.after_model_change(form, model, False)
        return True

    def on_model_change(self, form, model, is_created):
        model.Nombre = (form.Nombre.data or "").strip()
        model.url = (form.url.data or "").strip()
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

