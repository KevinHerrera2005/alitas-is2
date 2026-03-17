from datetime import datetime
import traceback
from flask_admin import expose
from flask import flash, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import OperationalError

from mensajes_logs import logger_
from models.permisos_mixin import PermisosAdminMixin


class HistorialFacturasAdmin(PermisosAdminMixin, ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    accion_buscar         = "buscar"
    accion_exportar_pdf   = "exportar pdf"
    accion_exportar_excel = "exportar excel"

    can_view_details = True
    can_export = True

    column_list = (
        "ID_Parametro",
        "Numero_Factura",
        "Fecha_Emision",
        "ID_Usuario_ClienteF",
        "Subtotal",
        "Descuento",
        "Impuesto",
        "Total_a_pagar",
    )

    column_labels = {
        "ID_Parametro": "ID Factura",
        "Numero_Factura": "Número Factura",
        "Fecha_Emision": "Fecha emisión",
        "ID_Usuario_ClienteF": "Cliente",
        "Subtotal": "Subtotal",
        "Descuento": "Descuento",
        "Impuesto": "Impuesto",
        "Total_a_pagar": "Total a pagar",
    }

    column_default_sort = ("Fecha_Emision", True)

    column_searchable_list = ("Numero_Factura",)

    column_filters = (
        "Fecha_Emision",
        "ID_Usuario_ClienteF",
        "ID_Cai",
    )

    column_formatters = {
        "Fecha_Emision": lambda view, context, model, name: (
            model.Fecha_Emision.strftime("%d/%m/%Y")
            if getattr(model, "Fecha_Emision", None)
            else "—"
        ),
        "Subtotal": lambda view, context, model, name: (
            f"{getattr(model, 'Subtotal', 0):.2f}"
            if getattr(model, "Subtotal", None) is not None
            else "0.00"
        ),
        "Descuento": lambda view, context, model, name: (
            f"{getattr(model, 'Descuento', 0):.2f}"
            if getattr(model, "Descuento", None) is not None
            else "0.00"
        ),
        "Impuesto": lambda view, context, model, name: (
            f"{getattr(model, 'Impuesto', 0):.2f}"
            if getattr(model, "Impuesto", None) is not None
            else "0.00"
        ),
        "Total_a_pagar": lambda view, context, model, name: (
            f"{getattr(model, 'Total_a_pagar', 0):.2f}"
            if getattr(model, "Total_a_pagar", None) is not None
            else "0.00"
        ),
        "ID_Usuario_ClienteF": lambda view, context, model, name: (
            getattr(getattr(model, "cliente", None), "Username", "-")
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
            logger_.Logger.add_to_log("error", str(error), "facturas", fecha)
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "facturas", fecha
            )
            return "esto es un error", 501

    @expose("/details/")
    def details_view(self, *args, **kwargs):
        try:
            return super().details_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "facturas_detalle", fecha)
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "facturas_detalle", fecha
            )
            return "esto es un error", 501

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    def handle_view_exception(self, exc):
        if isinstance(exc, OperationalError):
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log(
                "error", str(exc), "historial_facturas_visualizar", fecha
            )
            logger_.Logger.add_to_log(
                "error", traceback.format_exc(), "historial_facturas_visualizar", fecha
            )
            flash(
                "No hay conexión con SQL Server. Enciende la base de datos e intenta de nuevo.",
                "error",
            )
            return redirect(request.referrer or url_for(".index_view"))
        return super().handle_view_exception(exc)
