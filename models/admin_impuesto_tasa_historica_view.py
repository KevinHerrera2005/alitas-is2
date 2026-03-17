from datetime import datetime, timedelta
import traceback
from flask_admin import expose
from flask import flash, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.exc import OperationalError

from mensajes_logs import logger_


class ImpuestoTasaHistoricaAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    puede_exportar_pdf   = False
    puede_exportar_excel = False

    def is_accessible(self):
        from models.permisos_mixin import endpoint_accesible
        if not current_user.is_authenticated:
            return False
        if getattr(current_user, "tipo", None) != "empleado":
            return False
        return endpoint_accesible("impuesto_tasa_historica_admin.index_view")

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))

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
            logger_.Logger.add_to_log("error", str(error), "impuesto_historial", fecha)
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "impuesto_historial", fecha
            )
            return "esto es un error", 501

    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"

    @expose("/details/")
    def details_view(self,*args,**kwargs):
        try:
            return super().details_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_tasa_detalle", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_tasa_detalle", fecha)
            return "esto es un error", 501

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    def handle_view_exception(self, exc):
        if isinstance(exc, OperationalError):
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(exc), "impuesto_tasa_historica_visualizar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_tasa_historica_visualizar", fecha)
            flash("No hay conexión con SQL Server. Enciende la base de datos e intenta de nuevo.", "error")
            return redirect(request.referrer or url_for(".index_view"))
        return super().handle_view_exception(exc)