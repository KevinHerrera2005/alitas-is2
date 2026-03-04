from datetime import datetime
import traceback

from mensajes_logs import logger_

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, FloatField

from models import db
from models.ordenes_proveedores_model import (
    OrdenesProveedores,
    OrdenesProveedoresDetalle,
)
from models.proveedores_model import Proveedor
from models.empleado_model import Empleado
from models.sucursal_model import Sucursal
from models.insumo_model import Insumo
from models.unidades_medida_model import Unidades_medida


class SecureModelView(ModelView):
    pass


class OrdenesProveedoresAdmin(SecureModelView):
    column_list = (
        "ID_Orden_Proveedor",
        "Fecha_Inicio",
        "Fecha_Estimada",
        "Fecha_Entregado",
        "Estado",
        "proveedor",
        "empleado",
        "sucursal",
        "Comentarios",
    )

    column_labels = {
        "ID_Orden_Proveedor": "ID",
        "Fecha_Inicio": "Fecha inicio",
        "Fecha_Estimada": "Fecha estimada",
        "Fecha_Entregado": "Fecha entregado",
        "Estado": "Estado",
        "proveedor": "Proveedor",
        "empleado": "Encargado",
        "sucursal": "Sucursal",
        "Comentarios": "Comentarios",
    }

    form_columns = (
        "ID_Proveedor",
        "ID_Empleado_Encargado",
        "ID_Sucursal",
        "Fecha_Inicio",
        "Fecha_Estimada",
        "Fecha_Entregado",
        "Estado",
        "Comentarios",
    )

    form_overrides = {
        "Estado": SelectField,
    }

    def _cargar_choices(self, form):
        form.Estado.choices = [
            ("0", "Pendiente"),
            ("1", "Enviada"),
            ("2", "Entregada"),
            ("3", "Cancelada"),
        ]
        form.ID_Proveedor.choices = [
            (p.ID_Proveedor, p.Nombre_Proveedor) for p in Proveedor.query.all()
        ]
        form.ID_Empleado_Encargado.choices = [
            (e.ID_Empleado, e.Nombre) for e in Empleado.query.all()
        ]
        form.ID_Sucursal.choices = [
            (s.ID_sucursal, s.Descripcion) for s in Sucursal.query.all()
        ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._cargar_choices(form)
        form.Estado.data = "0"
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._cargar_choices(form)
        if obj is not None:
            form.Estado.data = str(obj.Estado)
        return form

    # Este botón sirve para entrar al listado y usar la búsqueda.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_busqueda", fecha)
            return "Error al abrir el listado de órdenes de proveedores.", 500

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
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_paginado", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_paginado", fecha)
            return 0, []

    # Este botón sirve para abrir la pantalla de crear.
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            return super().create_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_crear", fecha)
            return "Error al abrir o procesar la creación de la orden.", 500

    # Este botón sirve para abrir y procesar la vista de editar.
    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_editar", fecha)
            return "Error al abrir o procesar la edición de la orden.", 500

    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_eliminar", fecha)
            return "Error al procesar la eliminación de la orden.", 500

    # Este bloque se ejecuta cuando guardas una orden nueva.
    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_guardar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_guardar_crear", fecha)
            return False

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_guardar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_guardar_editar", fecha)
            return False

    # Este bloque elimina el registro en la base de datos.
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_borrar_bd", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_borrar_bd", fecha)
            return False


class OrdenesProveedoresDetalleAdmin(SecureModelView):
    column_list = (
        "ID_Detalle",
        "orden",
        "insumo",
        "unidad",
        "Cantidad_Solicitada",
        "Cantidad_Recibida",
    )

    column_labels = {
        "ID_Detalle": "ID",
        "orden": "Orden",
        "insumo": "Insumo",
        "unidad": "Unidad",
        "Cantidad_Solicitada": "Cant. solicitada",
        "Cantidad_Recibida": "Cant. recibida",
    }

    form_columns = (
        "ID_Orden_Proveedor",
        "ID_Insumo",
        "ID_Unidad",
        "Cantidad_Solicitada",
        "Cantidad_Recibida",
    )

    form_overrides = {
        "Cantidad_Solicitada": FloatField,
        "Cantidad_Recibida": FloatField,
    }

    def _cargar_choices(self, form):
        form.ID_Orden_Proveedor.choices = [
            (o.ID_Orden_Proveedor, f"#{o.ID_Orden_Proveedor}")
            for o in OrdenesProveedores.query.all()
        ]
        form.ID_Insumo.choices = [
            (i.ID_Insumo, i.Nombre_insumo) for i in Insumo.query.all()
        ]
        form.ID_Unidad.choices = [
            (u.ID_Unidad, u.Nombre) for u in Unidades_medida.query.all()
        ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._cargar_choices(form)
        return form

    def on_form_prefill(self, form, id):
        self._cargar_choices(form)

    # Este botón sirve para entrar al listado y usar la búsqueda.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_busqueda", fecha)
            return "Error al abrir el listado de detalles de órdenes de proveedores.", 500

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
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_paginado", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_paginado", fecha)
            return 0, []

    # Este botón sirve para abrir la pantalla de crear.
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            return super().create_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_crear", fecha)
            return "Error al abrir o procesar la creación del detalle.", 500

    # Este botón sirve para abrir y procesar la vista de editar.
    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_editar", fecha)
            return "Error al abrir o procesar la edición del detalle.", 500

    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_eliminar", fecha)
            return "Error al procesar la eliminación del detalle.", 500

    # Este bloque se ejecuta cuando guardas un detalle nuevo.
    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_guardar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_guardar_crear", fecha)
            return False

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_guardar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_guardar_editar", fecha)
            return False

    # Este bloque elimina el registro en la base de datos.
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "ordenes_proveedores_detalle_borrar_bd", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "ordenes_proveedores_detalle_borrar_bd", fecha)
            return False