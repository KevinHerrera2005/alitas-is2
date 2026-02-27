from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from sqlalchemy import text
from flask_login import login_required, current_user

bp_login_jefe = Blueprint('login_jefe', __name__, url_prefix='/login_jefe')

@bp_login_jefe.route('/', methods=['GET', 'POST'])
def login_jefe():
    return redirect(url_for('login'))

@bp_login_jefe.route('/panel')
@login_required
def panel_jefe():
    if getattr(current_user, "tipo", None) != "empleado" or current_user.id_puesto != 1:
        flash("No tienes permiso para acceder a este panel.", "danger")
        return redirect(url_for('pagina_principal_bp.menu'))

    return render_template('panel_jefe_de_cocina.html')
