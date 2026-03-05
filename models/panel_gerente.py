from datetime import datetime
import traceback

from mensajes_logs import logger_

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

panel_gerente = Blueprint("panel_gerente", __name__, url_prefix="/gerente")


# Este botón sirve para entrar a la raíz del panel gerente.
@panel_gerente.route("/")
def root():
    try:
        if getattr(current_user, "is_authenticated", False):
            return redirect(url_for("panel_gerente.panel"))
        return redirect(url_for("login"))
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "panel_gerente_root", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_gerente_root", fecha)
        return "Error al abrir la raíz del panel gerente.", 500


# Este botón sirve para abrir el panel del gerente.
@panel_gerente.route("/panel")
def panel():
    try:
        return render_template("panel_gerente.html")
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "panel_gerente_panel", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_gerente_panel", fecha)
        return "Error al abrir el panel del gerente.", 500