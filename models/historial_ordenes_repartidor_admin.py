from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import flash, redirect, url_for
from sqlalchemy import func, or_
from sqlalchemy import inspect as sa_inspect

from models import db
from models.historial_ordenes_repartidor_model import HistorialOrdenesRepartidor
from models.orden_entrega_model import OrdenEntrega
from models.direccion_model import Direccion
from models.usuario_cliente_model import UsuarioCliente
from models.empleado_model import Empleado
from models.factura_model import Factura


class HistorialOrdenesRepartidorAdmin(ModelView):
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)
    can_create = False
    can_edit = False
    can_delete = False

    page_size = 20
    can_search = True
    column_searchable_list = ("ID_Orden",)

    column_list = (
        "ID_Orden",
        "Numero_Factura_col",
        "Cliente_col",
        "Fecha_Creacion_col",
        "direccion_col",
        "Estado_Final",
        "Fecha_Finalizacion",
        "Motivo_Cancelacion_col",
    )

    column_labels = {
        "ID_Orden": "Orden",
        "Numero_Factura_col": "Número factura",
        "Cliente_col": "Cliente",
        "Fecha_Creacion_col": "Fecha creación",
        "direccion_col": "Dirección",
        "Estado_Final": "Estado final",
        "Fecha_Finalizacion": "Fecha finalización",
        "Motivo_Cancelacion_col": "Motivo de cancelación",
    }

    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))

    def _attr(self, cls, *names):
        for n in names:
            if hasattr(cls, n):
                return getattr(cls, n)
        return None

    def _es_empleado(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def _es_repartidor(self):
        return self._es_empleado() and getattr(current_user, "id_puesto", None) == 4

    def _id_empleado_actual(self):
        for attr in ("ID_Empleado", "id_empleado", "db_id", "id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass
        return None

    def _empleado_sucursal(self):
        for attr in ("ID_sucursal", "id_sucursal", "sucursal_id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass

        emp_id = self._id_empleado_actual()
        if emp_id is None:
            return None

        emp = Empleado.query.get(int(emp_id))
        if not emp:
            return None

        v = getattr(emp, "ID_sucursal", None) or getattr(emp, "id_sucursal", None) or getattr(emp, "sucursal_id", None)
        try:
            return int(v)
        except Exception:
            return None

    def _oe_cache(self):
        cache = getattr(self, "_cache_oe", None)
        if cache is None:
            cache = {}
            setattr(self, "_cache_oe", cache)
        if len(cache) > 600:
            cache.clear()
        return cache

    def _fac_cache(self):
        cache = getattr(self, "_cache_fac", None)
        if cache is None:
            cache = {}
            setattr(self, "_cache_fac", cache)
        if len(cache) > 600:
            cache.clear()
        return cache

    def _dir_cache(self):
        cache = getattr(self, "_cache_dir", None)
        if cache is None:
            cache = {}
            setattr(self, "_cache_dir", cache)
        if len(cache) > 600:
            cache.clear()
        return cache

    def _hist_oid_col(self):
        return self._attr(HistorialOrdenesRepartidor, "ID_Orden", "id_orden", "orden_id", "OrdenID")

    def _hist_rep_col(self):
        return self._attr(HistorialOrdenesRepartidor, "ID_Repartidor", "id_repartidor", "repartidor_id", "RepartidorID")

    def _orden_id_cols(self):
        cols = []
        for n in (
            "ID_Orden_Entrega",
            "id_orden_entrega",
            "orden_entrega_id",
            "ID_Parametro",
            "id_parametro",
            "parametro_id",
            "ID_Orden",
            "id_orden",
            "orden_id",
        ):
            c = self._attr(OrdenEntrega, n)
            if c is not None:
                cols.append(c)
        return cols

    def _orden_de_hist(self, hist_model):
        oid = getattr(hist_model, "ID_Orden", None)
        if oid is None:
            return None
        try:
            oid = int(oid)
        except Exception:
            return None

        cache = self._oe_cache()
        if oid in cache:
            return cache[oid]

        orden = None
        try:
            orden = db.session.get(OrdenEntrega, oid)
        except Exception:
            orden = None

        if orden is None:
            cand = self._orden_id_cols()
            if cand:
                try:
                    orden = db.session.query(OrdenEntrega).filter(or_(*[c == oid for c in cand])).first()
                except Exception:
                    orden = None

        cache[oid] = orden
        return orden

    def _factura_de_hist(self, hist_model):
        oid = getattr(hist_model, "ID_Orden", None)
        if oid is None:
            return None
        try:
            oid = int(oid)
        except Exception:
            return None

        cache = self._fac_cache()
        if oid in cache:
            return cache[oid]

        fac = None
        try:
            fac = db.session.get(Factura, oid)
        except Exception:
            fac = None

        if fac is None:
            try:
                fac = db.session.query(Factura).filter(Factura.ID_Parametro == oid).first()
            except Exception:
                fac = None

        cache[oid] = fac
        return fac

    def _estado_label(self, v):
        m = {3: "Entregada", 4: "Cancelada"}
        try:
            return m.get(int(v), str(v))
        except Exception:
            return str(v)

    def _nombre_apellido(self, obj):
        if not obj:
            return ""
        nombre = getattr(obj, "nombre", None) or getattr(obj, "Nombre", None) or getattr(obj, "Nombres", None) or ""
        apellido = getattr(obj, "apellido", None) or getattr(obj, "Apellido", None) or getattr(obj, "Apellidos", None) or ""
        return (str(nombre) + " " + str(apellido)).strip()

    def _format_numero_factura(self, hist_model):
        orden = self._orden_de_hist(hist_model)
        if orden:
            nf = getattr(orden, "Numero_Factura", None) or getattr(orden, "numero_factura", None)
            if nf:
                return str(nf)

        fac = self._factura_de_hist(hist_model)
        if fac:
            nf = getattr(fac, "Numero_Factura", None) or getattr(fac, "numero_factura", None)
            if nf:
                return str(nf)

        return ""

    def _format_cliente(self, hist_model):
        orden = self._orden_de_hist(hist_model)
        if orden:
            txt = self._nombre_apellido(orden)
            if txt:
                return txt

        fac = self._factura_de_hist(hist_model)
        if fac:
            cli = getattr(fac, "cliente", None)
            txt = self._nombre_apellido(cli)
            if txt:
                return txt

        return ""

    def _format_fecha_creacion(self, hist_model):
        orden = self._orden_de_hist(hist_model)
        dt = None
        if orden:
            dt = getattr(orden, "Fecha_Creacion", None) or getattr(orden, "fecha_creacion", None)

        if dt is None:
            fac = self._factura_de_hist(hist_model)
            if fac:
                dt = getattr(fac, "Fecha_Emision", None) or getattr(fac, "fecha_emision", None)

        if not dt:
            return ""
        try:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return str(dt)

    def _format_direccion(self, hist_model):
        orden = self._orden_de_hist(hist_model)
        if not orden:
            return ""

        dtxt = getattr(orden, "descripcion", None) or getattr(orden, "Descripcion", None) or ""
        if dtxt:
            return str(dtxt)

        dir_id = getattr(orden, "ID_Direccion", None) or getattr(orden, "id_direccion", None)
        if not dir_id:
            return ""

        try:
            dir_id = int(dir_id)
        except Exception:
            return ""

        cache = self._dir_cache()
        if dir_id in cache:
            return cache[dir_id]

        d = None
        try:
            d = Direccion.query.get(dir_id)
        except Exception:
            d = None

        res = ""
        if d:
            res = getattr(d, "Descripcion", None) or getattr(d, "descripcion", None) or ""
            res = str(res) if res else ""

        cache[dir_id] = res
        return res

    def _format_motivo_cancelacion(self, hist_model):
        orden = self._orden_de_hist(hist_model)
        if orden:
            mot = getattr(orden, "Motivo_Cancelacion", None) or getattr(orden, "motivo_cancelacion", None)
            if mot:
                return str(mot)

        mot2 = getattr(hist_model, "Observacion", None) or getattr(hist_model, "observacion", None) or ""
        return str(mot2) if mot2 else ""

    column_formatters = {
        "Estado_Final": lambda view, context, model, name: view._estado_label(getattr(model, "Estado_Final", None)),
        "Numero_Factura_col": lambda view, context, model, name: view._format_numero_factura(model),
        "Cliente_col": lambda view, context, model, name: view._format_cliente(model),
        "Fecha_Creacion_col": lambda view, context, model, name: view._format_fecha_creacion(model),
        "direccion_col": lambda view, context, model, name: view._format_direccion(model),
        "Motivo_Cancelacion_col": lambda view, context, model, name: view._format_motivo_cancelacion(model),
    }

    def _aplicar_filtro_sucursal(self, q):
        if not self._es_empleado():
            return q

        suc = self._empleado_sucursal()
        if not suc:
            return q.filter(False)

        hist_oid = self._hist_oid_col()
        if hist_oid is None:
            return q.filter(False)

        orden_cols = self._orden_id_cols()
        if orden_cols:
            q = q.outerjoin(OrdenEntrega, or_(*[c == hist_oid for c in orden_cols]))

        q = q.outerjoin(Factura, Factura.ID_Parametro == hist_oid)

        uc_pk = self._attr(UsuarioCliente, "ID_Usuario_ClienteF", "id_usuario_cliente", "usuario_cliente_id", "Usuario_ClienteID")
        uc_suc = self._attr(UsuarioCliente, "ID_sucursal", "id_sucursal", "sucursal_id", "SucursalID")
        if uc_pk is None or uc_suc is None:
            return q.filter(False)

        ord_cliente_fk = self._attr(OrdenEntrega, "ID_Usuario_ClienteF", "id_usuario_cliente", "usuario_cliente_id", "Usuario_ClienteID")
        if ord_cliente_fk is not None:
            q = q.outerjoin(UsuarioCliente, uc_pk == func.coalesce(ord_cliente_fk, Factura.ID_Usuario_ClienteF))
        else:
            q = q.outerjoin(UsuarioCliente, uc_pk == Factura.ID_Usuario_ClienteF)

        return q.filter(uc_suc == int(suc))

    def get_query(self):
        q = super().get_query()
        q = self._aplicar_filtro_sucursal(q)

        if self._es_repartidor():
            rid = self._id_empleado_actual()
            rep_col = self._hist_rep_col()
            if rid is None or rep_col is None:
                return q.filter(False)
            q = q.filter(rep_col == int(rid))

        return q.distinct()

    def get_count_query(self):
        q = self.get_query()
        pk = None
        try:
            pks = sa_inspect(HistorialOrdenesRepartidor).primary_key
            if pks:
                pk = pks[0]
        except Exception:
            pk = None

        if pk is None:
            pk = self._hist_oid_col()

        return q.with_entities(func.count(func.distinct(pk))).order_by(None)
