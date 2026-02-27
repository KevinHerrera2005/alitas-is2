from flask_admin.contrib.sqla import ModelView
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp
from flask_login import current_user

class UsuarioClienteAdmin(ModelView):
    column_list = ("Username", "nombre", "apellido", "telefono", "ID_sucursal", "estado")
    column_searchable_list = ("Username", "nombre", "apellido", "telefono")
    column_filters = ("Username", "nombre", "apellido", "telefono", "estado")

    column_labels = {
        "Username": "Usuario",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "telefono": "Teléfono",
        "ID_sucursal": "Sucursal",
        "estado": "Estado",
    }

    form_overrides = {
        "Username": StringField,
        "nombre": StringField,
        "apellido": StringField,
        "telefono": StringField,
    }

    form_args = {
        "Username": {"validators": [DataRequired(), Length(3, 50)]},
        "nombre": {"validators": [DataRequired(), Length(3, 50)]},
        "apellido": {"validators": [DataRequired(), Length(3, 50)]},
        "telefono": {
            "validators": [
                DataRequired(),
                Regexp(r"^[3789]\d{7}$", message="Teléfono inválido"),
            ]
        },
    }

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "is_admin", False)
