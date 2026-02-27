from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import SelectField

from models import db
from models.unidades_medida_model import Unidades_medida


class UnidadesMedidaAdmin(ModelView):
    create_template = "admin/model/unidad_create.html"
    edit_template = "admin/model/unidad_edit.html"

    can_search = True
    column_searchable_list = ("Nombre", "abreviatura")

    column_list = ("Nombre", "abreviatura", "Tipo")
    column_labels = {
        "Nombre": "Nombre de la unidad",
        "abreviatura": "Abreviatura",
        "Tipo": "Tipo",
    }
    column_default_sort = ("ID_Unidad", True)

    form_columns = ("Nombre", "abreviatura", "Tipo")

    form_widget_args = {
        "Nombre": {
            "data-validacion": "nombre",
            "id": "unidad_nombre",
        },
        "abreviatura": {
            "data-validacion": "abreviatura",
            "id": "unidad_abreviatura",
        },
        "Tipo": {
            "data-validacion": "numero_positivo",
            "id": "unidad_tipo",
        },
    }

    form_overrides = {
        "Tipo": SelectField,
    }

    form_args = {
        "Tipo": {
            "choices": [
                ("1", "1 - Peso"),
                ("2", "2 - Volumen"),
                ("3", "3 - Unidad"),
            ]
        }
    }
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "tipo", None) == "empleado"
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))

    def handle_view_exception(self, exc):
        flash(str(exc), "danger")
        return False

    def on_model_change(self, form, model, is_created):
        nombre = (form.Nombre.data or "").strip()
        abrev = (form.abreviatura.data or "").strip()
        tipo_raw = str(form.Tipo.data).strip() if form.Tipo.data is not None else ""

        if not nombre:
            raise ValueError("El nombre de la unidad es obligatorio.")

        if not abrev:
            raise ValueError("La abreviatura es obligatoria.")

        if not tipo_raw:
            raise ValueError("El tipo es obligatorio.")

        try:
            tipo_int = int(tipo_raw)
        except ValueError:
            raise ValueError("El tipo debe ser un número entero.")

        abrev = abrev.upper()

        with db.session.no_autoflush:
            q_nombre = Unidades_medida.query.filter(
                db.func.lower(Unidades_medida.Nombre) == nombre.lower()
            )

            if not is_created and getattr(model, "ID_Unidad", None) is not None:
                q_nombre = q_nombre.filter(
                    Unidades_medida.ID_Unidad != model.ID_Unidad
                )

            if q_nombre.first():
                raise ValueError("Ya existe una unidad con ese nombre.")

            q_abrev = Unidades_medida.query.filter(
                db.func.lower(Unidades_medida.abreviatura) == abrev.lower()
            )

            if not is_created and getattr(model, "ID_Unidad", None) is not None:
                q_abrev = q_abrev.filter(
                    Unidades_medida.ID_Unidad != model.ID_Unidad
                )

            if q_abrev.first():
                raise ValueError("Ya existe una unidad con esa abreviatura.")

        model.Nombre = nombre
        model.abreviatura = abrev
        model.Tipo = tipo_int
