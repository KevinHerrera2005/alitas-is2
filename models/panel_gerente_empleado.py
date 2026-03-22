from flask import Blueprint, render_template
from datetime import datetime
import traceback
from mensajes_logs import logger_

panel_gerente_emp = Blueprint("panel_gerente_emp", __name__)


@panel_gerente_emp.before_request
def _solo_empleado():
    from models.permisos_mixin import verificar_tipo
    return verificar_tipo("empleado")


@panel_gerente_emp.route("/panel_gerente_empleado")
def panel():
    try:
        from models.permisos_mixin import pantallas_del_empleado_actual
        pantallas_permitidas = pantallas_del_empleado_actual() or set()
        return render_template("panel_gerente_empleado.html", pantallas_permitidas=pantallas_permitidas)
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "panel_gerente_emp", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_gerente_emp", fecha)
        return "Error al abrir el panel.", 500
