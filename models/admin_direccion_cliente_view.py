from flask_admin.contrib.sqla import ModelView
from flask import request, url_for, session
from flask_login import current_user
from wtforms.validators import ValidationError
from sqlalchemy import text

from models import db
from models.direccion_cliente_model import DireccionDelCliente


class DireccionDelClienteAdmin(ModelView):
    base_template = "admin/direccion_master.html"
    create_template = "admin/model/direccion_cliente_create.html"
    edit_template = "admin/model/direccion_cliente_edit.html"

    can_view_details = False
    can_export = False

    name = "Ver mis direcciones"
    category = None

    column_list = (
        "ID_US_CO",
        "Descripcion",
    )

    column_labels = {
        "ID_US_CO": "Número",
        "Descripcion": "Dirección",
    }

    column_searchable_list = ("Descripcion",)

    form_columns = (
        "Descripcion",
    )

    form_widget_args = {
        "Descripcion": {
            "id": "direccion_textarea",
            "data-validacion": "descripcion",
        }
    }

    column_default_sort = ("ID_US_CO", True)

    def _get_usuario_id(self):
        user_id = session.get("ID_Usuario_ClienteF")
        if user_id:
            return user_id
        if hasattr(current_user, "ID_Usuario_ClienteF") and current_user.ID_Usuario_ClienteF:
            return current_user.ID_Usuario_ClienteF
        if hasattr(current_user, "id") and current_user.id:
            return current_user.id
        user_id = session.get("usuario_id") or session.get("cliente_id") or session.get("id_usuario")
        return user_id

    def get_query(self):
        query = super().get_query()
        user_id = self._get_usuario_id()
        if not user_id:
            return query.filter(False)
        return query.filter(self.model.ID_Usuario_ClienteF == user_id)

    def get_count_query(self):
        query = super().get_count_query()
        user_id = self._get_usuario_id()
        if not user_id:
            return query.filter(False)
        return query.filter(self.model.ID_Usuario_ClienteF == user_id)

    def on_model_change(self, form, model, is_created):
        user_id = self._get_usuario_id()
        if not user_id:
            raise ValidationError("No se pudo identificar al cliente actual. Inicie sesión antes de crear una dirección.")
        descripcion = (model.Descripcion or "").strip()
        if not descripcion:
            raise ValidationError("La descripción de la dirección es obligatoria.")
        result = db.session.execute(
            text("INSERT INTO Direcciones (descripcion) OUTPUT INSERTED.ID_Direccion VALUES (:desc)"),
            {"desc": descripcion}
        )
        id_direccion = result.scalar()
        model.ID_Usuario_ClienteF = user_id
        model.ID_Direccion = id_direccion

    def get_save_return_url(self, model, is_created):
        next_url = request.args.get("next")
        if next_url:
            return next_url
        return url_for("carrito_checkout")
