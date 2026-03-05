import re
import traceback
from datetime import datetime
from mensajes_logs import logger_

from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin.base import expose
from flask import flash, request
from wtforms import SelectField
from sqlalchemy import func

from models import db
from models.empleado_model import Puesto


class PuestoAdmin(ModelView):
    create_template = "admin/model/empleado_create.html"
    edit_template = "admin/model/empleado_edit.html"

    def is_visible(self):
        return self.is_accessible()

    column_list = ("Nombre_Puesto", "estado")
    column_default_sort = ("ID_Puesto", True)
    page_size = 10
    column_searchable_list = ("Nombre_Puesto",)

    column_labels = {
        "Nombre_Puesto": "Nombre del puesto",
        "estado": "Estado",
    }

    column_choices = {
        "estado": [
            (1, "Activo"),
            (0, "Inactivo"),
        ]
    }

    form_columns = ("Nombre_Puesto", "estado")

    form_widget_args = {
        "Nombre_Puesto": {
            "data-validacion": "nombre",
            "id": "puesto_nombre",
        },
        "estado": {
            "id": "puesto_estado",
        },
    }

    form_overrides = {
        "estado": SelectField,
    }

    def get_list(
        self,
        page,
        sort_column,
        sort_desc,
        search,
        filters,
        execute=True,
        page_size=None,
    ):
        try:
            return super().get_list(
                page,
                sort_column,
                sort_desc,
                search,
                filters,
                execute=execute,
                page_size=page_size,
            )
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "puesto_pantalla", fecha)
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "puesto_pantalla", fecha
            )
            return "esto es un error", 501

    def create_form(self, obj=None):
        try:
            form = super().create_form(obj)
            if "estado" in form._fields:
                form._fields.pop("estado")
            return form
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "puesto_pantalla", fecha)
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "puesto_pantalla", fecha
            )
            return "esto es un error", 501

    def edit_form(self, obj=None):
        try:
            form = super().edit_form(obj)
            if hasattr(form, "estado"):
                form.estado.choices = [("1", "Activo"), ("0", "Inactivo")]
                if request.method == "GET" and obj is not None:
                    form.estado.data = "1" if obj.estado == 1 else "0"
            return form
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "puesto_pantalla", fecha)
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "puesto_pantalla", fecha
            )
            return "esto es un error", 501

    def on_model_change(self, form, model, is_created):
        nombre = (form.Nombre_Puesto.data or "").strip()

        if not nombre:
            raise ValueError("El nombre del puesto es obligatorio.")
        if len(nombre) < 3:
            raise ValueError("El nombre del puesto debe tener al menos 3 caracteres.")

        with db.session.no_autoflush:
            q = Puesto.query.filter(
                func.lower(Puesto.Nombre_Puesto) == func.lower(nombre)
            )
            if not is_created and getattr(model, "ID_Puesto", None):
                q = q.filter(Puesto.ID_Puesto != model.ID_Puesto)
            if q.first():
                raise ValueError("Ya existe un puesto con ese nombre.")

        model.Nombre_Puesto = nombre

        if is_created:
            model.estado = 1
        else:
            if hasattr(form, "estado"):
                model.estado = 1 if str(form.estado.data).strip() == "1" else 0

    def handle_view_exception(self, exc):
        if isinstance(exc, ValueError):
            flash(str(exc), "danger")
            return True

        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(exc), "puesto_pantalla", fecha)
        logger_.Logger.add_to_log(
            "error", traceback.format_exc(), "puesto_pantalla", fecha
        )
        flash("esto es un error", "danger")
        return True

    @action("activar", "Activar seleccionados", "¿Activar los puestos seleccionados?")
    def action_activar(self, ids):
        try:
            self.session.query(Puesto).filter(Puesto.ID_Puesto.in_(ids)).update(
                {"estado": 1}, synchronize_session=False
            )
            self.session.commit()
            flash("Puestos activados.", "success")
        except Exception:
            self.session.rollback()
            flash("No se pudo activar.", "danger")

    @action(
        "inactivar", "Inactivar seleccionados", "¿Inactivar los puestos seleccionados?"
    )
    def action_inactivar(self, ids):
        try:
            self.session.query(Puesto).filter(Puesto.ID_Puesto.in_(ids)).update(
                {"estado": 0}, synchronize_session=False
            )
            self.session.commit()
            flash("Puestos inactivados.", "success")
        except Exception:
            self.session.rollback()
            flash("No se pudo inactivar.", "danger")

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    @expose("/")
    def index_view(self, *args, **kwargs):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "puesto_pantalla", fecha)
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "puesto_pantalla", fecha
            )
            return "esto es un error", 501


def _normalizar_texto(raw):
    if raw is None:
        return None
    out = " ".join(str(raw).strip().split())
    return out or None


def validar_nombre_puesto(raw, min_len=3, max_len=40):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if len(out) < int(min_len) or len(out) > int(max_len):
        return None
    if re.search(r"(.)\1\1", out.lower()):
        return None
    return out
