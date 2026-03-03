from mensajes_logs import logger_
from datetime import datetime
import traceback

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func

from models.categoria_recetas_model import Categoria_recetas


class CategoriaRecetaAdmin(ModelView):
    can_search = True
    column_searchable_list = ("Nombre_categoria_receta",)

    column_list = (
        "id_categoria_receta",
        "Nombre_categoria_receta",
        "descripcion",
    )
    column_default_sort = ("id_categoria_receta", True)

    column_labels = {
        "id_categoria_receta": "ID",
        "Nombre_categoria_receta": "Nombre de la categoría",
        "descripcion": "Descripción",
    }

    form_columns = ("Nombre_categoria_receta", "descripcion")

    create_template = "admin/model/categoria_receta_create.html"
    edit_template = "admin/model/categoria_receta_edit.html"

    form_widget_args = {
        "Nombre_categoria_receta": {
            "data-validacion": "nombre",
            "id": "catreceta_nombre",
        },
        "descripcion": {
            "data-validacion": "descripcion",
            "id": "catreceta_descripcion",
        },
    }

    # Este bloque solo pinta el panel en rojo.
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    # Este botón sirve para entrar al listado y usar la búsqueda.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_receta_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_receta_busqueda", fecha)

    # Este botón sirve para abrir la pantalla de crear.
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        return super().create_view()

    # Este botón sirve para abrir y procesar la vista de editar.
    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_receta_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_receta_editar", fecha)

    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_receta_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_receta_eliminar", fecha)


    # Este bloque se ejecuta cuando guardas una categoría nueva.
    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
                fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
                logger_.Logger.add_to_log("error", str(error), "categoria_receta_guardar_adentro", fecha)
                logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_receta_guardar_adentro", fecha)

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
                fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
                logger_.Logger.add_to_log("error", str(error), "categoria_receta_update", fecha)
                logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_receta_update", fecha)
    # Este bloque elimina el registro en la base de datos.
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as error:
                fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
                logger_.Logger.add_to_log("error", str(error), "categoria_receta_eliminar_de_bd", fecha)
                logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_receta_eliminar_de_bd", fecha)

def _normalizar_texto(raw):
    if raw is None:
        return None
    out = " ".join(str(raw).strip().split())
    return out or None


def validar_nombre_categoria_receta(raw, min_len=3, max_len=60):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if len(out) < int(min_len):
        return None
    if len(out) > int(max_len):
        return None
    return out


def validar_descripcion_categoria_receta(raw, min_len=0, max_len=200, permitir_none=True):
    out = _normalizar_texto(raw)
    if out is None:
        return None if permitir_none else None
    if len(out) < int(min_len):
        return None
    if len(out) > int(max_len):
        return None
    return out