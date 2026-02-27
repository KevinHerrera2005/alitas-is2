from flask_admin.contrib.sqla import ModelView
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from models import db
from models.parametro_sar_model import ParametroSAR

import re
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

    def on_model_change(self, form, model, is_created):
        nombre = (form.Parametro.data or "").strip()
        valor = (form.Valor.data or "").strip()

        if not nombre:
            raise ValueError("El nombre del parámetro es obligatorio.")
        if not valor:
            raise ValueError("El valor del parámetro es obligatorio.")

        model.Parametro = nombre
        model.Valor = valor
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

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