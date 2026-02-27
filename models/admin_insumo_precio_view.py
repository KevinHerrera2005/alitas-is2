from datetime import timedelta

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from sqlalchemy import inspect as sa_inspect

from models.insumo_precio_historico_model import InsumoPrecioHistorico
from models.insumo_model import Insumo
from models.empleado_model import Empleado


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
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    def _es_empleado(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def _empleado_id(self):
        if not current_user.is_authenticated:
            return None
        for attr in ("ID_Empleado", "id_empleado", "db_id", "id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass
        return None

    def _empleado_sucursal(self):
        if not current_user.is_authenticated:
            return None
        for attr in ("ID_sucursal", "id_sucursal", "sucursal_id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass
        emp_id = self._empleado_id()
        if emp_id is None:
            return None
        emp = Empleado.query.get(emp_id)
        if not emp:
            return None
        v = getattr(emp, "ID_sucursal", None) or getattr(emp, "id_sucursal", None)
        try:
            return int(v)
        except Exception:
            return None

    def _col_sucursal(self, model_cls):
        cols = {c.key for c in sa_inspect(model_cls).columns}
        for n in ("ID_sucursal", "id_sucursal", "SucursalID", "sucursal_id"):
            if n in cols:
                return getattr(model_cls, n)
        return None

    def _aplicar_filtro_sucursal(self, q):
        if not self._es_empleado():
            return q
        suc = self._empleado_sucursal()
        if not suc:
            return q.filter(False)
        suc_col = self._col_sucursal(Insumo)
        if suc_col is None:
            return q.filter(False)
        return q.join(Insumo, Insumo.ID_Insumo == InsumoPrecioHistorico.ID_Insumo).filter(suc_col == int(suc))

    def get_query(self):
        return self._aplicar_filtro_sucursal(super().get_query())

    def get_count_query(self):
        return self._aplicar_filtro_sucursal(super().get_count_query())

    def is_accessible(self):
        return self._es_empleado()

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))
