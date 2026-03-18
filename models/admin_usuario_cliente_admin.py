from datetime import datetime
import traceback

from mensajes_logs import logger_

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask import flash, request, session
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from models import db
from models.usuario_cliente_model import UsuarioCliente
from models.sucursal_model import Sucursal
from models.permisos_mixin import PermisosAdminMixin


class UsuarioClienteAdmin(PermisosAdminMixin, ModelView):
    accion_buscar         = "buscar"
    accion_crear          = "crear"
    accion_editar         = "editar"
    accion_eliminar       = "eliminar"
    accion_exportar_pdf   = "exportar pdf"
    accion_exportar_excel = "exportar excel"

    can_search = True
    column_searchable_list = ("Username", "nombre", "apellido", "correo")

    column_list = (
        "ID_Usuario_ClienteF",
        "Username",
        "nombre",
        "apellido",
        "telefono",
        "correo",
        "ID_sucursal",
        "estado",
    )

    column_labels = {
        "ID_Usuario_ClienteF": "ID",
        "Username": "Usuario",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "telefono": "Teléfono",
        "correo": "Correo",
        "ID_sucursal": "Sucursal",
        "estado": "Estado",
    }

    column_filters = ("Username", "nombre", "apellido", "estado")

    # password excluido del formulario — no exponer el hash
    form_columns = (
        "Username",
        "nombre",
        "apellido",
        "telefono",
        "correo",
        "ID_sucursal",
        "estado",
    )

    form_overrides = {
        "Username": StringField,
        "nombre": StringField,
        "apellido": StringField,
        "telefono": StringField,
        "correo": StringField,
        "estado": SelectField,
        "ID_sucursal": SelectField,
    }

    form_args = {
        "Username": {"validators": [DataRequired(), Length(3, 50)]},
        "nombre": {"validators": [DataRequired(), Length(1, 50)]},
        "apellido": {"validators": [DataRequired(), Length(1, 50)]},
        "telefono": {
            "validators": [
                DataRequired(),
                Regexp(r"^\d{7,15}$", message="Teléfono inválido (solo dígitos, 7-15 caracteres)"),
            ]
        },
        "correo": {"validators": [Optional(), Length(max=100)]},
    }

    form_widget_args = {
        "Username": {"autocomplete": "off"},
        "correo": {"type": "email"},
    }

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c30d0d")
        return super().render(template, **kwargs)

    def _quitar_flash_default_admin(self):
        flashes = session.get("_flashes", [])
        if not flashes:
            return
        filtrados = [
            (cat, msg)
            for cat, msg in flashes
            if not (isinstance(msg, str) and msg.strip().lower().startswith("record was successfully"))
        ]
        session["_flashes"] = filtrados

    def _cargar_choices(self, form):
        form.ID_sucursal.choices = [(str(s.ID_sucursal), s.Descripcion) for s in Sucursal.query.all()]
        form.estado.choices = [("1", "Activo"), ("0", "Inactivo")]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._cargar_choices(form)
        form.estado.data = "1"
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._cargar_choices(form)
        if obj is not None and request.method == "GET":
            form.estado.data = "1" if obj.estado == 1 else "0"
            if obj.ID_sucursal is not None:
                form.ID_sucursal.data = str(obj.ID_sucursal)
        return form

    def on_model_change(self, form, model, is_created):
        try:
            sucursal_id = int(form.ID_sucursal.data)
        except Exception:
            msg = "Sucursal inválida"
            form.ID_sucursal.errors.append(msg)
            from wtforms.validators import ValidationError
            raise ValidationError(msg)

        model.ID_sucursal = sucursal_id
        model.estado = int(form.estado.data)

        accion = "creado" if is_created else "actualizado"
        flash(f"Usuario {model.Username!r} {accion} correctamente.", "success")

    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_busqueda", fecha)
            return "Error al abrir el listado de usuarios.", 500

    def get_list(self, page, sort_column, sort_desc, search, filters, execute=True, page_size=None):
        try:
            return super().get_list(
                page, sort_column, sort_desc, search, filters,
                execute=execute, page_size=page_size,
            )
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_paginado", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_paginado", fecha)
            return 0, []

    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            resp = super().create_view()
            if request.method == "POST":
                self._quitar_flash_default_admin()
            return resp
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_crear", fecha)
            return "Error al abrir o procesar la creación del usuario.", 500

    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            resp = super().edit_view()
            if request.method == "POST":
                self._quitar_flash_default_admin()
            return resp
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_editar", fecha)
            return "Error al abrir o procesar la edición del usuario.", 500

    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_eliminar", fecha)
            return "Error al procesar la eliminación del usuario.", 500

    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_guardar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_guardar_crear", fecha)
            return False

    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_guardar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_guardar_editar", fecha)
            return False

    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "usuarios_cliente_borrar_bd", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "usuarios_cliente_borrar_bd", fecha)
            return False
