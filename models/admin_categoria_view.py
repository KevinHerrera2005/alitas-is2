from flask_admin.contrib.sqla import ModelView
from flask_admin.base import expose
from flask import flash, request, redirect
from wtforms import SelectField
from sqlalchemy import func
import traceback
from datetime import datetime
from mensajes_logs import logger_
from models.categoria_insumo_model import CategoriaInsumo


TIPO_CHOICES = [(1, "Sólido"), (2, "Líquido"), (3, "Medición")]
ESTADO_CHOICES = [(1, "Activo"), (0, "Inactivo")]


def fmt_tipo(view, context, model, name):
    m = dict(TIPO_CHOICES)
    return m.get(getattr(model, "tipo", None), "")


def fmt_estado(view, context, model, name):
    
    m = dict(ESTADO_CHOICES)
    return m.get(getattr(model, "estado", None), "")


class CategoriaAdmin(ModelView):
    create_template = "admin/model/categoria_create.html"
    edit_template = "admin/model/categoria_edit.html"

    can_search = True
    column_searchable_list = ("Nombre_categoria",)

    column_list = ("Nombre_categoria", "descripcion", "tipo", "estado")

    column_labels = {
        "Nombre_categoria": "Nombre de la categoría",
        "descripcion": "Descripción",
        "tipo": "Tipo",
        "estado": "Estado",
    }

    column_default_sort = ("ID_Categoria", True)
    page_size = 10

    form_columns = ("Nombre_categoria", "descripcion", "tipo", "estado")

    form_overrides = {
        "estado": SelectField,
        "tipo": SelectField,
    }

    form_args = {
        "tipo": {"choices": TIPO_CHOICES, "coerce": int},
        "estado": {"choices": ESTADO_CHOICES, "coerce": int},
    }

    column_formatters = {
        "tipo": fmt_tipo,
        "estado": fmt_estado,
    }

    column_choices = {
        "tipo": TIPO_CHOICES,
        "estado": ESTADO_CHOICES,
    }

    form_widget_args = {
        "Nombre_categoria": {"data-validacion": "nombre", "id": "categoria_nombre"},
        "descripcion": {"data-validacion": "descripcion", "id": "categoria_descripcion"},
        "tipo": {"id": "categoria_tipo"},
        "estado": {"id": "categoria_estado"},
    }

    def _silenciar_log_listado(self):
        return request.args.get("_origen_log") in ("create", "edit", "delete")

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    def handle_view_exception(self, exc):
        flash(str(exc), "danger")
        return False

    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            if not self._silenciar_log_listado():
                fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
                logger_.Logger.add_to_log("error", str(error), "categoria_insumo", fecha)
                logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_insumo", fecha)
        flash("No se pudo cargar el listado de categorías.", "danger")
        return ""

    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            return super().create_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_insumo_boton_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_insumo_boton_crear", fecha)
        flash("No se pudo abrir la pantalla de crear categoría.", "danger")
        return redirect(self.get_url(".index_view", _origen_log="create"))

    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_insumo_boton_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_insumo_boton_editar", fecha)
        flash("No se pudo abrir o procesar la edición.", "danger")
        return redirect(self.get_url(".index_view", _origen_log="edit"))

    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            id_value = request.form.get("id") or request.args.get("id")
            if not id_value:
                raise ValueError("No se recibió el ID para eliminar.")

            model = super().get_one(id_value)
            if model is None:
                raise ValueError("La categoría no existe.")

            self.delete_model(model)
            return redirect(self.get_url(".index_view", _origen_log="delete"))
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_insumo_boton_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_insumo_boton_eliminar", fecha)
        flash("No se pudo eliminar la categoría.", "danger")
        return redirect(self.get_url(".index_view", _origen_log="delete"))


    def create_form(self, obj=None):
        form = super().create_form(obj)

        if "estado" in form._fields:
            form._fields.pop("estado")

        if hasattr(form, "tipo") and form.tipo.data is None:
            form.tipo.data = 1

        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)

        if request.method == "GET" and obj is not None:
            if hasattr(form, "tipo"):
                tipo_val = validar_tipo_categoria(getattr(obj, "tipo", 1))
                form.tipo.data = tipo_val if tipo_val is not None else 1

            if hasattr(form, "estado"):
                form.estado.data = validar_estado_categoria(getattr(obj, "estado", 1))

        return form

    def on_model_change(self, form, model, is_created):
        nombre_raw = getattr(form, "Nombre_categoria").data or ""
        nombre = " ".join(str(nombre_raw).strip().split())

        if not nombre:
            raise ValueError("El nombre de la categoría es obligatorio.")

        session = self.session
        nombre_lower = nombre.lower()

        with session.no_autoflush:
            q = session.query(CategoriaInsumo.ID_Categoria).filter(
                func.lower(func.ltrim(func.rtrim(CategoriaInsumo.Nombre_categoria))) == nombre_lower
            )

            model_id = getattr(model, "ID_Categoria", None)
            if model_id is not None:
                q = q.filter(CategoriaInsumo.ID_Categoria != model_id)

            if q.first() is not None:
                raise ValueError("Esta categoría ya existe.")

        tipo_val = getattr(form, "tipo").data if hasattr(form, "tipo") else None
        if tipo_val not in (1, 2, 3):
            raise ValueError("Debes seleccionar el tipo de la categoría (Sólido/Líquido/Medición).")

        model.Nombre_categoria = nombre
        model.descripcion = (getattr(form, "descripcion").data or "").strip() or None
        model.tipo = int(tipo_val)

        if is_created:
            model.estado = 1
        else:
            est_val = getattr(form, "estado").data if hasattr(form, "estado") else 1
            model.estado = 1 if int(est_val) == 1 else 0

        session.flush()

    def after_model_change(self, form, model, is_created):
        self.session.refresh(model)

    def create_model(self, form):
        try:
            model = self.build_new_instance()
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
            self.after_model_change(form, model, True)
            return model
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_insumo_guardar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_insumo_guardar", fecha)
        self.session.rollback()
        flash("No se pudo crear la categoría.", "danger")
        return False

    def update_model(self, form, model):
        try:
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()
            self.after_model_change(form, model, False)
            return True
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_insumo_actualizar_cambios", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_insumo_actualizar_cambios", fecha)
        self.session.rollback()
        flash("No se pudo actualizar la categoría.", "danger")
        return False

    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            flash("Categoría eliminada correctamente.", "success")
            return True
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "categoria_insumo_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "categoria_insumo_eliminar", fecha)
        self.session.rollback()
        flash("No se pudo eliminar la categoría.", "danger")
        return False


def _normalizar_texto(raw):
    if raw is None:
        return None
    out = " ".join(str(raw).strip().split())
    return out or None


def validar_nombre_categoria(raw, min_len=3, max_len=60):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if len(out) < int(min_len):
        return None
    if len(out) > int(max_len):
        return None
    return out


def validar_descripcion_categoria(raw, min_len=0, max_len=200, permitir_none=True):
    out = _normalizar_texto(raw)
    if out is None:
        return None if permitir_none else None
    if len(out) < int(min_len):
        return None
    if len(out) > int(max_len):
        return None
    return out


def validar_tipo_categoria(raw):
    if raw is None:
        return None

    if isinstance(raw, float):
        if not raw.is_integer():
            return None
        raw = int(raw)

    s = str(raw).strip()
    if s == "":
        return None
    if not s.isdigit():
        return None

    out = int(s)
    if out not in (1, 2, 3):
        return None
    return out


def validar_estado_categoria(raw, default=1):
    if raw is None:
        return int(default)

    if isinstance(raw, float):
        if not raw.is_integer():
            return int(default)
        raw = int(raw)

    s = str(raw).strip()
    if s == "":
        return int(default)
    if not s.isdigit():
        return int(default)

    out = int(s)
    return 1 if out == 1 else 0