from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash, request
from wtforms import SelectField
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
import traceback

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
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))

    def handle_view_exception(self, exc):
        traceback.print_exc()
        flash(str(exc), "danger")
        return False

    def create_form(self, obj=None):
        form = super().create_form(obj)

        if "estado" in form._fields:
            form._fields.pop("estado")

        if hasattr(form, "tipo") and (form.tipo.data is None):
            form.tipo.data = 1

        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)

        if request.method == "GET" and obj is not None:
            if hasattr(form, "tipo"):
                try:
                    form.tipo.data = int(getattr(obj, "tipo", 1) or 1)
                except Exception:
                    form.tipo.data = 1

            if hasattr(form, "estado"):
                try:
                    form.estado.data = int(getattr(obj, "estado", 1) or 1)
                except Exception:
                    form.estado.data = 1

        return form

    def on_model_change(self, form, model, is_created):
        try:
            print("=== DEBUG on_model_change ===")
            print("is_created =", is_created, "method =", getattr(request, "method", None))
            print("pk =", getattr(model, "ID_Categoria", None))
            print("tipo antes =", getattr(model, "tipo", None), "estado antes =", getattr(model, "estado", None))

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

            print("tipo después set =", getattr(model, "tipo", None), "estado después set =", getattr(model, "estado", None))
            print("=== /DEBUG on_model_change ===")

        except Exception as e:
            print("=== ERROR en on_model_change ===")
            traceback.print_exc()
            print("=== /ERROR ===")
            raise

    def after_model_change(self, form, model, is_created):
        try:
            print("=== DEBUG after_model_change ===")
            print("pk =", getattr(model, "ID_Categoria", None))
            self.session.refresh(model)
            print("tipo en DB (refresh) =", getattr(model, "tipo", None), "estado en DB (refresh) =", getattr(model, "estado", None))
            print("=== /DEBUG after_model_change ===")
        except Exception:
            print("=== ERROR en after_model_change ===")
            traceback.print_exc()
            print("=== /ERROR ===")

    def update_model(self, form, model):
        try:
            ok = super().update_model(form, model)
            print("=== DEBUG update_model ===")
            print("update_model ok =", ok, "pk =", getattr(model, "ID_Categoria", None))
            self.session.refresh(model)
            print("tipo final =", getattr(model, "tipo", None), "estado final =", getattr(model, "estado", None))
            print("=== /DEBUG update_model ===")
            return ok
        except Exception:
            print("=== ERROR en update_model ===")
            traceback.print_exc()
            print("=== /ERROR ===")
            raise

    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
            flash("Categoría eliminada correctamente.", "success")
            return True
        except IntegrityError:
            self.session.rollback()
            flash(
                "No se puede eliminar la categoría porque está siendo utilizada por uno o más insumos.",
                "danger",
            )
            return False
        except Exception:
            self.session.rollback()
            flash("No se pudo eliminar la categoría por un error", "danger")
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
    try:
        out = int(raw)
    except Exception:
        return int(default)
    return 1 if out == 1 else 0

