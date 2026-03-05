import traceback
from datetime import datetime

from flask import Response, session
from flask_admin.base import expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import DBAPIError, OperationalError

from mensajes_logs import logger_


class HistorialOrdenesProveedoresAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_list = (
        "ID_Orden_Proveedor",
        "Fecha_Inicio",
        "proveedor",
        "sucursal",
        "Estado",
        "Numero_Factura",
        "Comentarios",
    )

    column_labels = {
        "ID_Orden_Proveedor": "ID",
        "Fecha_Inicio": "Fecha inicio",
        "Fecha_Estimada": "Fecha estimada",
        "Fecha_Entregado": "Fecha entregado",
        "Estado": "Estado",
        "Numero_Factura": "Número de factura",
        "Comentarios": "Comentarios",
        "proveedor": "Proveedor",
        "sucursal": "Sucursal",
    }

    column_default_sort = ("ID_Orden_Proveedor", True)
    page_size = 20

    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"

    def _log_error(self, error, tag):
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), tag, fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), tag, fecha)

    def _solo_error_response(self):
        session.pop("_flashes", None)
        return Response(
            "Esto es un error", status=200, mimetype="text/plain; charset=utf-8"
        )

    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except (OperationalError, DBAPIError) as error:
            self._log_error(error, "historial_ordenes_proveedores_db")
            return self._solo_error_response()
        except Exception as error:
            self._log_error(error, "historial_ordenes_proveedores_index")
            raise

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
        except (OperationalError, DBAPIError) as error:
            self._log_error(error, "historial_ordenes_proveedores_db")
            raise
        except Exception as error:
            self._log_error(error, "historial_ordenes_proveedores_get_list")
            raise

    def get_query(self):
        return super().get_query().filter(self.model.Estado.in_([2, 3]))

    def get_count_query(self):
        return super().get_count_query().filter(self.model.Estado.in_([2, 3]))

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    @expose("/details/")
    def details_view(self):
        try:
            return super().details_view()
        except (OperationalError, DBAPIError) as error:
            self._log_error(error, "historial_ordenes_proveedores_db")
            return self._solo_error_response()
        except Exception as error:
            self._log_error(error, "historial_ordenes_proveedores_details")
            raise

    def _estado_label(self, v):
        m = {0: "Pendiente", 1: "Enviada", 2: "Entregada", 3: "Cancelada"}
        try:
            return m.get(int(v), str(v))
        except Exception:
            return str(v)

    column_formatters = {
        "proveedor": lambda v, c, m, p: (
            (
                getattr(m.proveedor, "Nombre_Proveedor", None)
                or getattr(m.proveedor, "Nombre", None)
                or ""
            )
            if getattr(m, "proveedor", None) is not None
            else ""
        ),
        "sucursal": lambda v, c, m, p: (
            (getattr(m.sucursal, "Descripcion", None) or "")
            if getattr(m, "sucursal", None) is not None
            else ""
        ),
        "Estado": lambda v, c, m, p: HistorialOrdenesProveedoresAdmin._estado_label(
            HistorialOrdenesProveedoresAdmin, m.Estado
        ),
    }
