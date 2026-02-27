from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
import traceback

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
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "tipo", None) == "empleado"
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))

    def handle_view_exception(self, exc):
        traceback.print_exc()
        flash(str(exc), "danger")
        return False

    def on_model_change(self, form, model, is_created):
        nombre = (form.Nombre_categoria_receta.data or "").strip()
        if not nombre:
            raise ValueError("El nombre de la categoría es obligatorio.")

        nombre_lower = nombre.lower()
        session = self.session

        q = session.query(Categoria_recetas).filter(
            func.lower(Categoria_recetas.Nombre_categoria_receta) == nombre_lower
        )

        if getattr(model, "id_categoria_receta", None):
            q = q.filter(
                Categoria_recetas.id_categoria_receta != model.id_categoria_receta
            )

        existentes = [c for c in q.all() if c is not model]
        if existentes:
            raise ValueError("Esta categoría ya existe.")

        model.Nombre_categoria_receta = nombre

        if hasattr(form, "descripcion"):
            model.descripcion = (form.descripcion.data or "").strip()

    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            flash("La categoría de receta fue eliminada correctamente.", "success")
            return True
        except IntegrityError:
            self.session.rollback()
            flash(
                "No se puede eliminar esta categoría porque está relacionada con una o más recetas.",
                "danger",
            )
            return False
        except Exception:
            self.session.rollback()
            flash(
                "No se pudo eliminar la categoría por un error inesperado.",
                "danger",
            )
            return False
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