from decimal import Decimal

from flask import request, jsonify, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from sqlalchemy import text

from models import db
from models.carrito_model import Carrito
from models.in_re_model import IN_RE
from models.receta_model import Receta
from models.usuario_cliente_model import UsuarioCliente
from models.direccion_cliente_model import DireccionDelCliente
from models.direccion_model import Direccion
from models.metodos_money_model import MetodosMoney
from models.pagos_cliente_model import PagosCliente
from models.empleado_model import Empleado
from models.orden_entrega_model import OrdenEntrega


ID_PUESTO_REPARTIDOR = 4
MAX_CANTIDAD_POR_INSUMO = 20
def _cliente_valido(id_cliente):
    return id_cliente is not None
def _limite_cantidad(cantidad_actual, cantidad_a_agregar, limite=MAX_CANTIDAD_POR_INSUMO):
    if cantidad_actual is None:
        cantidad_actual = 0
    if cantidad_a_agregar is None:
        return False
    try:
        cantidad_actual = int(cantidad_actual)
        cantidad_a_agregar = int(cantidad_a_agregar)
        limite = int(limite)
    except Exception:
        return False
    if cantidad_a_agregar < 0:
        return False
    return (cantidad_actual + cantidad_a_agregar) <= limite

def carrito_routes(app):
    def _obtener_id_cliente():
        cid = session.get("cliente_id")
        if cid:
            return cid
        if current_user.is_authenticated and hasattr(current_user, "ID_Usuario_ClienteF"):
            return current_user.ID_Usuario_ClienteF
        return None

    def _obtener_repartidor_disponible(id_sucursal: int):
        if not id_sucursal:
            return None

        repartidores = (
            Empleado.query
            .filter(
                Empleado.ID_Puesto == ID_PUESTO_REPARTIDOR,
                Empleado.ID_sucursal == id_sucursal,
                Empleado.estado == 1,
            )
            .all()
        )

        if not repartidores:
            return None

        for rep in repartidores:
            activos = (
                OrdenEntrega.query
                .filter(
                    OrdenEntrega.ID_Empleado_Repartidor == rep.ID_Empleado,
                    OrdenEntrega.estado.in_([0, 1, 2]),
                )
                .count()
            )
            if activos < 5:
                return rep

        return None

    @app.route("/carrito/agregar", methods=["POST"])
    @login_required
    def carrito_agregar():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            return jsonify({"ok": False, "redirect": url_for("login")}), 401

        data = request.get_json() or {}
        id_in_re = data.get("id_in_re")

        if not id_in_re:
            return jsonify({"ok": False, "error": "Falta id_in_re"}), 400

        insumo_receta = IN_RE.query.get(id_in_re)
        if not insumo_receta:
            return jsonify({"ok": False, "error": "Registro no encontrado"}), 404

        precio_valor = getattr(insumo_receta, "precio_venta", None)
        if precio_valor is None:
            precio_valor = getattr(insumo_receta, "precio", None)

        if precio_valor is None:
            id_receta = getattr(insumo_receta, "ID_Receta", None) or getattr(
                insumo_receta, "id_receta", None
            )
            if id_receta is not None:
                total_costo = db.session.execute(
                    text(
                        """
                        SELECT 
                            SUM(
                                (i.precio_lempiras / NULLIF(i.peso_individual, 0))
                                * ir.cantidad_usada
                            ) AS total
                        FROM IN_RE ir
                        JOIN Insumos i ON i.ID_Insumo = ir.ID_Insumo
                        WHERE ir.ID_Receta = :id_receta
                          AND ir.Activo = 1
                        """
                    ),
                    {"id_receta": id_receta},
                ).scalar()
                if total_costo is not None:
                    precio_valor = total_costo

        if precio_valor is None:
            return jsonify({"ok": False, "error": "El precio no está definido"}), 400

        precio_unitario = Decimal(str(precio_valor))

        linea = Carrito.query.filter_by(
            ID_Usuario_ClienteF=id_cliente,
            ID_IN_RE=id_in_re,
        ).first()

        if linea:
            if not _limite_cantidad(linea.Cantidad, 1, limite=20):
                return jsonify({"ok": False, "error": "No puedes agregar más de 20 de este producto"}), 400
            linea.Cantidad += 1
            linea.total = precio_unitario * linea.Cantidad
        else:
            if not _limite_cantidad(0, 1, limite=20):
                return jsonify({"ok": False, "error": "No puedes agregar más de 20 de este producto"}), 400
            linea = Carrito(
                ID_Usuario_ClienteF=id_cliente,
                ID_IN_RE=id_in_re,
                Cantidad=1,
                total=precio_unitario,
            )
            db.session.add(linea)

        db.session.commit()

        total_general = (
            db.session.query(db.func.coalesce(db.func.sum(Carrito.total), 0))
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .scalar()
        )
        total_items = (
            db.session.query(db.func.coalesce(db.func.sum(Carrito.Cantidad), 0))
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .scalar()
        )

        return jsonify(
            {
                "ok": True,
                "total_general": float(total_general),
                "total_items": int(total_items),
            }
        )

    @app.route("/carrito/actualizar", methods=["POST"])
    @login_required
    def carrito_actualizar():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            return jsonify({"ok": False, "redirect": url_for("login")}), 401

        data = request.get_json() or {}
        id_carrito = data.get("id_carrito")
        accion = data.get("accion")

        if not id_carrito or accion not in ("sumar", "restar"):
            return jsonify({"ok": False, "error": "Datos inválidos"}), 400

        linea = Carrito.query.filter_by(
            ID_Carrito=id_carrito,
            ID_Usuario_ClienteF=id_cliente,
        ).first()

        if not linea:
            return jsonify({"ok": False, "error": "Línea no encontrada"}), 404

        eliminado = False

        if accion == "restar" and linea.Cantidad <= 1:
            db.session.delete(linea)
            db.session.commit()
            eliminado = True
        else:
            cantidad_actual = linea.Cantidad or 0
            if cantidad_actual <= 0:
                cantidad_actual = 1

            if linea.total is not None and cantidad_actual > 0:
                unitario = linea.total / cantidad_actual
            else:
                detalle = IN_RE.query.get(linea.ID_IN_RE)
                valor = None
                if detalle is not None:
                    valor = getattr(detalle, "precio_venta", None) or getattr(
                        detalle, "precio", None
                    )
                unitario = Decimal(str(valor or "0"))

            if accion == "sumar":
                nueva = cantidad_actual + 1
            else:
                nueva = max(0, cantidad_actual - 1)

            if nueva <= 0:
                db.session.delete(linea)
                db.session.commit()
                eliminado = True
            else:
                linea.Cantidad = nueva
                linea.total = unitario * nueva
                db.session.commit()

        total_general = (
            db.session.query(db.func.coalesce(db.func.sum(Carrito.total), 0))
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .scalar()
        )
        total_items = (
            db.session.query(db.func.coalesce(db.func.sum(Carrito.Cantidad), 0))
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .scalar()
        )

        if eliminado:
            return jsonify(
                {
                    "ok": True,
                    "deleted": True,
                    "linea": {"id_carrito": id_carrito},
                    "total_general": float(total_general),
                    "total_items": int(total_items),
                }
            )

        return jsonify(
            {
                "ok": True,
                "deleted": False,
                "linea": {
                    "id_carrito": linea.ID_Carrito,
                    "cantidad": int(linea.Cantidad),
                    "subtotal": float(linea.total),
                },
                "total_general": float(total_general),
                "total_items": int(total_items),
            }
        )

    @app.route("/carrito/resumen")
    @login_required
    def carrito_resumen():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            return redirect(url_for("login"))

        filas = (
            db.session.query(Carrito, IN_RE, Receta)
            .join(IN_RE, Carrito.ID_IN_RE == IN_RE.ID_IN_RE)
            .join(Receta, IN_RE.ID_Receta == Receta.ID_Receta)
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .all()
        )

        items = []
        total_general = Decimal("0")

        for linea, detalle, receta in filas:
            nombre = getattr(receta, "Nombre_receta", None) or getattr(
                receta, "nombre_receta", None
            ) or f"Receta {receta.ID_Receta}"

            precio_unit = getattr(detalle, "precio_venta", None)
            if precio_unit is None:
                precio_unit = getattr(detalle, "precio", None)
            if precio_unit is None and linea.Cantidad:
                precio_unit = linea.total / linea.Cantidad

            subtotal = linea.total
            total_general += subtotal

            items.append(
                {
                    "id_carrito": linea.ID_Carrito,
                    "nombre": nombre,
                    "cantidad": linea.Cantidad,
                    "precio_unit": precio_unit,
                    "subtotal": subtotal,
                }
            )

        return render_template(
            "carrito/panel.html",
            items=items,
            total_general=total_general,
        )

    @app.route("/carrito/estado")
    def carrito_estado():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            return jsonify({"ok": False, "total_general": 0, "total_items": 0})

        total_general = (
            db.session.query(db.func.coalesce(db.func.sum(Carrito.total), 0))
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .scalar()
        )
        total_items = (
            db.session.query(db.func.coalesce(db.func.sum(Carrito.Cantidad), 0))
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .scalar()
        )

        return jsonify(
            {
                "ok": True,
                "total_general": float(total_general),
                "total_items": int(total_items),
            }
        )

    @app.route("/carrito/checkout")
    @login_required
    def carrito_checkout():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            return redirect(url_for("login"))

        cliente = UsuarioCliente.query.get(id_cliente)
        if not cliente:
            session.pop("checkout_sucursal_id", None)
            return redirect(url_for("carrito_resumen"))

        id_sucursal_cliente = (
            getattr(cliente, "ID_sucursal", None)
            or getattr(cliente, "id_sucursal", None)
        )

        if not id_sucursal_cliente:
            session.pop("checkout_sucursal_id", None)
            return redirect(url_for("carrito_resumen"))

        session["checkout_sucursal_id"] = int(id_sucursal_cliente)

        repartidor_disponible = _obtener_repartidor_disponible(id_sucursal_cliente)
        if not repartidor_disponible:
            flash(
                "En este momento no hay repartidores disponibles para tu sucursal. "
                "Por favor intenta de nuevo más tarde.",
                "warning",
            )
        filas = (
            db.session.query(Carrito, IN_RE, Receta)
            .join(IN_RE, Carrito.ID_IN_RE == IN_RE.ID_IN_RE)
            .join(Receta, IN_RE.ID_Receta == Receta.ID_Receta)
            .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
            .all()
        )

        items = []
        total_general = Decimal("0")

        for linea, detalle, receta in filas:
            nombre = getattr(receta, "Nombre_receta", None) or getattr(
                receta, "nombre_receta", None
            ) or f"Receta {receta.ID_Receta}"

            precio_unit = getattr(detalle, "precio_venta", None)
            if precio_unit is None:
                precio_unit = getattr(detalle, "precio", None)
            if precio_unit is None and linea.Cantidad:
                precio_unit = linea.total / linea.Cantidad

            subtotal = linea.total
            total_general += subtotal

            items.append(
                {
                    "id_carrito": linea.ID_Carrito,
                    "nombre": nombre,
                    "cantidad": linea.Cantidad,
                    "precio_unit": precio_unit,
                    "subtotal": subtotal,
                }
            )

        cliente_nombre = (
            getattr(cliente, "Nombre", None)
            or getattr(cliente, "nombre", None)
            or ""
        )
        cliente_apellido = (
            getattr(cliente, "Apellido", None)
            or getattr(cliente, "apellido", None)
            or ""
        )

        metodos_pago = (
            MetodosMoney.query
            .order_by(MetodosMoney.Tipo)
            .all()
        )

        tarjetas_view = []
        tarjetas_db = (
            PagosCliente.query
            .filter(
                PagosCliente.ID_Usuario_ClienteF == id_cliente,
                PagosCliente.Numero_tarjeta.isnot(None),
            )
            .order_by(PagosCliente.ID_Pago.desc())
            .all()
        )

        for t in tarjetas_db:
            ult4 = (t.Numero_tarjeta or "").strip()
            label = f"{t.a_nombre_de or 'Sin nombre'} – termina en {ult4 or 'XXXX'}"
            tarjetas_view.append(
                {
                    "id_pago": t.ID_Pago,
                    "label": label,
                }
            )

        direcciones = []
        filas_dir = (
            db.session.query(DireccionDelCliente, Direccion)
            .join(Direccion, Direccion.ID_Direccion == DireccionDelCliente.ID_Direccion)
            .filter(DireccionDelCliente.ID_Usuario_ClienteF == id_cliente)
            .all()
        )

        for dc, dir_obj in filas_dir:
            direcciones.append(
                {
                    "id": dir_obj.ID_Direccion,
                    "texto": dir_obj.Descripcion,
                }
            )

        return render_template(
            "carrito/checkout.html",
            items=items,
            total_general=total_general,
            cliente_nombre=cliente_nombre,
            cliente_apellido=cliente_apellido,
            metodos_pago=metodos_pago,
            direcciones=direcciones,
            tarjetas=tarjetas_view,
            repartidor_disponible=bool(repartidor_disponible),
        )
def _in_re_valido(insumo_receta):
    return insumo_receta is not None

def _hay_repartidor_disponible(repartidor):
    return repartidor is not None


def _repartidor_misma_sucursal(id_sucursal_cliente, id_sucursal_repartidor):
    if id_sucursal_cliente is None or id_sucursal_repartidor is None:
        return False
    try:
        return int(id_sucursal_cliente) == int(id_sucursal_repartidor)
    except Exception:
        return False