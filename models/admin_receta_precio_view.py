from datetime import timedelta

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from sqlalchemy import func
from sqlalchemy import inspect as sa_inspect

from models import db
from models.recetas_precio_historico_model import RecetaPrecioHistorico
from models.receta_model import Receta
from models.empleado_model import Empleado


class RecetaPrecioHistoricoAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = False

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

    def _col(self, model_cls, names):
        cols = {c.key for c in sa_inspect(model_cls).columns}
        for n in names:
            if n in cols:
                return getattr(model_cls, n)
        return None

    def _aplicar_filtro_sucursal(self, q):
        if not self._es_empleado():
            return q
        suc = self._empleado_sucursal()
        if not suc:
            return q.filter(False)

        suc_col = self._col(Receta, ("ID_sucursal", "id_sucursal", "SucursalID", "sucursal_id"))
        if suc_col is None:
            return q.filter(False)

        receta_pk = self._col(Receta, ("ID_Receta", "id_receta", "RecetaID"))
        hist_fk = self._col(RecetaPrecioHistorico, ("ID_Receta", "id_receta", "RecetaID"))
        if receta_pk is None or hist_fk is None:
            return q.filter(False)

        return q.join(Receta, receta_pk == hist_fk).filter(suc_col == int(suc))

    def get_query(self):
        return self._aplicar_filtro_sucursal(db.session.query(RecetaPrecioHistorico))

    def get_count_query(self):
        q = db.session.query(func.count(RecetaPrecioHistorico.ID_Receta_precio_historico))
        q = self._aplicar_filtro_sucursal(q.select_from(RecetaPrecioHistorico))
        return q

    def is_accessible(self):
        return self._es_empleado()

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))
