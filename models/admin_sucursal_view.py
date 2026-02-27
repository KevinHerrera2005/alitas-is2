from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash, request
from wtforms import StringField, SelectField
from sqlalchemy import text

from models import db
from models.direccion_model import Direccion


class SucursalAdmin(ModelView):
    can_search = True
    column_searchable_list = ("Descripcion",)

    column_list = ("Descripcion", "ID_Direccion", "estado")
    column_default_sort = ("ID_sucursal", True)

    column_labels = {
        "Descripcion": "Descripción de la sucursal",
        "ID_Direccion": "Dirección",
        "DireccionTexto": "Dirección",
        "estado": "Estado",
    }

    form_columns = ("Descripcion", "DireccionTexto", "estado")

    form_extra_fields = {
        "DireccionTexto": StringField("Dirección"),
    }

    create_template = "admin/model/sucursal_create.html"
    edit_template = "admin/model/sucursal_edit.html"

    form_widget_args = {
        "Descripcion": {
            "data-validacion": "descripcion",
            "id": "suc_descripcion",
        },
        "DireccionTexto": {
            "data-validacion": "descripcion",
            "id": "suc_direccion",
        },
        "estado": {
            "id": "suc_estado",
        },
    }

    form_overrides = {
        "estado": SelectField,
    }

    def _direccion_label(self, id_dir):
        if not id_dir:
            return ""
        dir_obj = Direccion.query.get(id_dir)
        return dir_obj.Descripcion if dir_obj else ""

    column_formatters = {
        "ID_Direccion": lambda view, context, model, name: view._direccion_label(
            model.ID_Direccion
        )
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        if "estado" in form._fields:
            form._fields.pop("estado")
        return form
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    def edit_form(self, obj=None):
        form = super().edit_form(obj)

        if hasattr(form, "estado"):
            form.estado.choices = [("1", "Activa"), ("0", "Inactiva")]
            if request.method == "GET" and obj is not None:
                form.estado.data = "1" if obj.estado == 1 else "0"

        if obj and obj.ID_Direccion:
            dir_obj = Direccion.query.get(obj.ID_Direccion)
            if dir_obj:
                form.DireccionTexto.data = dir_obj.Descripcion

        return form

    def handle_view_exception(self, exc):
        flash(str(exc), "danger")
        return False

    def on_model_change(self, form, model, is_created):
        descripcion = (form.Descripcion.data or "").strip()
        descripcion = " ".join(descripcion.split())
        if not descripcion:
            raise ValueError("La descripción de la sucursal es obligatoria.")

        model.Descripcion = descripcion

        if is_created:
            model.estado = 1
        else:
            if hasattr(form, "estado"):
                valor = str(form.estado.data).strip()
                model.estado = 1 if valor == "1" else 0

        dir_texto = (form.DireccionTexto.data or "").strip()
        dir_texto = " ".join(dir_texto.split())
        if not dir_texto:
            raise ValueError("La dirección es obligatoria.")

        if is_created or not getattr(model, "ID_Direccion", None):
            with self.session.no_autoflush:
                result = self.session.execute(
                    text(
                        """
                        INSERT INTO Direcciones (descripcion)
                        OUTPUT INSERTED.ID_Direccion
                        VALUES (:desc)
                        """
                    ),
                    {"desc": dir_texto},
                )
                new_id = result.scalar()
            model.ID_Direccion = int(new_id)
        else:
            with self.session.no_autoflush:
                self.session.execute(
                    text(
                        """
                        UPDATE Direcciones
                        SET descripcion = :desc
                        WHERE ID_Direccion = :id
                        """
                    ),
                    {"desc": dir_texto, "id": model.ID_Direccion},
                )

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        tipo = getattr(current_user, "tipo", None)
        if tipo == "gerente":
            return True

        if tipo == "empleado":
            puesto = getattr(current_user, "id_puesto", None)
            if puesto is None:
                puesto = getattr(current_user, "ID_Puesto", None)
            try:
                puesto = int(puesto)
            except Exception:
                puesto = None
            return puesto == 16

        return False

    def is_visible(self):
        return self.is_accessible()

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))
