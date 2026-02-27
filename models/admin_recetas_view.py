from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import SelectField, TextAreaField, StringField

from models.receta_model import Receta
from models.categoria_recetas_model import Categoria_recetas


class RecetaAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a Recetas.", "danger")
        return redirect(url_for("login"))

    def is_visible(self):
        return self.is_accessible()

    column_list = (
        "Nombre_receta",
        "categoria",
        "Estado",
        "descripcion",
    )

    column_labels = {
        "Nombre_receta": "Nombre de la receta",
        "categoria": "Categoría",
        "Estado": "Estado",
        "descripcion": "Descripción",
    }

    column_default_sort = ("Nombre_receta", True)
    page_size = 10

    form_columns = (
        "Nombre_receta",
        "categoria",
        "descripcion",
    )

    form_overrides = {
        "Nombre_receta": StringField,
        "descripcion": TextAreaField,
        "categoria": SelectField,
    }

    form_widget_args = {
        "Nombre_receta": {
            "data-validacion": "nombre",
            "id": "receta_nombre",
        },
        "descripcion": {
            "data-validacion": "descripcion",
            "id": "receta_descripcion",
        },
        "categoria": {
            "id": "receta_categoria",
        },
    }

    create_template = "admin/model/receta_create.html"
    edit_template = "admin/model/receta_edit.html"

    def _categoria_choices(self):
        categorias = Categoria_recetas.query.order_by(Categoria_recetas.Nombre_categoria_receta).all()
        return [(str(c.id_categoria_receta), c.Nombre_categoria_receta) for c in categorias]

    def _sucursal_id_actual(self):
        sid = getattr(current_user, "id_sucursal", None) or getattr(current_user, "ID_sucursal", None)
        try:
            return int(sid) if sid is not None else None
        except Exception:
            return None

    def get_query(self):
        q = super().get_query()
        sid = self._sucursal_id_actual()
        if sid is None:
            return q.filter(Receta.ID_Receta == -1)
        return q.filter(Receta.ID_sucursal == sid)

    def get_count_query(self):
        q = super().get_count_query()
        sid = self._sucursal_id_actual()
        if sid is None:
            return q.filter(Receta.ID_Receta == -1)
        return q.filter(Receta.ID_sucursal == sid)

    def create_form(self, obj=None):
        form = super().create_form(obj)
        if hasattr(form, "categoria"):
            form.categoria.choices = self._categoria_choices()
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if hasattr(form, "categoria"):
            form.categoria.choices = self._categoria_choices()
            if obj and obj.categoria is not None:
                form.categoria.data = str(obj.categoria)
        return form

    def on_model_change(self, form, model, is_created):
        sid = self._sucursal_id_actual()
        if sid is None:
            raise ValueError("No se pudo determinar la sucursal del usuario.")

        if hasattr(form, "categoria") and form.categoria.data:
            try:
                model.categoria = int(form.categoria.data)
            except ValueError:
                model.categoria = None

        if is_created:
            model.ID_sucursal = sid

            if hasattr(current_user, "ID_Jefe_de_cocina"):
                model.ID_Jefe_de_cocina = current_user.ID_Jefe_de_cocina
            elif hasattr(current_user, "db_id"):
                model.ID_Jefe_de_cocina = current_user.db_id
            elif hasattr(current_user, "id"):
                model.ID_Jefe_de_cocina = current_user.id

            model.Estado = 1
        else:
            if model.ID_sucursal != sid:
                raise ValueError("No puedes editar recetas de otra sucursal.")
            if model.Estado is None:
                model.Estado = 1
import re
from sqlalchemy import text
from models import db


def _normalizar_texto(raw):
    if raw is None:
        return None
    out = " ".join(str(raw).strip().split())
    return out or None


def validar_nombre_receta(raw, min_len=3, max_len=30):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if len(out) < int(min_len) or len(out) > int(max_len):
        return None
    if out.isdigit():
        return None
    if re.search(r"(.)\1\1", out.lower()):
        return None
    for ch in out:
        if not (ch.isalnum() or ch in " +=-"):
            return None
    return out


def validar_pasos_receta(raw, min_len=6):
    if raw is None:
        return None
    txt = str(raw)
    if txt.strip() == "":
        return None
    if "\n" not in txt:
        return None

    lineas = txt.splitlines()
    if any(l.strip() == "" for l in lineas):
        return None

    for l in lineas:
        s = l.strip()
        if len(s) < 3:
            return None
        if "@" in s:
            return None

    if len(txt.strip()) < int(min_len):
        return None

    return txt


def validar_estado_receta(raw):
    if raw in (None, ""):
        return 1
    try:
        out = int(str(raw).strip())
    except Exception:
        return 1
    if out == 1:
        return 1
    if out == 0:
        return 0
    return 0


def categoria_receta_existe_db(raw_id):
    try:
        rid = int(raw_id)
    except Exception:
        return False

    try:
        existe = db.session.execute(
            text(
                "SELECT TOP 1 1 FROM categoria_recetas WHERE id_categoria_receta = :id"
            ),
            {"id": rid},
        ).scalar()
        return bool(existe)
    except Exception:
        return False