from datetime import datetime

from flask import Blueprint, flash, redirect, url_for, request, session, render_template
from flask_login import login_required, current_user

from models import db
from models.orden_entrega_model import OrdenEntrega
from models.historial_ordenes_repartidor_model import HistorialOrdenesRepartidor

cancelar_bp = Blueprint("cancelar_bp", __name__)

def _cliente_id():
    for k in ("cliente_id", "ID_Usuario_ClienteF", "id_cliente", "usuario_cliente_id"):
        v = session.get(k)
        if v is not None:
            try:
                return int(v)
            except Exception:
                pass

    if getattr(current_user, "is_authenticated", False):
        tipo = getattr(current_user, "tipo", None)
        if tipo and tipo != "cliente":
            return None

        for attr in ("ID_Usuario_ClienteF", "id_usuario_cliente", "Usuario_ClienteID", "db_id", "id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass

    return None

def _upsert_historial_cancelacion(orden, motivo):
    orden_id = getattr(orden, "ID_Orden_Entrega", None)
    repartidor_id = getattr(orden, "ID_Empleado_Repartidor", None)

    if not orden_id:
        return

    existente = HistorialOrdenesRepartidor.query.filter_by(ID_Orden=int(orden_id)).first()
    if existente:
        existente.Estado_Final = 4
        existente.Fecha_Finalizacion = datetime.utcnow()
        existente.Observacion = motivo or None
        db.session.add(existente)
        return

    db.session.add(
        HistorialOrdenesRepartidor(
            ID_Orden=int(orden_id),
            ID_Repartidor=int(repartidor_id) if repartidor_id is not None else 0,
            Estado_Final=4,
            Fecha_Finalizacion=datetime.utcnow(),
            Observacion=motivo or None,
        )
    )

@cancelar_bp.route("/cancelar/<int:orden_id>", methods=["GET", "POST"])
@login_required
def cancelar(orden_id):
    cid = _cliente_id()
    if not cid:
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for("login"))

    next_url = (request.args.get("next") or "").strip()

    orden = OrdenEntrega.query.get(int(orden_id))
    if not orden or int(getattr(orden, "ID_Usuario_ClienteF", 0) or 0) != int(cid):
        flash("No puedes cancelar esta orden.", "danger")
        return redirect(next_url or url_for("mis_pedidos_bp.mis_pedidos"))

    estado_actual = int(getattr(orden, "estado", 0) or 0)

    if estado_actual == 3:
        flash("No se puede cancelar una orden entregada.", "danger")
        return redirect(next_url or url_for("mis_pedidos_bp.mis_pedidos"))

    if estado_actual == 4:
        flash("Esta orden ya está cancelada.", "danger")
        return redirect(next_url or url_for("mis_pedidos_bp.mis_pedidos"))

    if request.method == "GET":
        return render_template(
            "cancelar.html",
            orden=orden,
            next=next_url or url_for("mis_pedidos_bp.mis_pedidos"),
        )

    motivo = (request.form.get("motivo") or "").strip()
    if not motivo:
        motivo = "Cancelado por el cliente"

    orden.estado = 4
    orden.Motivo_Cancelacion = motivo

    _upsert_historial_cancelacion(orden, motivo)

    db.session.add(orden)
    db.session.commit()

    flash("Tu pedido fue cancelado.", "success")
    return redirect(next_url or url_for("mis_pedidos_bp.mis_pedidos"))
