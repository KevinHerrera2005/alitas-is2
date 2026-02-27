from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import SelectField

from models import db
from models.empleado_model import Empleado
from models.tipo_documento_model import TipoDocumento
from models.empleado_documento_model import EmpleadoDocumento


class EmpleadoDocumentoAdmin(ModelView):
    can_create = True
    can_edit = False
    can_delete = True

    column_list = ("empleado", "tipo_documento")
    column_labels = {
        "empleado": "Empleado",
        "tipo_documento": "Documento",
    }

    form_columns = ("ID_Empleado", "tipo_doc")

    form_overrides = {
        "ID_Empleado": SelectField,
        "tipo_doc": SelectField,
    }

    def _build_empleado_choices(self):
        empleados = (
            Empleado.query.filter_by(estado=1)
            .order_by(Empleado.Nombre, Empleado.Apellido)
            .all()
        )
        return [(str(e.ID_Empleado), f"{e.Nombre} {e.Apellido}") for e in empleados]

    def _build_tipo_doc_choices(self):
        tipos = TipoDocumento.query.order_by(TipoDocumento.descripcion).all()

        def etiqueta(t):
            mapa = {1: "DNI", 2: "RTN", 3: "Pasaporte", 4: "Otro"}
            tipo_txt = mapa.get(t.tipo, "Desconocido")
            return f"{tipo_txt} - {t.numero_documento}"

        return [(str(t.tipo_doc), etiqueta(t)) for t in tipos]

    def create_form(self, obj=None):
        form = super().create_form(obj)

        if hasattr(form, "ID_Empleado"):
            form.ID_Empleado.choices = self._build_empleado_choices()

        if hasattr(form, "tipo_doc"):
            form.tipo_doc.choices = self._build_tipo_doc_choices()

        return form

    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "tipo", None) == "gerente"
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))
