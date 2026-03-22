from flask import Blueprint, render_template
from flask_login import current_user
from datetime import datetime
import traceback
from mensajes_logs import logger_

index_admin_bp = Blueprint("index_admin_bp", __name__)


@index_admin_bp.before_request
def _solo_staff():
    from models.permisos_mixin import verificar_tipo
    return verificar_tipo("gerente", "empleado")


@index_admin_bp.route("/index_admin")
def index():
    from flask import redirect, url_for as _url_for
    from models.permisos_mixin import es_admin_panel, pantallas_del_empleado_actual

    # Gerentes y empleados admin van directamente al hub de administración
    if es_admin_panel():
        return redirect(_url_for("ver_permisos_empleado", modulo="permisos_puesto"))

    # Empleados normales: mostrar su panel personal con las pantallas que tienen asignadas
    try:
        permisos = pantallas_del_empleado_actual() or set()
        nombre = (
            getattr(current_user, "nombre", None)
            or getattr(current_user, "Nombre", None)
            or "Usuario"
        )
        tipo = getattr(current_user, "tipo", None)
        return render_template(
            "index_admin.html",
            pantallas_permitidas=permisos,
            nombre_usuario=nombre,
            tipo_usuario=tipo,
        )
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "index_admin", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "index_admin", fecha)
        return "Error al abrir el panel.", 500
