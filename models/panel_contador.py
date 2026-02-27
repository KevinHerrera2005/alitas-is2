from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

panel_contador = Blueprint("panel_contador", __name__)

@panel_contador.route("/panel_contador")
@login_required
def panel():

    if getattr(current_user, "tipo", None) != "empleado" or getattr(current_user, "id_puesto", None) != 10:
        flash("No tienes permiso para acceder a este panel.", "danger")
        return redirect(url_for("pagina_principal_bp.menu"))

    return render_template("panel_contador.html")
