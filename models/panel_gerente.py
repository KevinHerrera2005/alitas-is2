from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

panel_gerente = Blueprint("panel_gerente", __name__, url_prefix="/gerente")


def _tiene_permiso_gerente():
    if getattr(current_user, "tipo", None) == "gerente":
        return True
    if getattr(current_user, "tipo", None) == "empleado" and getattr(current_user, "id_puesto", None) == 16:
        return True
    return False


@panel_gerente.route("/")
def root():
    if getattr(current_user, "is_authenticated", False):
        return redirect(url_for("panel_gerente.panel"))
    return redirect(url_for("login"))


@panel_gerente.route("/panel")
@login_required
def panel():
    if not _tiene_permiso_gerente():
        flash("No tienes permiso para acceder a este panel.", "danger")
        return redirect(url_for("pagina_principal_bp.menu"))
    return render_template("panel_gerente.html")
