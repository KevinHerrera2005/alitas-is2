from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_login import current_user
from flask import redirect, url_for, flash, request
from wtforms import SelectField, SelectMultipleField
from wtforms.validators import ValidationError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import db
from models.impuestos_model import Impuesto, ImpuestoCategoria
from models.categoria_insumo_model import CategoriaInsumo
from models.insumo_model import Insumo


class ImpuestoAdmin(ModelView):
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)
    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"

    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "tipo", None) == "empleado"
            and getattr(current_user, "id_puesto", None) == 10
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))

    def is_visible(self):
        return self.is_accessible()

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
        """
        Activa / desactiva filas en Impuesto_Categoria según lo elegido.
        """
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

    def _recalcular_precios_insumos(self, model: Impuesto):
        """
        Recalcula el precio de todos los insumos cuyas categorías
        están asociadas a este impuesto (ImpuestoCategoria.Activo = 1).

        precio_lempiras = precio_base * (1 + tasa/100)
        """
        try:
            tasa = float(model.tasa or 0)
        except (TypeError, ValueError):
            tasa = 0.0

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

    def delete_model(self, model):
        try:
            self.session.query(ImpuestoCategoria).filter_by(
                ID_Impuesto=model.ID_Impuesto
            ).delete(synchronize_session=False)

            self.session.delete(model)
            self.session.commit()
            flash("Impuesto eliminado correctamente.", "success")
            return True
        except IntegrityError:
            self.session.rollback()
            flash(
                "No se puede eliminar el impuesto por restricciones de la base de datos.",
                "danger",
            )
            return False
        except Exception:
            self.session.rollback()
            flash("No se pudo eliminar el impuesto.", "danger")
            return False

    @action("activar", "Activar seleccionados", "¿Activar los impuestos seleccionados?")
    def action_activar(self, ids):
        try:
            self.session.query(Impuesto).filter(
                Impuesto.ID_Impuesto.in_(ids)
            ).update({"activo": 1}, synchronize_session=False)
            self.session.commit()
            flash("Impuestos activados.", "success")
        except Exception:
            self.session.rollback()
            flash("No se pudo activar.", "danger")

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
        except Exception:
            self.session.rollback()
            flash("No se pudo inactivar.", "danger")
