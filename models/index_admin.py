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
    try:
        tipo = getattr(current_user, "tipo", None)
        id_puesto = (
            getattr(current_user, "id_puesto", None)
            or getattr(current_user, "ID_Puesto", None)
        )

        if tipo == "gerente" and not id_puesto:
            # Gerente sin puesto asignado → acceso total
            pantallas_permitidas = None
        else:
            from models.permisos_mixin import pantallas_del_empleado_actual
            pantallas_permitidas = pantallas_del_empleado_actual() or set()

        nombre = (
            getattr(current_user, "nombre", None)
            or getattr(current_user, "Nombre", None)
            or "Usuario"
        )
        return render_template(
            "index_admin.html",
            pantallas_permitidas=pantallas_permitidas,
            nombre_usuario=nombre,
            tipo_usuario=tipo,
        )
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "index_admin", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "index_admin", fecha)
        return "Error al abrir el panel.", 500
