from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import SelectField
from wtforms.validators import DataRequired, Regexp

from models.tipo_documento_model import TipoDocumento


class TipoDocumentoAdmin(ModelView):
    can_create = True
    can_edit = True
    can_delete = False

    can_view_details = True
    can_export = True

    column_list = ("tipo", "descripcion", "numero_documento")
    column_labels = {
        "tipo": "Tipo",
        "descripcion": "Descripción",
        "numero_documento": "Número identificador del documento",
    }

    form_columns = ("tipo", "descripcion", "numero_documento")

    form_overrides = {
        "tipo": SelectField,
    }

    form_args = {
        "tipo": {
            "label": "Tipo de documento a registrar",
            "choices": [
                ("1", "DNI"),
                ("2", "RTN"),
                ("3", "Pasaporte"),
                ("4", "Otro"),
            ],
            "coerce": int,
            "validators": [DataRequired(message="Debes seleccionar un tipo de documento.")],
        },
        "descripcion": {
            "label": "Descripción",
            "validators": [DataRequired(message="La descripción es obligatoria.")],
        },
        "numero_documento": {
            "label": "Número identificador del documento",
            "validators": [
                DataRequired(message="El número de documento es obligatorio."),
                Regexp("^[0-9]+$", message="Solo se permiten dígitos."),
            ],
        },
    }

    form_widget_args = {
        "descripcion": {
            "data-validacion": "descripcion",
            "id": "doc_descripcion",
        },
        "numero_documento": {
            "id": "doc_numero",
            "inputmode": "numeric",
            "pattern": "[0-9]*",
        },
    }

    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "tipo", None) == "gerente"
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))
import re


def _normalizar_texto(raw):
    if raw is None:
        return None
    out = " ".join(str(raw).strip().split())
    return out or None


def validar_tipo_documento(raw):
    if raw is None:
        return None
    if isinstance(raw, float) and not raw.is_integer():
        return None
    s = str(raw).strip()
    if s == "":
        return None
    if not s.isdigit():
        return None
    out = int(s)
    if out not in (1, 2, 3, 4):
        return None
    return out


def validar_descripcion_documento(raw, min_len=3, max_len=60):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if len(out) < int(min_len) or len(out) > int(max_len):
        return None
    if re.search(r"(.)\1\1", out.lower()):
        return None
    if "@" in out:
        return None
    return out


def validar_numero_documento(raw_numero, tipo):
    numero = _normalizar_texto(raw_numero)
    if numero is None:
        return None

    t = validar_tipo_documento(tipo)
    if t is None:
        return None

    if t == 1:
        if not numero.isdigit() or len(numero) != 13:
            return None
        return numero

    if t == 2:
        if not numero.isdigit() or len(numero) != 14:
            return None
        return numero

    if t == 3:
        if not numero.isalnum() or len(numero) != 8:
            return None
        if not numero[0].isalpha():
            return None
        return numero

    if t == 4:
        if not numero.isalnum() or len(numero) < 4:
            return None
        return numero

    return None