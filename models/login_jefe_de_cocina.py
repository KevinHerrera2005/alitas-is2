from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from sqlalchemy import text
from flask_login import login_required, current_user
from mensajes_logs import logger_
from datetime import datetime
import traceback

bp_login_jefe = Blueprint('login_jefe', __name__, url_prefix='/login_jefe')

@bp_login_jefe.route('/', methods=['GET', 'POST'])
def login_jefe():
    return redirect(url_for('login'))

@bp_login_jefe.route('/panel')
def panel_jefe():
    try:
        if getattr(current_user, "tipo", None) != "empleado" or current_user.id_puesto != 1:
            flash("No tienes permiso para acceder a este panel.", "danger")
            return redirect(url_for('pagina_principal_bp.menu'))
    except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "gestion_receta_volver_al_menu", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "gestion_receta_volver_al_menu", fecha)

    return render_template('panel_jefe_de_cocina.html')
