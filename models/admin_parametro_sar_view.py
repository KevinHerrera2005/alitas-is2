from datetime import datetime
import re
import traceback

from mensajes_logs import logger_

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from models.parametro_sar_model import ParametroSAR


class ParametroSARAdmin(ModelView):
    create_template = "admin/model/parametro_sar_create.html"
    edit_template = "admin/model/parametro_sar_edit.html"

    column_list = ("ID_Parametro", "Parametro", "Valor")

    column_labels = {
        "ID_Parametro": "ID",
        "Parametro": "Parámetro",
        "Valor": "Valor",
    }

    column_default_sort = ("ID_Parametro", True)
    page_size = 10

    column_searchable_list = ("Parametro",)

    form_columns = ("Parametro", "Valor")

    form_overrides = {
        "Parametro": StringField,
        "Valor": StringField,
    }

    form_args = {
        "Parametro": {
            "label": "Parámetro",
            "validators": [DataRequired(), Length(max=50)],
            "render_kw": {"id": "Parametro", "data-validacion": "nombre"},
        },
        "Valor": {
            "label": "Valor",
            "validators": [DataRequired(), Length(max=50)],
            "render_kw": {"id": "Valor", "inputmode": "numeric", "pattern": "[0-9]*"},
        },
    }

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    # Este botón sirve para entrar al listado y usar la búsqueda.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_busqueda", fecha)
            return "Error al abrir el listado de parámetros SAR.", 500

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
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_paginado", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_paginado", fecha)
            return 0, []

    # Este botón sirve para abrir y procesar la vista de crear.
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            return super().create_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_crear", fecha)
            return "Error al abrir o procesar la creación del parámetro SAR.", 500

    # Este botón sirve para abrir y procesar la vista de editar.
    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_editar", fecha)
            return "Error al abrir o procesar la edición del parámetro SAR.", 500

    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_eliminar", fecha)
            return "Error al procesar la eliminación del parámetro SAR.", 500

    def on_model_change(self, form, model, is_created):
        nombre = (form.Parametro.data or "").strip()
        valor = (form.Valor.data or "").strip()

        if not nombre:
            raise ValueError("El nombre del parámetro es obligatorio.")
        if not valor:
            raise ValueError("El valor del parámetro es obligatorio.")

        model.Parametro = nombre
        model.Valor = valor

    # Este bloque se ejecuta cuando guardas un parámetro nuevo.
    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_guardar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_guardar_crear", fecha)
            return False

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_guardar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_guardar_editar", fecha)
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
            logger_.Logger.add_to_log("error", str(error), "parametro_sar_borrar_bd", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "parametro_sar_borrar_bd", fecha)
            return False


def _normalizar_texto(raw):
    if raw is None:
        return None
    out = " ".join(str(raw).strip().split())
    return out or None


def validar_parametro_nombre(raw, min_len=3, max_len=40):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if any(ch.isdigit() for ch in out):
        return None
    if len(out) < int(min_len) or len(out) > int(max_len):
        return None
    if re.search(r"(.)\1\1", out.lower()):
        return None
    return out


def validar_parametro_valor(raw):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if not out.isdigit():
        return None
    try:
        val = int(out)
    except Exception:
        return None
    if val <= 0:
        return None
    return val