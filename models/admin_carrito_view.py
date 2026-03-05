from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash

from models.carrito_model import Carrito


class CarritoAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True
    can_export = True

    column_list = (
        "ID_Carrito",
        "ID_Usuario_ClienteF",
        "ID_IN_RE",
        "Cantidad",
        "total",
    )

    column_default_sort = ("ID_Carrito", True)

    column_labels = {
        "ID_Carrito": "ID Carrito",
        "ID_Usuario_ClienteF": "Cliente",
        "ID_IN_RE": "ID IN_RE",
        "Cantidad": "Cantidad",
        "total": "Total línea",
    }


