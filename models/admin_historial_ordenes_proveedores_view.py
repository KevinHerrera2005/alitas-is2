from flask import flash, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))


class HistorialOrdenesProveedoresAdmin(SecureModelView):
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

    def get_query(self):
        return super().get_query().filter(self.model.Estado.in_([2, 3]))

    def get_count_query(self):
        return super().get_count_query().filter(self.model.Estado.in_([2, 3]))
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)
    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"

    def _estado_label(self, v):
        m = {0: "Pendiente", 1: "Enviada", 2: "Entregada", 3: "Cancelada"}
        try:
            return m.get(int(v), str(v))
        except Exception:
            return str(v)

    column_formatters = {
        "proveedor": lambda v, c, m, p: (
            getattr(m.proveedor, "Nombre_Proveedor", None)
            or getattr(m.proveedor, "Nombre", None)
            or ""
        )
        if getattr(m, "proveedor", None) is not None
        else "",
        "sucursal": lambda v, c, m, p: (
            getattr(m.sucursal, "Descripcion", None) or ""
        )
        if getattr(m, "sucursal", None) is not None
        else "",
        "Estado": lambda v, c, m, p: HistorialOrdenesProveedoresAdmin._estado_label(
            HistorialOrdenesProveedoresAdmin, m.Estado
        ),
    }
