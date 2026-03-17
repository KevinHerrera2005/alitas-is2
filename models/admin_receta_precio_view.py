from datetime import timedelta, datetime
import traceback

from mensajes_logs import logger_

from flask import redirect, url_for, flash
from flask_login import current_user
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

from models.recetas_precio_historico_model import RecetaPrecioHistorico


class RecetaPrecioHistoricoAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = False
    puede_exportar_pdf = False
    puede_exportar_excel = False

    def is_accessible(self):
        from models.permisos_mixin import endpoint_accesible
        if not current_user.is_authenticated:
            return False
        if getattr(current_user, "tipo", None) != "empleado":
            return False
        return endpoint_accesible("receta_precio_historico_admin.index_view")

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))

    column_list = (
        "nombre_receta",
        "Costo",
        "Fecha_inicio",
        "Fecha_Fin",
    )

    column_labels = {
        "nombre_receta": "Receta",
        "Costo": "Costo",
        "Fecha_inicio": "Fecha inicio",
        "Fecha_Fin": "Fecha fin",
    }

    column_default_sort = ("ID_Receta_precio_historico", True)
    column_sortable_list = ("Costo", "Fecha_inicio", "Fecha_Fin")

    column_formatters = {
        "Costo": lambda view, context, model, name: (
            f"LPS. {model.Costo:,.2f}" if model.Costo is not None else "—"
        ),
        "Fecha_inicio": lambda view, context, model, name: (
            model.Fecha_inicio.strftime("%d/%m/%Y")
            if getattr(model, "Fecha_inicio", None)
            else "—"
        ),
        "Fecha_Fin": lambda view, context, model, name: (
            (getattr(model, "Fecha_Fin") + timedelta(days=1)).strftime("%d/%m/%Y")
            if getattr(model, "Fecha_Fin", None)
            else "—"
        ),
    }

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    def get_query(self):
        return super().get_query()

    def get_count_query(self):
        return super().get_count_query()

    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "receta_precio_historico_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "receta_precio_historico_busqueda", fecha)


