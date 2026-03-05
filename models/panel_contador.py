from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from mensajes_logs import logger_
from datetime import datetime
import traceback

panel_contador = Blueprint("panel_contador", __name__)

@panel_contador.route("/panel_contador")
@login_required
def panel():
    try:
        return render_template("panel_contador.html")
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "orden_entrega_eliminar", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "orden_entrega_eliminar", fecha)