from datetime import datetime
import traceback

from mensajes_logs import logger_

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask import flash, request
from wtforms import SelectField, SelectMultipleField
from wtforms.validators import ValidationError
from sqlalchemy import func

from models import db
from models.impuestos_model import Impuesto, ImpuestoCategoria
from models.categoria_insumo_model import CategoriaInsumo
from models.insumo_model import Insumo
from models.permisos_mixin import PermisosAdminMixin


class ImpuestoAdmin(PermisosAdminMixin, ModelView):
    accion_buscar         = "buscar"
    accion_crear          = "crear"
    accion_editar         = "editar"
    accion_eliminar       = "eliminar"
    accion_exportar_pdf   = "exportar pdf"
    accion_exportar_excel = "exportar excel"
    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"

    column_list = (
        "Nombre_Impuesto",
        "tasa",
        "descripcion",
        "activo",
    )
    column_default_sort = ("ID_Impuesto", True)
    page_size = 10
    column_searchable_list = ("Nombre_Impuesto", "descripcion")

    column_labels = {
        "Nombre_Impuesto": "Nombre del impuesto",
        "tasa": "Tasa",
        "descripcion": "Descripción",
        "activo": "Estado",
    }

    column_formatters = {
        "activo": lambda v, c, m, n: "Activo" if m.activo == 1 else "Inactivo"
    }

    form_columns = (
        "Nombre_Impuesto",
        "tasa",
        "descripcion",
        "categorias_ids",
        "activo",
    )

    form_overrides = {
        "activo": SelectField,
    }

    form_widget_args = {
        "Nombre_Impuesto": {
            "id": "imp_nombre",
            "data-validacion": "nombre",
        },
        "tasa": {
            "id": "imp_tasa",
        },
        "descripcion": {
            "id": "imp_descripcion",
            "data-validacion": "descripcion",
        },
        "categorias_ids": {
            "id": "imp_categorias",
        },
        "activo": {
            "id": "imp_activo",
        },
    }

    form_extra_fields = {
        "categorias_ids": SelectMultipleField(
            "Categorías a las que aplica",
            coerce=int,
        )
    }
    

    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    def is_visible(self):
        return self.is_accessible()

    def _build_categoria_choices(self):
        categorias = CategoriaInsumo.query.order_by(
            CategoriaInsumo.Nombre_categoria
        ).all()
        return [(c.ID_Categoria, c.Nombre_categoria) for c in categorias]

    def create_form(self, obj=None):
        form = super().create_form(obj)

        if hasattr(form, "activo"):
            form._fields.pop("activo")

        if hasattr(form, "categorias_ids"):
            form.categorias_ids.choices = self._build_categoria_choices()

        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)

        if hasattr(form, "categorias_ids"):
            form.categorias_ids.choices = self._build_categoria_choices()
            if obj is not None:
                activos = (
                    ImpuestoCategoria.query.filter_by(
                        ID_Impuesto=obj.ID_Impuesto,
                        Activo=1,
                    )
                    .with_entities(ImpuestoCategoria.ID_Categoria)
                    .all()
                )
                form.categorias_ids.data = [row.ID_Categoria for row in activos]

        if hasattr(form, "activo"):
            form.activo.choices = [("1", "Activo"), ("0", "Inactivo")]
            if request.method == "GET" and obj is not None:
                form.activo.data = "1" if obj.activo == 1 else "0"

        return form

    def _validar_campos(self, form, model, is_created):
        nombre = (form.Nombre_Impuesto.data or "").strip()
        descripcion = (form.descripcion.data or "").strip()
        tasa_raw = form.tasa.data

        if not nombre or not descripcion or tasa_raw is None:
            raise ValidationError("Todos los campos de impuesto son obligatorios.")

        try:
            tasa_val = float(tasa_raw)
        except (TypeError, ValueError):
            raise ValidationError("La tasa debe ser un número.")

        if tasa_val < 0 or tasa_val > 1000:
            raise ValidationError("La tasa debe ser un valor positivo razonable.")

        if not form.categorias_ids.data:
            raise ValidationError("Debes seleccionar al menos una categoría.")

        with self.session.no_autoflush:
            q_nombre = (
                self.session.query(Impuesto)
                .filter(func.lower(Impuesto.Nombre_Impuesto) == nombre.lower())
            )
            if getattr(model, "ID_Impuesto", None):
                q_nombre = q_nombre.filter(
                    Impuesto.ID_Impuesto != model.ID_Impuesto
                )
            if q_nombre.first():
                raise ValidationError("Ya existe un impuesto con ese nombre.")

        model.Nombre_Impuesto = nombre
        model.descripcion = descripcion
        model.tasa = tasa_val

        if is_created:
            model.activo = 1
        else:
            if hasattr(form, "activo"):
                model.activo = 1 if str(form.activo.data).strip() == "1" else 0

        model.ID_Categoria = int(form.categorias_ids.data[0])

    def _sincronizar_categorias(self, form, model):
        self.session.flush()

        seleccionadas = set(form.categorias_ids.data or [])

        relaciones = ImpuestoCategoria.query.filter_by(
            ID_Impuesto=model.ID_Impuesto
        ).all()

        existentes = {r.ID_Categoria: r for r in relaciones}

        for cat_id in seleccionadas:
            rel = existentes.get(cat_id)
            if rel:
                rel.Activo = 1
            else:
                rel = ImpuestoCategoria(
                    ID_Impuesto=model.ID_Impuesto,
                    ID_Categoria=cat_id,
                    Activo=1,
                )
                self.session.add(rel)

        for cat_id, rel in existentes.items():
            if cat_id not in seleccionadas:
                rel.Activo = 0

        self.session.flush()

    def _recalcular_precios_insumos(self, model):
        tasa = float(model.tasa or 0)

        if tasa <= 0:
            return

        factor = 1.0 + (tasa / 100.0)

        categorias_ids = [
            r.ID_Categoria
            for r in ImpuestoCategoria.query
            .filter_by(ID_Impuesto=model.ID_Impuesto, Activo=1)
            .all()
        ]

        if not categorias_ids:
            return

        insumos = (
            self.session.query(Insumo)
            .filter(Insumo.ID_Categoria.in_(categorias_ids))
            .all()
        )

        for ins in insumos:
            base = ins.precio_base
            if base is None and ins.precio_lempiras is not None:
                base = ins.precio_lempiras
                ins.precio_base = base

            if base is None:
                continue

            ins.precio_lempiras = float(base) * factor

        self.session.flush()

    def on_model_change(self, form, model, is_created):
        self._validar_campos(form, model, is_created)
        self._sincronizar_categorias(form, model)
        self._recalcular_precios_insumos(model)

    # Este botón sirve para entrar al listado y usar la búsqueda.
    @expose("/")
    def index_view(self):
        try:
            return super().index_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_busqueda", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_busqueda", fecha)
            return "Error al abrir el listado de impuestos.", 500

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
            logger_.Logger.add_to_log("error", str(error), "impuesto", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto", fecha)
            return 0, []

    # Este botón sirve para abrir la pantalla de crear.
    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        try:
            return super().create_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_crear", fecha)
            return "Error al abrir o procesar la creación del impuesto.", 500

    # Este botón sirve para abrir y procesar la vista de editar.
    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        try:
            return super().edit_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_editar", fecha)
            return "Error al abrir o procesar la edición del impuesto.", 500

    # Este botón sirve para procesar la acción de eliminar.
    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        try:
            return super().delete_view()
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_eliminar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_eliminar", fecha)
            return "Error al procesar la eliminación del impuesto.", 500

    # Este bloque se ejecuta cuando guardas un impuesto nuevo.
    def create_model(self, form):
        try:
            return super().create_model(form)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_guardar_crear", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_guardar_crear", fecha)
            flash("No se pudo guardar el impuesto.", "danger")
            return False

    # Este bloque se ejecuta cuando guardas una edición.
    def update_model(self, form, model):
        try:
            return super().update_model(form, model)
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_guardar_editar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_guardar_editar", fecha)
            flash("No se pudo guardar la edición del impuesto.", "danger")
            return False

    # Este bloque elimina el registro en la base de datos.
    def delete_model(self, model):
        try:
            self.session.query(ImpuestoCategoria).filter_by(
                ID_Impuesto=model.ID_Impuesto
            ).delete(synchronize_session=False)

            self.session.delete(model)
            self.session.commit()
            flash("Impuesto eliminado correctamente.", "success")
            return True
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_borrar_bd", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_borrar_bd", fecha)
            flash("No se pudo eliminar el impuesto.", "danger")
            return False

    # Este botón sirve para activar los impuestos seleccionados.
    @action("activar", "Activar seleccionados", "¿Activar los impuestos seleccionados?")
    def action_activar(self, ids):
        try:
            self.session.query(Impuesto).filter(
                Impuesto.ID_Impuesto.in_(ids)
            ).update({"activo": 1}, synchronize_session=False)
            self.session.commit()
            flash("Impuestos activados.", "success")
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_activar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_activar", fecha)
            flash("No se pudo activar.", "danger")

    # Este botón sirve para inactivar los impuestos seleccionados.
    @action(
        "inactivar",
        "Inactivar seleccionados",
        "¿Inactivar los impuestos seleccionados?",
    )
    def action_inactivar(self, ids):
        try:
            self.session.query(Impuesto).filter(
                Impuesto.ID_Impuesto.in_(ids)
            ).update({"activo": 0}, synchronize_session=False)
            self.session.commit()
            flash("Impuestos inactivados.", "success")
        except Exception as error:
            self.session.rollback()
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "impuesto_inactivar", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "impuesto_inactivar", fecha)
            flash("No se pudo inactivar.", "danger")