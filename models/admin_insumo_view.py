from datetime import datetime
import traceback

from flask_admin.contrib.sqla import ModelView
from flask_admin.base import expose
from flask_login import current_user
from flask import flash, request, jsonify
from wtforms.validators import ValidationError

from mensajes_logs import logger_
from models.unidades_medida_model import Unidades_medida
from models.categoria_insumo_model import CategoriaInsumo
from models.insumo_model import Insumo


class InsumoAdmin(ModelView):
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    column_default_sort = ("ID_Insumo", True)

    column_list = (
        "Nombre_insumo",
        "categoria",
        "unidad",
        "stock_total",
        "stock_minimo",
        "stock_maximo",
        "precio_base",
        "precio_lempiras",
    )

    column_labels = {
        "Nombre_insumo": "Nombre del insumo",
        "stock_total": "Stock total",
        "stock_minimo": "Stock mínimo",
        "stock_maximo": "Stock máximo",
        "precio_base": "Precio base (sin impuesto)",
        "precio_lempiras": "Precio final (con impuesto)",
        "peso_individual": "Peso individual (cantidad que equivale al costo sin impuestos)",
        "categoria": "Categoría",
        "unidad": "Unidad",
    }

    column_formatters = {
        "categoria": lambda view, context, model, name: (model.categoria.Nombre_categoria if getattr(model, "categoria", None) else ""),
        "unidad": lambda view, context, model, name: (model.unidad.Nombre if getattr(model, "unidad", None) else ""),
    }

    column_searchable_list = ("Nombre_insumo",)

    create_template = "admin/model/insumo_create.html"
    edit_template = "admin/model/insumo_edit.html"

    form_columns = (
        "unidad",
        "categoria",
        "Nombre_insumo",
        "stock_total",
        "stock_minimo",
        "stock_maximo",
        "precio_base",
        "peso_individual",
    )

    form_widget_args = {
        "unidad": {"id": "unidad"},
        "categoria": {"id": "categoria"},
        "Nombre_insumo": {"data-validacion": "nombre", "id": "nombre"},
        "stock_total": {"data-validacion": "numero", "id": "stock_total"},
        "stock_minimo": {"data-validacion": "numero", "id": "stock_minimo"},
        "stock_maximo": {"data-validacion": "numero", "id": "stock_maximo"},
        "precio_base": {"data-validacion": "numero", "id": "precio_base"},
        "peso_individual": {"data-validacion": "numero", "id": "peso_individual"},
    }

    form_excluded_columns = ("precios_historicos",)

    form_ajax_refs = {
        "unidad": {
            "fields": (Unidades_medida.Nombre,),
            "order_by": Unidades_medida.Nombre,
            "minimum_input_length": 0,
        },
        "categoria": {
            "fields": (CategoriaInsumo.Nombre_categoria,),
            "order_by": CategoriaInsumo.Nombre_categoria,
            "minimum_input_length": 0,
        },
    }
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self, *args, **kwargs):
        try:
            if request.method == "GET":
                fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
                logger_.Logger.add_to_log("info", "Abrio formulario de crear insumo", "insumo_abrir_crear", fecha)
            return super().create_view(*args, **kwargs)
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_abrir_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_abrir_crear", fecha)
    def _sucursal_id_actual(self):
        try:
            sid = getattr(current_user, "id_sucursal", None) or getattr(current_user, "ID_sucursal", None)
            return int(sid) if sid is not None else None
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_sucursal_actual", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_sucursal_actual", fecha)
            return None

    def get_query(self):
        try:
            q = super().get_query()
            sid = self._sucursal_id_actual()
            if sid is None:
                return q.filter(Insumo.ID_Insumo == -1)
            return q.filter(Insumo.ID_sucursal == sid)
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_listar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_listar", fecha)
            return super().get_query().filter(Insumo.ID_Insumo == -1)

    def get_count_query(self):
        try:
            q = super().get_count_query()
            sid = self._sucursal_id_actual()
            if sid is None:
                return q.filter(Insumo.ID_Insumo == -1)
            return q.filter(Insumo.ID_sucursal == sid)
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo", fecha)
            return super().get_count_query().filter(Insumo.ID_Insumo == -1)

    def _session_get(self, model_cls, pk):
        if pk is None:
            return None
        try:
            return self.session.get(model_cls, pk)
        except Exception:
            return self.session.query(model_cls).get(pk)

    def _tipo_unidad(self, unidad_obj_or_id):
        if unidad_obj_or_id is None:
            return None

        obj = unidad_obj_or_id
        if not hasattr(obj, "__table__"):
            obj = self._session_get(Unidades_medida, int(obj))

        if obj is None:
            return None

        t = getattr(obj, "Tipo", None)
        if t is None:
            t = getattr(obj, "tipo", None)

        try:
            return int(t) if t is not None else None
        except Exception:
            return None

    def _tipo_categoria(self, cat_obj_or_id):
        if cat_obj_or_id is None:
            return None

        obj = cat_obj_or_id
        if not hasattr(obj, "__table__"):
            obj = self._session_get(CategoriaInsumo, int(obj))

        if obj is None:
            return None

        try:
            return int(getattr(obj, "tipo", None))
        except Exception:
            return None

    def _agregar_error_form(self, form, campo, mensaje):
        if not form:
            return
        if hasattr(form, campo):
            f = getattr(form, campo)
            if hasattr(f, "errors"):
                f.errors.append(mensaje)

    def _validar_tipo_unidad_categoria(self, model, form):
        unidad_data = getattr(form, "unidad", None).data if hasattr(form, "unidad") else None
        categoria_data = getattr(form, "categoria", None).data if hasattr(form, "categoria") else None

        tu = self._tipo_unidad(unidad_data or getattr(model, "unidad", None))
        tc = self._tipo_categoria(categoria_data or getattr(model, "categoria", None))

        if tu is None or tc is None:
            msg = "No se pudo validar el tipo: verifica que unidad y categoría tengan tipo asignado."
            self._agregar_error_form(form, "unidad", msg)
            self._agregar_error_form(form, "categoria", msg)
            raise ValidationError(msg)

        if tu != tc:
            msg = "Verifique que la categoría y la unidad sean del mismo estado. Ej: sólido con sólido o líquido con líquido. No se puede sólido(categoría) con líquido(unidad)."
            self._agregar_error_form(form, "unidad", msg)
            self._agregar_error_form(form, "categoria", msg)
            raise ValidationError(msg)

    @expose("/tipo_lookup/")
    def tipo_lookup(self):
        try:
            unidad_id = request.args.get("unidad_id", type=int)
            categoria_id = request.args.get("categoria_id", type=int)

            u = self._session_get(Unidades_medida, unidad_id) if unidad_id else None
            c = self._session_get(CategoriaInsumo, categoria_id) if categoria_id else None

            tu = self._tipo_unidad(u) if u is not None else None
            tc = self._tipo_categoria(c) if c is not None else None

            return jsonify({"unidad_tipo": tu, "categoria_tipo": tc})
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_tipo_lookup", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_tipo_lookup", fecha)
            return jsonify({"error": str(error)}), 500

    def create_form(self, obj=None):
        form = super().create_form(obj)

        try:
            tipo_url = self.get_url(".tipo_lookup")
        except Exception:
            tipo_url = None

        if hasattr(form, "unidad"):
            rw = getattr(form.unidad, "render_kw", None) or {}
            if tipo_url:
                rw["data-tipo-url"] = tipo_url
            form.unidad.render_kw = rw

        if hasattr(form, "categoria"):
            rw = getattr(form.categoria, "render_kw", None) or {}
            if tipo_url:
                rw["data-tipo-url"] = tipo_url
            form.categoria.render_kw = rw

        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)

        try:
            tipo_url = self.get_url(".tipo_lookup")
        except Exception:
            tipo_url = None

        if hasattr(form, "unidad"):
            rw = getattr(form.unidad, "render_kw", None) or {}
            if tipo_url:
                rw["data-tipo-url"] = tipo_url
            form.unidad.render_kw = rw

        if hasattr(form, "categoria"):
            rw = getattr(form.categoria, "render_kw", None) or {}
            if tipo_url:
                rw["data-tipo-url"] = tipo_url
            form.categoria.render_kw = rw

        return form

    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_editar", fecha)
            try:
                self.session.rollback()
            except Exception:
                pass
            flash("No se pudo abrir o procesar la edición del insumo.", "error")
            return "", 500

    def handle_view_exception(self, exc):
        if isinstance(exc, ValidationError):
            flash(str(exc), "error")
            return True

        if isinstance(exc, ValueError):
            flash(str(exc), "error")
            return True

        return super().handle_view_exception(exc)

    def get_list(self, page, sort_column, sort_desc, search, filters, page_size=None):
        try:
            return super().get_list(page, sort_column, sort_desc, search, filters, page_size=page_size)
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_listar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_listar", fecha)
            flash("No se pudo cargar el listado de insumos.", "error")
            return 0, []

    def on_model_change(self, form, model, is_created):
        sid = self._sucursal_id_actual()
        if sid is None:
            raise ValidationError("No se pudo determinar la sucursal del usuario.")

        if is_created:
            model.ID_sucursal = sid
        else:
            if model.ID_sucursal != sid:
                raise ValidationError("No puedes editar insumos de otra sucursal.")

        self._validar_tipo_unidad_categoria(model, form)

        return super().on_model_change(form, model, is_created)

    def create_model(self, form):
        try:
            creado = super().create_model(form)
            return creado
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_crear", fecha)
            try:
                self.session.rollback()
            except Exception:
                pass
            flash(f"Error al crear el insumo: {str(error)}", "error")
            return False

    def update_model(self, form, model):
        try:
            actualizado = super().update_model(form, model)
            return actualizado
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_actualizar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_actualizar", fecha)
            try:
                self.session.rollback()
            except Exception:
                pass
            flash(f"Error al actualizar el insumo: {str(error)}", "error")
            return False

    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "insumo_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "insumo_eliminar", fecha)
            try:
                self.session.rollback()
            except Exception:
                pass
            flash("No se pudo eliminar el insumo.", "error")
            return "", 500