from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import text
from models import db

mis_pedidos_bp = Blueprint("mis_pedidos_bp", __name__)

def _cliente_id():
    for k in ("cliente_id", "ID_Usuario_ClienteF", "id_cliente", "usuario_cliente_id"):
        v = session.get(k)
        if v is not None:
            try:
                return int(v)
            except Exception:
                pass

    if getattr(current_user, "is_authenticated", False):
        for attr in ("ID_Usuario_ClienteF", "id_usuario_cliente", "Usuario_ClienteID", "db_id", "id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass

    return None

def _estado_texto(estado):
    try:
        estado = int(estado)
    except Exception:
        return str(estado)

    mapa = {
        0: "En preparación",
        1: "Listo para recoger",
        2: "En camino",
        3: "Entregado",
        4: "Cancelado",
    }
    return mapa.get(estado, f"Estado {estado}")

def _first_attr(obj, names):
    for n in names:
        if obj is None:
            return None
        if hasattr(obj, n):
            v = getattr(obj, n)
            if v is not None:
                return v
    return None

@mis_pedidos_bp.route("/mis_pedidos", methods=["GET"])
@login_required
def mis_pedidos():
    cid = _cliente_id()
    if not cid:
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for("login"))

    q = (request.args.get("q") or "").strip()

    try:
        page = int(request.args.get("page", 1))
    except Exception:
        page = 1
    if page < 1:
        page = 1

    try:
        per_page = int(request.args.get("per_page", 8))
    except Exception:
        per_page = 8
    if per_page < 5:
        per_page = 5
    if per_page > 50:
        per_page = 50

    params = {"cid": cid}
    filtro = ""

    if q:
        filtro = " AND (oe.Numero_Factura LIKE :q OR uc.nombre LIKE :q OR uc.apellido LIKE :q)"
        params["q"] = f"%{q}%"

    total = db.session.execute(
        text(
            f"""
            SELECT COUNT(*) AS total
            FROM Orden_Entrega oe
            INNER JOIN Usuarios_cliente uc ON uc.ID_Usuario_ClienteF = oe.ID_Usuario_ClienteF
            WHERE oe.ID_Usuario_ClienteF = :cid
            {filtro}
            """
        ),
        params,
    ).scalar() or 0

    total_pages = (total + per_page - 1) // per_page if total else 1
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * per_page
    params_list = dict(params)
    params_list.update({"limit": int(per_page), "offset": int(offset)})

    filas = db.session.execute(
        text(
            f"""
            SELECT
                oe.ID_Orden_Entrega,
                oe.Numero_Factura AS Numero_factura,
                uc.nombre,
                uc.apellido,
                oe.estado,
                oe.Fecha_Creacion AS Fecha_Creacion,
                oe.Motivo_Cancelacion
            FROM Orden_Entrega oe
            INNER JOIN Usuarios_cliente uc ON uc.ID_Usuario_ClienteF = oe.ID_Usuario_ClienteF
            WHERE oe.ID_Usuario_ClienteF = :cid
            {filtro}
            ORDER BY oe.Fecha_Creacion DESC
            OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
            """
        ),
        params_list,
    ).mappings().all()

    pedidos = []
    for f in filas:
        estado = int(f["estado"]) if f["estado"] is not None else 0
        pedidos.append(
            {
                "ID_Orden_Entrega": f["ID_Orden_Entrega"],
                "Numero_factura": f["Numero_factura"],
                "nombre": f["nombre"],
                "apellido": f["apellido"],
                "estado": estado,
                "estado_texto": _estado_texto(estado),
                "Fecha_Creacion": f["Fecha_Creacion"],
                "Motivo_Cancelacion": f["Motivo_Cancelacion"],
                "puede_cancelar": estado not in (3, 4),
            }
        )

    return render_template(
        "mis_pedidos.html",
        pedidos=pedidos,
        q=q,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
    )

@mis_pedidos_bp.route("/mis_pedidos/imprimir/<path:numero_factura>", methods=["GET"])
@login_required
def imprimir_factura(numero_factura):
    cid = _cliente_id()
    if not cid:
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for("login"))

    nf = (numero_factura or "").strip()
    if not nf:
        flash("Número de factura inválido.", "danger")
        return redirect(url_for("mis_pedidos_bp.mis_pedidos"))

    from models.factura_model import Factura
    from models.factura_detalle_model import FacturaDetalle
    from models.pago_detalle_model import PagoDetalle
    from models.cai_model import CAI
    from models.sucursal_model import Sucursal
    from models.empleado_model import Empleado
    from models.usuario_cliente_model import UsuarioCliente
    from models.orden_entrega_model import OrdenEntrega
    from models.direccion_model import Direccion
    from models.parametro_sar_model import ParametroSAR
    from models.metodos_money_model import MetodosMoney

    def _param_sar(id_param, default):
        try:
            obj = ParametroSAR.query.get(int(id_param))
            if obj and getattr(obj, "Valor", None):
                return str(obj.Valor).strip()
        except Exception:
            pass
        return default

    def _metodo_nombre(metodo):
        nombre = None
        tipo = None
        if metodo is not None:
            nombre = (
                getattr(metodo, "Nombre", None)
                or getattr(metodo, "nombre", None)
                or getattr(metodo, "Metodo", None)
                or getattr(metodo, "metodo", None)
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
        return nombre or "No especificado"

    factura = (
        Factura.query
        .filter(Factura.Numero_Factura == nf, Factura.ID_Usuario_ClienteF == int(cid))
        .first()
    )
    if not factura:
        flash("No se encontró la factura o no tienes permiso para verla.", "danger")
        return redirect(url_for("mis_pedidos_bp.mis_pedidos"))

    cliente = getattr(factura, "cliente", None) or UsuarioCliente.query.get(int(cid))

    cai = CAI.query.get(int(factura.ID_Cai)) if getattr(factura, "ID_Cai", None) is not None else None

    sucursal = None
    if cai is not None:
        sid = _first_attr(cai, ["ID_sucursal", "ID_Sucursal", "id_sucursal"])
        if sid is not None:
            try:
                sucursal = Sucursal.query.get(int(sid))
            except Exception:
                sucursal = None

    empleado = None
    if getattr(factura, "ID_Empleado", None) is not None:
        try:
            empleado = Empleado.query.get(int(factura.ID_Empleado))
        except Exception:
            empleado = None

    orden = (
        OrdenEntrega.query
        .filter(OrdenEntrega.ID_Parametro == int(factura.ID_Parametro), OrdenEntrega.ID_Usuario_ClienteF == int(cid))
        .first()
    )
    if orden is None:
        orden = (
            OrdenEntrega.query
            .filter(OrdenEntrega.Numero_Factura == nf, OrdenEntrega.ID_Usuario_ClienteF == int(cid))
            .first()
        )

    direccion = None
    if orden is not None:
        dir_id = _first_attr(orden, ["ID_Direccion", "ID_DireccionF", "id_direccion", "ID_direccion"])
        if dir_id is not None:
            try:
                direccion = Direccion.query.get(int(dir_id))
            except Exception:
                direccion = None

    rtn_emisor = _param_sar(4, current_app.config.get("RTN_EMISOR") or "N/A")
    telefono_emisor = (
        _first_attr(empleado, ["Telefono", "telefono"])
        or current_app.config.get("TELEFONO_EMISOR")
        or "N/A"
    )

    rtn_cliente = "N/A"
    try:
        row = db.session.execute(
            text(
                """
                SELECT TOP 1 td.numero_documento
                FROM clientes_documento cd
                JOIN Tipo_documentos td ON td.tipo_doc = cd.tipo_doc
                WHERE cd.ID_Usuario_ClienteF = :id_cliente
                  AND td.tipo = 2
                """
            ),
            {"id_cliente": int(cid)},
        ).first()
        if row and row[0]:
            rtn_cliente = str(row[0]).strip()
    except Exception:
        pass

    if (not rtn_cliente or rtn_cliente == "N/A") and cliente is not None:
        rtn_cliente = _first_attr(cliente, ["RTN", "rtn"]) or "N/A"

    pago_detalle = getattr(factura, "pago_detalle", None)
    if pago_detalle is None and getattr(factura, "ID_pago", None) is not None:
        try:
            pago_detalle = PagoDetalle.query.get(int(factura.ID_pago))
        except Exception:
            pago_detalle = None

    metodo_pago_label = "No especificado"
    tarjeta_ult4 = None
    efectivo_label = None

    if pago_detalle is not None:
        tarjeta_raw = _first_attr(pago_detalle, ["Numero_tarjeta", "numero_tarjeta"])
        if tarjeta_raw:
            tarjeta_ult4 = str(tarjeta_raw)[-4:]

        efectivo_db = _first_attr(pago_detalle, ["Efectivo", "efectivo"])
        if efectivo_db is not None:
            try:
                efectivo_label = f"Efectivo: L {float(efectivo_db):.2f}"
            except Exception:
                efectivo_label = f"Efectivo: L {efectivo_db}"

        metodo_id = _first_attr(pago_detalle, ["ID_Metodo", "id_metodo", "ID_metodo"])
        if metodo_id is not None:
            try:
                metodo = MetodosMoney.query.get(int(metodo_id))
            except Exception:
                metodo = None
            metodo_pago_label = _metodo_nombre(metodo)

    detalles = []
    try:
        detalles = list(getattr(factura, "detalles", []) or [])
    except Exception:
        detalles = []

    if not detalles:
        try:
            detalles = FacturaDetalle.query.filter(FacturaDetalle.ID_Parametro == int(factura.ID_Parametro)).all()
        except Exception:
            detalles = []

    items = []
    for d in detalles:
        cant = _first_attr(d, ["Cantidad", "cantidad"]) or 0
        nombre = _first_attr(d, ["Descripcion", "descripcion"]) or "Item"
        pu = _first_attr(d, ["Precio_unitario", "precio_unitario", "Precio_Unitario"]) or 0
        sub = _first_attr(d, ["Subtotal_linea", "subtotal_linea", "Subtotal"]) 

        try:
            cant_f = float(cant)
        except Exception:
            cant_f = 0.0

        try:
            pu_f = float(pu)
        except Exception:
            pu_f = 0.0

        try:
            sub_f = float(sub) if sub is not None else (cant_f * pu_f)
        except Exception:
            sub_f = cant_f * pu_f

        items.append(
            {
                "cantidad": int(cant_f) if float(cant_f).is_integer() else cant_f,
                "nombre": str(nombre),
                "precio_unit": pu_f,
                "subtotal": sub_f,
            }
        )

    fecha_emision = getattr(factura, "Fecha_Emision", None)

    try:
        subtotal = float(getattr(factura, "Subtotal", 0) or 0)
    except Exception:
        subtotal = 0.0

    try:
        impuesto = float(getattr(factura, "Impuesto", 0) or 0)
    except Exception:
        impuesto = 0.0

    try:
        total = float(getattr(factura, "Total_a_pagar", 0) or 0)
    except Exception:
        total = 0.0

    if subtotal == 0.0 and items:
        subtotal = sum(float(i["subtotal"]) for i in items)

    if impuesto == 0.0 and subtotal > 0:
        impuesto = round(subtotal * 0.15, 2)

    if total == 0.0 and subtotal > 0:
        total = round(subtotal + impuesto, 2)

    return render_template(
        "factura_generada.html",
        numero_factura=nf,
        sucursal=sucursal,
        rtn_emisor=rtn_emisor,
        telefono_emisor=telefono_emisor,
        cai=cai,
        fecha_emision=fecha_emision,
        cliente=cliente,
        rtn_cliente=rtn_cliente,
        direccion=direccion,
        metodo_pago_label=metodo_pago_label,
        tarjeta_ult4=tarjeta_ult4,
        efectivo_label=efectivo_label,
        empleado=empleado,
        items=items,
        subtotal=subtotal,
        impuesto=impuesto,
        total=total,
    )


