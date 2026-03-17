from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from flask_login import current_user
from mensajes_logs import logger_
from datetime import datetime
import traceback

from models.Pantallas_model import Pantallas
from models.estado_pantalla_empleado_model import EstadoPantallaEmpleado
from models.permisos_puesto_model import PermisosPuesto
from models.pantallas_acciones_model import PantallasAcciones

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
        logger_.Logger.add_to_log("error", str(error), "panel_jefe", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_jefe", fecha)

    # Pantallas del puesto del empleado (las que le corresponden por PermisosPuesto)
    try:
        id_empleado = getattr(current_user, "db_id", None) or getattr(current_user, "ID_Empleado", None)
        id_puesto = current_user.id_puesto

        # IDs de pantallas asignadas al puesto
        ids_pantallas_del_puesto = {r[0] for r in db.session.query(Pantallas.ID_Pantalla).join(
            PantallasAcciones, PantallasAcciones.ID_Pantalla == Pantallas.ID_Pantalla
        ).join(
            PermisosPuesto, PermisosPuesto.ID_Pantalla_Accion == PantallasAcciones.ID_Pantalla_Accion
        ).filter(
            PermisosPuesto.ID_Puesto == id_puesto
        ).distinct().all()}

        if not ids_pantallas_del_puesto:
            pantallas_permitidas = set()
        else:
            # Pantallas explícitamente activas (activa=1)
            activadas = {r[0] for r in db.session.query(Pantallas.url).join(
                EstadoPantallaEmpleado, EstadoPantallaEmpleado.ID_Pantalla == Pantallas.ID_Pantalla
            ).filter(
                EstadoPantallaEmpleado.ID_Empleado == int(id_empleado),
                EstadoPantallaEmpleado.activa == 1,
                Pantallas.ID_Pantalla.in_(ids_pantallas_del_puesto)
            ).all()}

            # Pantallas del puesto sin registro aún = activas por defecto
            ids_con_registro = {r[0] for r in db.session.query(EstadoPantallaEmpleado.ID_Pantalla).filter(
                EstadoPantallaEmpleado.ID_Empleado == int(id_empleado),
                EstadoPantallaEmpleado.ID_Pantalla.in_(ids_pantallas_del_puesto)
            ).all()}
            sin_registro = {r[0] for r in db.session.query(Pantallas.url).filter(
                Pantallas.ID_Pantalla.in_(ids_pantallas_del_puesto - ids_con_registro)
            ).all()}

            pantallas_permitidas = activadas | sin_registro
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "panel_jefe_permisos", fecha)
        pantallas_permitidas = set()

    return render_template('panel_jefe_de_cocina.html', pantallas_permitidas=pantallas_permitidas)
