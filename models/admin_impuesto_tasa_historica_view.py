from datetime import datetime, timedelta
import traceback

from mensajes_logs import logger_

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView


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

    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    # Este botón sirve para visualizar el listado general.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_tasa_historica_visualizar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_tasa_historica_visualizar", fecha)
            return "Error al visualizar el historial de tasas de impuestos.", 500