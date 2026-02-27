from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, current_user

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


def crear_direcciones_routes(app):
    @app.route("/direcciones/nueva", methods=["GET", "POST"])
    @login_required
    def crear_direccion():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            return redirect(url_for("login"))

        if request.method == "POST":
            descripcion = request.form.get("descripcion", "").strip()
            if not descripcion:
                return render_template("crear_direcciones.html", error="La descripción es obligatoria.")

            nueva_dir = Direccion(Descripcion=descripcion)
            db.session.add(nueva_dir)
            db.session.flush()

            enlace = DireccionDelCliente(
                ID_Usuario_ClienteF=id_cliente,
                ID_Direccion=nueva_dir.ID_Direccion,
            )
            db.session.add(enlace)
            db.session.commit()

            return redirect(url_for("carrito_checkout"))

        return render_template("crear_direcciones.html", error=None)
