from flask import render_template, redirect, url_for, session
from flask_login import login_required, current_user
import re
from wtforms.validators import ValidationError

from models import db
from models.direccion_model import Direccion
from models.direccion_cliente_model import DireccionDelCliente


def _obtener_id_cliente():
    cid = session.get("cliente_id")
    if cid:
        return cid
    if current_user.is_authenticated and hasattr(current_user, "ID_Usuario_ClienteF"):
        return current_user.ID_Usuario_ClienteF
    return None


def tus_direcciones_routes(app):
    @app.route("/tus-direcciones", endpoint="tus_direcciones")
    @login_required
    def tus_direcciones():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            return redirect(url_for("login"))

        filas = (
            db.session.query(
                DireccionDelCliente.ID_US_CO.label("numero"),
                Direccion.Descripcion.label("descripcion"),
            )
            .join(
                Direccion,
                Direccion.ID_Direccion == DireccionDelCliente.ID_Direccion,
            )
            .filter(DireccionDelCliente.ID_Usuario_ClienteF == id_cliente)
            .order_by(DireccionDelCliente.ID_US_CO)
            .all()
        )

        return render_template("tusdirecciones.html", direcciones=filas)
def _tiene_tres_iguales_seguidos(texto):
    if texto is None:
        return False
    s = str(texto)
    for i in range(len(s) - 2):
        if s[i] == s[i + 1] == s[i + 2]:
            return True
    return False


def validar_descripcion_direccion(valor, max_len=300):
    if valor is None:
        raise ValidationError("La descripción es obligatoria.")
    valor = str(valor)
    if valor.strip() == "":
        raise ValidationError("La descripción no puede estar vacía.")
    if len(valor.strip()) > max_len:
        raise ValidationError(f"La descripción no puede superar {max_len} caracteres.")
    if _tiene_tres_iguales_seguidos(valor):
        raise ValidationError("La descripción no puede tener 3 caracteres iguales seguidos.")
    return valor.strip()