from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from collections import defaultdict

from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from wtforms.validators import ValidationError
from models import db
from models.cai_model import CAI
from models.factura_model import Factura
from models.factura_detalle_model import FacturaDetalle
from models.empleado_model import Empleado
from models.sucursal_model import Sucursal
from models.carrito_model import Carrito
from models.in_re_model import IN_RE
from models.receta_model import Receta
from models.usuario_cliente_model import UsuarioCliente
from models.direccion_cliente_model import DireccionDelCliente
from models.direccion_model import Direccion
from models.insumo_model import Insumo
from models.parametro_sar_model import ParametroSAR
from models.metodos_money_model import MetodosMoney
from models.pagos_cliente_model import PagosCliente
from models.orden_entrega_model import OrdenEntrega
from models.pago_detalle_model import PagoDetalle


ID_PUESTO_CAJERO = 13
ID_PUESTO_REPARTIDOR = 4


def obtener_cajero_por_sucursal(id_sucursal: int):
    if not id_sucursal:
        return None

    return (
        Empleado.query
        .filter(
            Empleado.ID_Puesto == ID_PUESTO_CAJERO,
            Empleado.ID_sucursal == id_sucursal,
            Empleado.estado == 1,
        )
        .first()
    )


def obtener_repartidor_disponible(id_sucursal: int):
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


def _obtener_id_cliente():
    cid = session.get("cliente_id")
    if cid:
        return cid

    if current_user.is_authenticated and hasattr(current_user, "ID_Usuario_ClienteF"):
        return current_user.ID_Usuario_ClienteF

    return None


def _obtener_parametro_sar(id_parametro: int, default: str) -> str:
    try:
        obj = ParametroSAR.query.get(id_parametro)
    except Exception:
        obj = None

    if obj and obj.Valor:
        return str(obj.Valor).strip()

    return default


def _metodo_nombre_y_tipo(metodo: MetodosMoney | None):
    tipo = None
    nombre = None

    if metodo is not None:
        nombre = (
            getattr(metodo, "Nombre", None)
            or getattr(metodo, "nombre", None)
            or getattr(metodo, "Metodo", None)
        )
        tipo = getattr(metodo, "Tipo", None)

    try:
        tipo = int(tipo)
    except Exception:
        tipo = None

    if not nombre and tipo is not None:
        if tipo == 1:
            nombre = "Efectivo"
        elif tipo == 2:
            nombre = "Tarjeta"
        elif tipo == 3:
            nombre = "Mixto"

    if not nombre:
        nombre = "No especificado"

    return nombre, tipo


def factura_routes(app):
    if "generar_factura" in app.view_functions:
        return
    @app.route("/facturar", methods=["GET"])
    @login_required
    def generar_factura():
        try:
            id_cliente = _obtener_id_cliente()
            if not id_cliente:
                flash("No se pudo identificar el cliente para esta compra.", "danger")
                return redirect(url_for("carrito_checkout"))

            id_sucursal = session.get("checkout_sucursal_id")
            if not id_sucursal:
                flash("No se pudo determinar la sucursal para esta compra.", "danger")
                return redirect(url_for("carrito_checkout"))

            try:
                id_sucursal = int(id_sucursal)
            except (TypeError, ValueError):
                flash("La sucursal seleccionada es inválida.", "danger")
                return redirect(url_for("carrito_checkout"))

            sucursal = (
                Sucursal.query
                .filter_by(ID_sucursal=id_sucursal, estado=1)
                .first()
            )
            if not sucursal:
                flash("La sucursal seleccionada no existe o está inactiva.", "danger")
                return redirect(url_for("carrito_checkout"))

            empleado_cajero = obtener_cajero_por_sucursal(id_sucursal)
            if not empleado_cajero:
                flash("No hay cajeros disponibles para tu sucursal.", "danger")
                return redirect(url_for("carrito_checkout"))

            repartidor = obtener_repartidor_disponible(id_sucursal)
            if not repartidor:
                flash(
                    "En este momento no hay repartidores disponibles para tu sucursal. "
                    "Por favor intenta de nuevo más tarde.",
                    "danger",
                )
                return redirect(url_for("carrito_checkout"))

            telefono_emisor = (
                getattr(empleado_cajero, "Telefono", None)
                or getattr(empleado_cajero, "telefono", None)
                or "N/A"
            )

            hoy = date.today()
            cai = (
                CAI.query.filter(
                    CAI.ID_sucursal == id_sucursal,
                    CAI.estado == 1,
                    CAI.Fecha_Emision <= hoy,
                    CAI.Fecha_Final >= hoy,
                )
                .first()
            )

            if not cai:
                flash(
                    "No hay un CAI activo o vigente para la sucursal seleccionada.",
                    "danger",
                )
                return redirect(url_for("carrito_checkout"))

            if cai.Secuencia >= cai.Rango_Final:
                flash(
                    "El rango de facturación del CAI se ha agotado para esta sucursal.",
                    "danger",
                )
                return redirect(url_for("carrito_checkout"))

            codigo_factura = _obtener_parametro_sar(1, "01")
            codigo_caja = _obtener_parametro_sar(5, "001")
            rtn_emisor = _obtener_parametro_sar(4, "00000000000000")

            codigo_factura = "".join(ch for ch in codigo_factura if ch.isdigit()) or "01"
            codigo_caja = "".join(ch for ch in codigo_caja if ch.isdigit()) or "001"

            filas = (
                db.session.query(Carrito, IN_RE, Receta)
                .join(IN_RE, Carrito.ID_IN_RE == IN_RE.ID_IN_RE)
                .join(Receta, IN_RE.ID_Receta == Receta.ID_Receta)
                .filter(Carrito.ID_Usuario_ClienteF == id_cliente)
                .all()
            )

            if not filas:
                flash("Tu carrito está vacío, no se puede generar la factura.", "danger")
                return redirect(url_for("carrito_checkout"))

            items = []
            total_general = Decimal("0")
            consumo_por_insumo = defaultdict(Decimal)

            for linea, detalle, receta in filas:
                nombre_receta = (
                    getattr(receta, "Nombre_receta", None)
                    or getattr(receta, "nombre_receta", None)
                    or f"Receta {receta.ID_Receta}"
                )

                precio_unit = getattr(detalle, "precio_final", None)
                if precio_unit is None and linea.Cantidad:
                    precio_unit = linea.total / linea.Cantidad

                subtotal_linea = linea.total
                total_general += Decimal(subtotal_linea)

                items.append(
                    {
                        "id_in_re": linea.ID_IN_RE,
                        "nombre": nombre_receta,
                        "cantidad": linea.Cantidad,
                        "precio_unit": precio_unit,
                        "subtotal": subtotal_linea,
                    }
                )

                cantidad_vendida = Decimal(linea.Cantidad or 0)
                if cantidad_vendida > 0:
                    id_insumo = detalle.ID_Insumo
                    cantidad_usada = Decimal(detalle.cantidad_usada or 0)
                    if id_insumo and cantidad_usada > 0:
                        consumo_por_insumo[id_insumo] += (
                            cantidad_vendida * cantidad_usada
                        )

            if total_general <= 0:
                flash(
                    "El total de la compra es cero, no se puede generar la factura.",
                    "danger",
                )
                return redirect(url_for("carrito_checkout"))

            for id_insumo, cantidad_consumida in consumo_por_insumo.items():
                insumo = Insumo.query.get(id_insumo)
                if not insumo:
                    continue

                stock_actual = Decimal(str(insumo.stock_total or 0))
                if stock_actual < cantidad_consumida:
                    db.session.rollback()
                    flash(
                        "Lo siento, no hay insumos para esa receta ahorita mismo, inténtelo más tarde.",
                        "danger",
                    )
                    return redirect(url_for("carrito_checkout"))

            total_general = total_general.quantize(Decimal("0.01"))
            impuesto_total = (total_general * Decimal("0.15")).quantize(
                Decimal("0.01")
            )
            subtotal_sin_impuesto = (total_general - impuesto_total).quantize(
                Decimal("0.01")
            )

            eee = str(id_sucursal).zfill(3)
            ppp = codigo_caja.zfill(3)[:3]
            tt = codigo_factura.zfill(2)[:2]
            correlativo = str(cai.Secuencia).zfill(6)

            numero_factura = f"{eee}-{ppp}-{tt}-{correlativo}"

            data_req = request.args if request.method == "GET" else request.form

            metodo_id_raw = data_req.get("metodo_pago")
            if not metodo_id_raw or not str(metodo_id_raw).isdigit():
                flash("Selecciona un método de pago para continuar.", "danger")
                return redirect(url_for("carrito_checkout"))

            metodo_id = int(metodo_id_raw)
            metodo = MetodosMoney.query.get(metodo_id)
            if not metodo:
                flash("El método de pago seleccionado es inválido.", "danger")
                return redirect(url_for("carrito_checkout"))

            metodo_nombre, tipo_metodo_num = _metodo_nombre_y_tipo(metodo)

            tarjeta_ult4 = None
            if tipo_metodo_num in (2, 3):
                tarjeta_id_raw = data_req.get("tarjeta_id")
                if not tarjeta_id_raw or not str(tarjeta_id_raw).isdigit():
                    flash("Selecciona una tarjeta para continuar.", "danger")
                    return redirect(url_for("carrito_checkout"))

                pago = (
                    PagosCliente.query
                    .filter(
                        PagosCliente.ID_Pago == int(tarjeta_id_raw),
                        PagosCliente.ID_Usuario_ClienteF == id_cliente,
                    )
                    .first()
                )
                if not pago or not pago.Numero_tarjeta:
                    flash("La tarjeta seleccionada es inválida.", "danger")
                    return redirect(url_for("carrito_checkout"))

                tarjeta_ult4 = str(pago.Numero_tarjeta)[-4:]

            efectivo_db = None
            if tipo_metodo_num == 1:
                efectivo_db = total_general

            elif tipo_metodo_num == 3:
                efectivo_raw = (data_req.get("efectivo_monto") or "").strip()
                if not efectivo_raw:
                    flash("Ingresa el monto en efectivo para el pago mixto.", "danger")
                    return redirect(url_for("carrito_checkout"))

                try:
                    tmp = Decimal(efectivo_raw).quantize(Decimal("0.01"))
                except InvalidOperation:
                    flash("El monto en efectivo es inválido.", "danger")
                    return redirect(url_for("carrito_checkout"))

                if tmp <= 0:
                    flash("El monto en efectivo debe ser mayor a 0.", "danger")
                    return redirect(url_for("carrito_checkout"))

                min_ef = (total_general * Decimal("0.10")).quantize(Decimal("0.01"))
                max_ef = (total_general * Decimal("0.50")).quantize(Decimal("0.01"))

                if tmp < min_ef or tmp > max_ef:
                    flash(
                        f"El efectivo en pago mixto debe estar entre Lps. {min_ef} (10%) y Lps. {max_ef} (50%).",
                        "danger",
                    )
                    return redirect(url_for("carrito_checkout"))

                efectivo_db = tmp

            pago_detalle = PagoDetalle(
                ID_Metodo=metodo_id,
                Efectivo=efectivo_db,
                Numero_tarjeta=tarjeta_ult4,
            )
            db.session.add(pago_detalle)
            db.session.flush()

            nueva_factura = Factura(
                Numero_Factura=numero_factura,
                Fecha_Emision=datetime.now(timezone.utc),
                ID_Empleado=empleado_cajero.ID_Empleado,
                ID_Cai=cai.ID_Cai,
                ID_Usuario_ClienteF=int(id_cliente),
                Subtotal=subtotal_sin_impuesto,
                Descuento=Decimal("0.00"),
                Impuesto=impuesto_total,
                Total_a_pagar=total_general,
                ID_pago=pago_detalle.ID_pago,
            )

            db.session.add(nueva_factura)
            db.session.flush()

            for item in items:
                impuesto_linea = (
                    Decimal(item["subtotal"]) * Decimal("0.15")
                ).quantize(Decimal("0.01"))

                detalle_factura = FacturaDetalle(
                    ID_Parametro=nueva_factura.ID_Parametro,
                    ID_IN_RE=item["id_in_re"],
                    Descripcion=item["nombre"],
                    Cantidad=item["cantidad"],
                    Precio_unitario=item["precio_unit"],
                    Subtotal_linea=item["subtotal"],
                    Impuesto_linea=impuesto_linea,
                )
                db.session.add(detalle_factura)

            cai.Secuencia += 1

            for id_insumo, cantidad_consumida in consumo_por_insumo.items():
                insumo = Insumo.query.get(id_insumo)
                if not insumo:
                    continue

                stock_actual = Decimal(str(insumo.stock_total or 0))
                nuevo_stock = stock_actual - cantidad_consumida
                insumo.stock_total = float(nuevo_stock)

            cliente = UsuarioCliente.query.get(id_cliente)
            rtn_cliente = None

            nombre_cliente = ""
            apellido_cliente = ""
            telefono_cliente = ""

            if cliente:
                nombre_cliente = (
                    getattr(cliente, "Nombre", None)
                    or getattr(cliente, "nombre", None)
                    or ""
                )
                apellido_cliente = (
                    getattr(cliente, "Apellido", None)
                    or getattr(cliente, "apellido", None)
                    or ""
                )
                telefono_cliente = (
                    getattr(cliente, "telefono", None)
                    or getattr(cliente, "Telefono", None)
                    or ""
                )

                sql_rtn_cliente = text(
                    """
                    SELECT td.numero_documento
                    FROM clientes_documento cd
                    JOIN Tipo_documentos td
                        ON td.tipo_doc = cd.tipo_doc
                    WHERE cd.ID_Usuario_ClienteF = :id_cliente
                      AND td.tipo = 2
                    """
                )
                row = db.session.execute(
                    sql_rtn_cliente, {"id_cliente": id_cliente}
                ).first()

                if row:
                    rtn_cliente = row[0]

            if not rtn_cliente and cliente:
                rtn_cliente = (
                    getattr(cliente, "RTN", None)
                    or getattr(cliente, "rtn", None)
                )

            if not rtn_cliente:
                rtn_cliente = "99999999999999"

            direccion = None
            dir_rel_us_co = None
            id_direccion_orden = None

            direccion_id = data_req.get("direccion_id")
            if direccion_id and str(direccion_id).isdigit():
                dir_rel = (
                    DireccionDelCliente.query
                    .filter_by(
                        ID_Usuario_ClienteF=id_cliente,
                        ID_Direccion=int(direccion_id),
                    )
                    .first()
                )
                if dir_rel:
                    dir_rel_us_co = dir_rel.ID_US_CO
                    direccion = Direccion.query.get(int(direccion_id))

            if direccion is None:
                dir_rel = (
                    DireccionDelCliente.query
                    .filter_by(ID_Usuario_ClienteF=id_cliente)
                    .first()
                )
                if dir_rel:
                    dir_rel_us_co = dir_rel.ID_US_CO
                    direccion = Direccion.query.get(dir_rel.ID_Direccion)

            if direccion is not None:
                id_direccion_orden = (
                    getattr(direccion, "ID_Direccion", None)
                    or getattr(direccion, "id_direccion", None)
                )

            if not dir_rel_us_co or not id_direccion_orden:
                db.session.rollback()
                flash(
                    "No se pudo determinar la dirección de entrega para la orden.",
                    "danger",
                )
                return redirect(url_for("carrito_checkout"))

            descripcion_direccion = ""
            if direccion is not None:
                descripcion_direccion = (
                    getattr(direccion, "descripcion", None)
                    or getattr(direccion, "Descripcion", None)
                    or ""
                )

            nombre_final = nombre_cliente or f"Cliente {id_cliente}"
            apellido_final = apellido_cliente or "Sin apellido"
            telefono_final = telefono_cliente or "Sin teléfono"
            descripcion_final = descripcion_direccion or "Sin descripción"

            orden_entrega = OrdenEntrega(
                ID_Parametro=nueva_factura.ID_Parametro,
                ID_Usuario_ClienteF=id_cliente,
                ID_US_CO=dir_rel_us_co,
                ID_Direccion=id_direccion_orden,
                ID_sucursal=id_sucursal,
                ID_Empleado_Repartidor=repartidor.ID_Empleado,
                Numero_Factura=numero_factura,
                nombre=nombre_final,
                apellido=apellido_final,
                descripcion=descripcion_final,
                telefono=telefono_final,
                estado=0,
            )
            db.session.add(orden_entrega)

            efectivo_label = None
            if efectivo_db is not None:
                efectivo_label = f"Efectivo: L {efectivo_db}"

            db.session.commit()

            return render_template(
                "factura_generada.html",
                numero_factura=numero_factura,
                sucursal=sucursal,
                cai=cai,
                empleado=empleado_cajero,
                cliente=cliente,
                direccion=direccion,
                items=items,
                subtotal=subtotal_sin_impuesto,
                impuesto=impuesto_total,
                total=total_general,
                fecha_emision=nueva_factura.Fecha_Emision,
                rtn_emisor=rtn_emisor,
                telefono_emisor=telefono_emisor,
                rtn_cliente=rtn_cliente,
                metodo_pago_label=metodo_nombre,
                efectivo_label=efectivo_label,
                tarjeta_ult4=tarjeta_ult4,
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error al generar la factura: " + str(e), "danger")
            return redirect(url_for("carrito_checkout"))
def validar_metodo_pago(raw):
    if raw is None:
        raise ValidationError("Debes seleccionar un método de pago.")
    raw = str(raw).strip()
    if raw == "":
        raise ValidationError("Debes seleccionar un método de pago.")
    if not raw.isdigit():
        raise ValidationError("El método de pago es inválido.")
    return int(raw)