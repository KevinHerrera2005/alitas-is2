from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date, datetime
import re
import traceback
from mensajes_logs import logger_

panel_repartidor = Blueprint("panel_repartidor", __name__)


@panel_repartidor.route("/panel_repartidor")
def panel():
    try:
        if (
            getattr(current_user, "tipo", None) != "empleado"
            or getattr(current_user, "id_puesto", None) != 4
        ):
            flash("No tienes permiso para acceder a este panel.", "danger")
            return redirect(url_for("pagina_principal_bp.menu"))

        return render_template("panel_repartidor.html")
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "panel_repartidor", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_repartidor", fecha)