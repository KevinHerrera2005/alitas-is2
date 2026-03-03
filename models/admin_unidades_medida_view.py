from mensajes_logs import logger_
from datetime import datetime
import traceback


from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField

from models import db
from models.unidades_medida_model import Unidades_medida


class UnidadesMedidaAdmin(ModelView):
    create_template = "admin/model/unidad_create.html"
    edit_template = "admin/model/unidad_edit.html"

    can_search = True
    column_searchable_list = ("Nombre", "abreviatura")

    column_list = ("Nombre", "abreviatura", "Tipo")
    column_labels = {
        "Nombre": "Nombre de la unidad",
        "abreviatura": "Abreviatura",
        "Tipo": "Tipo",
    }
    column_default_sort = ("ID_Unidad", True)

    form_columns = ("Nombre", "abreviatura", "Tipo")

    form_widget_args = {
        "Nombre": {
            "data-validacion": "nombre",
            "id": "unidad_nombre",
        },
        "abreviatura": {
            "data-validacion": "abreviatura",
            "id": "unidad_abreviatura",
        },
        "Tipo": {
            "data-validacion": "numero_positivo",
            "id": "unidad_tipo",
        },
    }

    form_overrides = {
        "Tipo": SelectField,
    }

    form_args = {
        "Tipo": {
            "choices": [
                ("1", "1 - Peso"),
                ("2", "2 - Volumen"),
                ("3", "3 - Unidad"),
            ]
        }
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
            logger_.Logger.add_to_log("error", str(error), "unidades_medida_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "unidades_medida_busqueda", fecha)

    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
            return super().create_view()


    # Este botón sirve para abrir la pantalla de editar.
    @expose("/edit/", methods=("GET", "POST"))

    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "unidades_medida_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "unidades_medida_editar", fecha)
    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "unidades_medida_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "unidades_medida_eliminar", fecha)

    # Este bloque valida y prepara los datos cuando guardas al crear o editar.
    def on_model_change(self, form, model, is_created):
        try:
            nombre = (form.Nombre.data or "").strip()
            abrev = (form.abreviatura.data or "").strip()
            tipo_raw = str(form.Tipo.data).strip() if form.Tipo.data is not None else ""

            if not nombre:
                raise ValueError("El nombre de la unidad es obligatorio.")

            if not abrev:
                raise ValueError("La abreviatura es obligatoria.")

            if not tipo_raw:
                raise ValueError("El tipo es obligatorio.")

            tipo_int = int(tipo_raw)
            abrev = abrev.upper()

            with db.session.no_autoflush:
                q_nombre = Unidades_medida.query.filter(
                    db.func.lower(Unidades_medida.Nombre) == nombre.lower()
                )

                if not is_created and getattr(model, "ID_Unidad", None) is not None:
                    q_nombre = q_nombre.filter(
                        Unidades_medida.ID_Unidad != model.ID_Unidad
                    )

                if q_nombre.first():
                    raise ValueError("Ya existe una unidad con ese nombre.")

                q_abrev = Unidades_medida.query.filter(
                    db.func.lower(Unidades_medida.abreviatura) == abrev.lower()
                )

                if not is_created and getattr(model, "ID_Unidad", None) is not None:
                    q_abrev = q_abrev.filter(
                        Unidades_medida.ID_Unidad != model.ID_Unidad
                    )

                if q_abrev.first():
                    raise ValueError("Ya existe una unidad con esa abreviatura.")

            model.Nombre = nombre
            model.abreviatura = abrev
            model.Tipo = tipo_int
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "unidades_medida_guardar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "unidades_medida_guardar", fecha)
    # Este bloque se ejecuta cuando guardas una unidad nueva.
    def create_model(self, form):
        return super().create_model(form)

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        return super().update_model(form, model)

    # Este bloque elimina el registro en la base de datos.
    def delete_model(self, model):
        self.session.delete(model)
        self.session.commit()
        return True