from datetime import datetime
import traceback

from mensajes_logs import logger_

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for
from flask_login import current_user
from models.cai_historico_model import CAIHistorico
from models.sucursal_model import Sucursal


class CAIHistoricoAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True
    puede_exportar_pdf   = True
    puede_exportar_excel = True

    def is_accessible(self):
        from models.permisos_mixin import endpoint_accesible
        if not current_user.is_authenticated:
            return False
        if getattr(current_user, "tipo", None) != "empleado":
            return False
        return endpoint_accesible("cai_historico.index_view")

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))

    column_default_sort = ("Fecha_Registro", True)

    column_list = (
        "Fecha_Registro",
        "ID_Cai",
        "Fecha_Emision",
        "Fecha_Final",
        "Rango_Inicial",
        "Rango_Final",
        "Secuencia",
        "estado",
        "ID_sucursal",
    )

    column_labels = {
        "Fecha_Registro": "Fecha de registro",
        "ID_Cai": "ID CAI",
        "Fecha_Emision": "Fecha de emisión",
        "Fecha_Final": "Fecha final",
        "Rango_Inicial": "Rango inicial",
        "Rango_Final": "Rango final",
        "Secuencia": "Secuencia",
        "estado": "Estado",
        "ID_sucursal": "Sucursal",
    }

    column_formatters = {
        "Fecha_Registro": lambda v, c, m, p: (
            m.Fecha_Registro.strftime("%Y-%m-%d") if m.Fecha_Registro else ""
        ),
        "estado": lambda v, c, m, p: "Activo" if m.estado == 1 else "Inactivo",
        "ID_sucursal": lambda v, c, m, p: (
            (Sucursal.query.get(m.ID_sucursal).Descripcion)
            if Sucursal.query.get(m.ID_sucursal)
            else m.ID_sucursal
        ),
    }

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    # Este botón sirve para entrar al listado y visualizar el historial.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "cai_historico_visualizar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_visualizar", fecha)
            return "Error al visualizar el historial de CAI.", 500

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
            logger_.Logger.add_to_log("error", str(error), "cai_historico_paginado", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_paginado", fecha)
            return 0, []

    # Este botón sirve para ver el detalle de un registro.
    @expose("/details/")
    def details_view(self):
        try:
            return super().details_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "cai_historico_detalle", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_detalle", fecha)
            return "Error al visualizar el detalle del historial de CAI.", 500

    # Este botón sirve para abrir la pantalla de crear.
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            return super().create_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "cai_historico_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_crear", fecha)
            return "Error al abrir o procesar la creación del historial de CAI.", 500

    # Este botón sirve para abrir y procesar la vista de editar.
    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "cai_historico_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_editar", fecha)
            return "Error al abrir o procesar la edición del historial de CAI.", 500

    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "cai_historico_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_eliminar", fecha)
            return "Error al procesar la eliminación del historial de CAI.", 500

    # Este bloque se ejecuta cuando guardas un registro nuevo.
    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "cai_historico_guardar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_guardar_crear", fecha)
            return False

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "cai_historico_guardar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_guardar_editar", fecha)
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
            logger_.Logger.add_to_log("error", str(error), "cai_historico_borrar_bd", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "cai_historico_borrar_bd", fecha)
            return False