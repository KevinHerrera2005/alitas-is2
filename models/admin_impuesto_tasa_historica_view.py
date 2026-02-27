from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from datetime import timedelta  


class ImpuestoTasaHistoricaAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

    can_view_details = True
    can_export = True

    column_list = (
        "ID_Impuesto_historico",
        "nombre_impuesto",
        "fecha_inicio",
        "fecha_fin",
        "tasa",
    )

    column_labels = {
        "ID_Impuesto_historico": "ID Histórico",
        "nombre_impuesto": "Impuesto",
        "fecha_inicio": "Fecha inicio",
        "fecha_fin": "Fecha fin",
        "tasa": "Tasa",
    }

    column_default_sort = ("fecha_inicio", True)
    column_filters = ("ID_Impuesto", "fecha_inicio", "fecha_fin")

    column_formatters = {
        "fecha_inicio": lambda view, context, model, name: (
            model.fecha_inicio.strftime("%d/%m/%Y")
            if getattr(model, "fecha_inicio", None)
            else "—"
        ),
        "fecha_fin": lambda view, context, model, name: (
            (getattr(model, "fecha_fin") + timedelta(days=1)).strftime("%d/%m/%Y")
            if getattr(model, "fecha_fin", None)
            else "—"
        ),
    }
    
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)
    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))
