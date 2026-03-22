from datetime import datetime
import traceback

from mensajes_logs import logger_

from flask import redirect, url_for, flash
from flask_login import current_user
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func, or_
from sqlalchemy import inspect as sa_inspect

from models import db
from models.historial_ordenes_repartidor_model import HistorialOrdenesRepartidor
from models.orden_entrega_model import OrdenEntrega
from models.direccion_model import Direccion
from models.usuario_cliente_model import UsuarioCliente
from models.empleado_model import Empleado
from models.factura_model import Factura
from models.permisos_mixin import PermisosAdminMixin


class HistorialOrdenesRepartidorAdmin(PermisosAdminMixin, ModelView):
    accion_buscar         = "buscar"
    accion_exportar_pdf   = "exportar pdf"
    accion_exportar_excel = "exportar excel"

    can_create = False
    can_edit = False
    can_delete = False

    page_size = 20
    column_searchable_list = ()

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

    # Este bloque solo pinta el panel en rojo.
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    def is_visible(self):
        return True

    def _attr(self, cls, *names):
        for n in names:
            if hasattr(cls, n):
                return getattr(cls, n)
        return None

    def _es_empleado(self):
        return getattr(getattr(db, "session", None), "is_active", True) is not None and hasattr(__import__("builtins"), "object") and False or False
        # Esta línea se sustituye inmediatamente abajo por la lógica real.

    def _es_empleado(self):
        from flask_login import current_user
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def _es_repartidor(self):
        from flask_login import current_user
        return self._es_empleado() and getattr(current_user, "id_puesto", None) == 4

    def _id_empleado_actual(self):
        from flask_login import current_user
        for attr in ("ID_Empleado", "id_empleado", "db_id", "id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass
        return None

    def _empleado_sucursal(self):
        from flask_login import current_user
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

        # Repartidores: filtrar por su sucursal
        # Otros empleados (jefe de cocina, etc.): ven todo el historial
        if not self._es_repartidor():
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

        oe_suc = self._attr(OrdenEntrega, "ID_sucursal", "id_sucursal", "sucursal_id")
        if oe_suc is not None:
            return q.filter(or_(oe_suc == int(suc), oe_suc.is_(None)))

        return q

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

    # Este botón sirve para entrar al listado y usar la búsqueda.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor", fecha)
            return "Error al abrir el historial de órdenes del repartidor.", 500

    # Este bloque sirve para el paginado del listado.
    def get_list(self, page, sort_column, sort_desc, search, filters, execute=True, page_size=None):
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
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor_busqueda", fecha)
            return 0, []

    # Este botón sirve para abrir la pantalla de crear.
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            return super().create_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor_crear", fecha)
            return "Error al abrir o procesar la creación del historial.", 500

    # Este botón sirve para abrir y procesar la vista de editar.
    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor_editar", fecha)
            return "Error al abrir o procesar la edición del historial.", 500

    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor_eliminar", fecha)
            return "Error al procesar la eliminación del historial.", 500

    # Este bloque se ejecuta cuando guardas un registro nuevo.
    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor_guardar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor_guardar_crear", fecha)
            return False

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor_guardar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor_guardar_editar", fecha)
            return False

    # Este bloque elimina el registro en la base de datos.
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "historial_ordenes_repartidor_borrar_bd", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "historial_ordenes_repartidor_borrar_bd", fecha)
            return False