from datetime import timedelta, datetime
import traceback

from mensajes_logs import logger_

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

from models.insumo_precio_historico_model import InsumoPrecioHistorico


class InsumoPrecioHistoricoAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

    can_view_details = True
    can_export = True

    column_list = (
        "ID_Insumo_precio_historico",
        "nombre_insumo",
        "fecha_inicio",
        "fecha_fin",
        "Precio",
    )

    column_labels = {
        "ID_Insumo_precio_historico": "ID Histórico",
        "nombre_insumo": "Insumo",
        "fecha_inicio": "Fecha inicio",
        "fecha_fin": "Fecha fin",
        "Precio": "Precio (Lps)",
    }

    column_default_sort = ("fecha_inicio", True)
    column_filters = ("ID_Insumo", "fecha_inicio", "fecha_fin")

    column_formatters = {
        "Precio": lambda view, context, model, name: (
            f"LPS. {model.Precio:,.2f}" if model.Precio is not None else "—"
        ),
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

    # Este bloque solo pinta el panel en rojo.
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    # Este botón sirve para entrar al listado y usar la búsqueda.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_precio_historico_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_precio_historico_busqueda", fecha)

    # Este botón sirve para ver el detalle de un registro.
    @expose("/details/")
    def details_view(self):
        try:
            return super().details_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_precio_historico_detalle", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_precio_historico_detalle", fecha)

    # Este botón sirve para exportar el historial.
    @expose("/export/<export_type>/")
    def export(self, export_type):
        try:
            return super().export(export_type)
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_precio_historico_exportar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_precio_historico_exportar", fecha)
        
