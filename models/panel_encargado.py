from datetime import datetime
import json
import smtplib
import ssl
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DBAPIError
from jinja2 import TemplateNotFound

from mensajes_logs import logger_

from models import db
from models.insumo_model import Insumo
from models.proveedores_model import Proveedor, ProveedorInsumo
from models.ordenes_proveedores_model import OrdenesProveedores, OrdenesProveedoresDetalle
from models.empleado_model import Empleado
from models.sucursal_model import Sucursal

panel_encargado = Blueprint("panel_encargado", __name__)


@panel_encargado.before_request
def _panel_encargado_log_request():
    fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        logger_.Logger.add_to_log("info", f"{request.method} {request.path}", "panel_encargado_request", fecha)
    except Exception:
        pass


def _parse_int(v):
    try:
        return int(str(v).strip())
    except Exception:
        return None


def _norm(txt):
    return (txt or "").strip().lower()


def _to_float(v):
    try:
        if v is None or v == "":
            return None
        return float(v)
    except Exception:
        try:
            return float(str(v).replace(",", "."))
        except Exception:
            return None


def _correo_de_proveedor(proveedor: Proveedor | None) -> str | None:
    if proveedor is None:
        return None
    return (getattr(proveedor, "email", None) or getattr(proveedor, "Email", None) or "").strip() or None


def _unidad_nombre_de_insumo(ins):
    unidad_nombre = "unidad"
    unidad_obj = getattr(ins, "unidad", None)
    if unidad_obj is not None:
        unidad_nombre = getattr(unidad_obj, "Nombre", None) or getattr(unidad_obj, "Nombre_Unidad", None) or unidad_nombre
    return unidad_nombre


def _stock_min(ins):
    return _to_float(getattr(ins, "stock_minimo", None))


def _stock_max(ins):
    v = getattr(ins, "stock_maximo", None)
    if v is None:
        v = getattr(ins, "stock_max", None)
    return _to_float(v)


def _stock_total(ins):
    return _to_float(getattr(ins, "stock_total", None))


def _proveedores_de_insumos(insumos_ids):
    ids = [int(x) for x in (insumos_ids or []) if str(x).strip().isdigit()]
    if not ids:
        return []

    q = (
        db.session.query(Proveedor)
        .join(ProveedorInsumo, ProveedorInsumo.ID_Proveedor == Proveedor.ID_Proveedor)
        .filter(ProveedorInsumo.ID_Insumo.in_(ids))
    )
    if hasattr(ProveedorInsumo, "Activo"):
        q = q.filter(ProveedorInsumo.Activo == 1)

    rows = q.all()
    seen = set()
    out = []
    for prov in rows:
        pid = int(getattr(prov, "ID_Proveedor"))
        if pid in seen:
            continue
        seen.add(pid)
        out.append(
            {
                "id": pid,
                "nombre": getattr(prov, "Nombre_Proveedor", None) or getattr(prov, "Nombre", None) or str(pid),
                "email": _correo_de_proveedor(prov),
            }
        )
    out.sort(key=lambda x: _norm(x.get("nombre")))
    return out


def _insumos_ui_unicos_por_sucursal(sucursal_id: int):
    if not sucursal_id:
        return []

    insumos = (
        Insumo.query
        .filter(Insumo.ID_sucursal == sucursal_id)
        .order_by(Insumo.Nombre_insumo)
        .all()
    )

    grupos = {}
    for ins in insumos:
        nombre = (getattr(ins, "Nombre_insumo", None) or "").strip()
        key = _norm(nombre) or f"__id__{int(ins.ID_Insumo)}"

        st_total = _stock_total(ins)
        st_total = float(st_total) if st_total is not None else 0.0
        st_min = _stock_min(ins)
        st_max = _stock_max(ins)

        g = grupos.get(key)
        if g is None:
            grupos[key] = {
                "rep": ins,
                "ids": [int(ins.ID_Insumo)],
                "nombre": nombre,
                "stock_total": st_total,
                "stock_min": st_min,
                "stock_max": st_max,
            }
        else:
            g["ids"].append(int(ins.ID_Insumo))
            g["stock_total"] += st_total

            if st_min is not None:
                if g["stock_min"] is None:
                    g["stock_min"] = st_min
                else:
                    g["stock_min"] = max(float(g["stock_min"]), float(st_min))

            if st_max is not None:
                if g["stock_max"] is None:
                    g["stock_max"] = st_max
                else:
                    g["stock_max"] = min(float(g["stock_max"]), float(st_max))

            if int(ins.ID_Insumo) < int(g["rep"].ID_Insumo):
                g["rep"] = ins
                g["nombre"] = nombre

    salida = []
    for g in grupos.values():
        rep = g["rep"]
        stock_total_val = float(g["stock_total"] or 0.0)
        stock_min_val = float(g["stock_min"]) if g["stock_min"] is not None else None
        stock_max_val = float(g["stock_max"]) if g["stock_max"] is not None else None

        faltante = 0.0
        if stock_min_val is not None:
            faltante = max(stock_min_val - stock_total_val, 0.0)

        salida.append(
            {
                "id": int(rep.ID_Insumo),
                "nombre": (g["nombre"] or getattr(rep, "Nombre_insumo", "") or "").strip(),
                "stock_minimo": stock_min_val,
                "stock_maximo": stock_max_val,
                "stock_total": stock_total_val,
                "faltante": faltante,
                "unidad": _unidad_nombre_de_insumo(rep),
                "proveedores": _proveedores_de_insumos(g["ids"]),
            }
        )

    salida.sort(key=lambda x: _norm(x.get("nombre")))
    return salida


def enviar_correo_orden(proveedor: Proveedor, por_sucursal: dict):
    remitente = (current_app.config.get("GMAIL_USER") or "").strip()
    clave = (current_app.config.get("GMAIL_PASSWORD") or "").strip()
    destino = (_correo_de_proveedor(proveedor) or "").strip()

    if not remitente or not clave:
        return False, "Falta configurar GMAIL_USER o GMAIL_PASSWORD"
    if not destino:
        return False, "El proveedor no tiene email"

    asunto = "Solicitud de pedido de insumos"

    def fmt(x):
        try:
            xf = float(x)
            if xf.is_integer():
                return str(int(xf))
            return str(xf)
        except Exception:
            return str(x)

    prov_nombre = getattr(proveedor, "Nombre_Proveedor", None) or getattr(proveedor, "Nombre", None) or ""

    lineas = [
        f"Estimado(a) {prov_nombre}:",
        "",
        "Un cordial saludo, hablamos de parte de la empresa Alitas el Comelón.",
        "A continuación se le solicitan los siguientes insumos para las siguientes sucursales.",
        "Favor de confirmar el pedido e incluir una fecha estimada en la que se recibirá el insumo.",
        "",
    ]

    data_ordenada = sorted(
        list((por_sucursal or {}).values()),
        key=lambda d: _norm(getattr((d.get("sucursal") or None), "Descripcion", "") or ""),
    )

    for data in data_ordenada:
        sucursal = data.get("sucursal")
        items = data.get("items") or []
        orden_id = data.get("orden_id")

        sucursal_nombre = getattr(sucursal, "Descripcion", None) or "N/D"
        sucursal_dir = "N/D"
        if sucursal is not None and getattr(sucursal, "direccion", None) is not None:
            sucursal_dir = getattr(sucursal.direccion, "Descripcion", "") or "N/D"

        lineas.append(f"{sucursal_nombre}:")
        lineas.append(f"Dirección: {sucursal_dir}")

        for insumo, cantidad, unidad_nombre in items:
            nombre_ins = getattr(insumo, "Nombre_insumo", None) or getattr(insumo, "nombre", None) or ""
            lineas.append(f"- {nombre_ins}: {fmt(cantidad)} {unidad_nombre}")

        if orden_id:
            lineas.append("")
            lineas.append(f"numero de orden: {orden_id}")

        lineas.append("")
        lineas.append("")

    lineas.append("Mensaje generado automáticamente por el sistema.")
    cuerpo = "\n".join([l for l in lineas if l is not None])

    mensaje = MIMEMultipart()
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destino
    mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

    try:
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto, timeout=20) as servidor:
            servidor.login(remitente, clave)
            servidor.sendmail(remitente, [destino], mensaje.as_string())
        return True, None
    except smtplib.SMTPAuthenticationError as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "encargar_insumos_enviar_correo", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "encargar_insumos_enviar_correo", fecha)
        return False, "Gmail rechazó la autenticación (usa App Password)"
    except Exception as e:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(e), "encargar_insumos_enviar_correo", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "encargar_insumos_enviar_correo", fecha)
        return False, f"Error SMTP: {type(e).__name__}"


@panel_encargado.route("/panel_encargado")
def panel():
    fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        logger_.Logger.add_to_log("info", "open_panel", "panel_encargado_panel", fecha)
        return render_template("panel_encargado.html")
    except Exception as error:
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_panel", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_panel", fecha)
        flash("Error al abrir el panel. Revisa los logs.", "danger")
        return render_template("panel_encargado.html"), 200


@panel_encargado.route("/encargar_insumos_data")
def encargar_insumos_data():
    fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        sucursal_id = _parse_int(request.args.get("sucursal_id"))
        if not sucursal_id:
            return jsonify({"ok": True, "insumos": []})

        insumos_ui = _insumos_ui_unicos_por_sucursal(sucursal_id)
        return jsonify({"ok": True, "insumos": insumos_ui})
    except Exception as error:
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_encargar_insumos_data", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_encargar_insumos_data", fecha)
        return jsonify({"ok": False, "insumos": [], "error": "Error al cargar insumos."}), 200


@panel_encargado.route("/encargar_insumos", methods=["GET", "POST"])
def encargar_insumos():
    fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        modo_todos = request.args.get("todos") == "1"

        if request.method == "POST":
            lineas_raw = (request.form.get("lineas_json") or "").strip()

            if not lineas_raw:
                flash("Debes guardar al menos un insumo con su proveedor y cantidad.", "warning")
                params = {"todos": "1"} if modo_todos else {}
                return redirect(url_for("panel_encargado.encargar_insumos", **params))

            try:
                lineas_data = json.loads(lineas_raw)
            except Exception:
                flash("Los datos enviados no son válidos.", "danger")
                params = {"todos": "1"} if modo_todos else {}
                return redirect(url_for("panel_encargado.encargar_insumos", **params))

            if not isinstance(lineas_data, list) or not lineas_data:
                flash("Debes guardar al menos un insumo con su proveedor y cantidad.", "warning")
                params = {"todos": "1"} if modo_todos else {}
                return redirect(url_for("panel_encargado.encargar_insumos", **params))

            agrupado = {}

            for linea in lineas_data:
                insumo_id = _parse_int(linea.get("insumo_id"))
                proveedor_id = _parse_int(linea.get("proveedor_id"))
                sucursal_id = _parse_int(linea.get("sucursal_id"))

                try:
                    cantidad = float(str(linea.get("cantidad")).replace(",", "."))
                except Exception:
                    cantidad = None

                if not insumo_id or not proveedor_id or not sucursal_id or not cantidad or cantidad <= 0:
                    continue

                insumo = Insumo.query.get(insumo_id)
                proveedor = Proveedor.query.get(proveedor_id)
                sucursal_obj = Sucursal.query.get(sucursal_id)

                if not insumo or not proveedor or not sucursal_obj:
                    continue

                if getattr(insumo, "ID_sucursal", None) != sucursal_id:
                    flash("Hay insumos que no pertenecen a la sucursal indicada.", "danger")
                    params = {"todos": "1"} if modo_todos else {}
                    return redirect(url_for("panel_encargado.encargar_insumos", **params))

                unidad_nombre = linea.get("unidad") or _unidad_nombre_de_insumo(insumo) or "unidad"

                if proveedor_id not in agrupado:
                    agrupado[proveedor_id] = {"proveedor": proveedor, "por_sucursal": {}}

                por_sucursal = agrupado[proveedor_id]["por_sucursal"]
                if sucursal_id not in por_sucursal:
                    por_sucursal[sucursal_id] = {"sucursal": sucursal_obj, "items_map": {}, "orden_id": None, "items": []}

                items_map = por_sucursal[sucursal_id]["items_map"]
                key_ins = int(insumo.ID_Insumo)

                if key_ins in items_map:
                    ins_prev, cant_prev, uni_prev = items_map[key_ins]
                    items_map[key_ins] = (ins_prev, float(cant_prev) + float(cantidad), uni_prev or unidad_nombre)
                else:
                    items_map[key_ins] = (insumo, float(cantidad), unidad_nombre)

            if not agrupado:
                flash("Los datos de la orden están vacíos o no son válidos.", "danger")
                params = {"todos": "1"} if modo_todos else {}
                return redirect(url_for("panel_encargado.encargar_insumos", **params))

            proveedores_sin_email = [d["proveedor"] for d in agrupado.values() if not _correo_de_proveedor(d["proveedor"])]
            if proveedores_sin_email:
                nombres = ", ".join(getattr(p, "Nombre_Proveedor", None) or getattr(p, "Nombre", None) or "" for p in proveedores_sin_email)
                flash(f"Los siguientes proveedores no tienen definido un email: {nombres}", "danger")
                params = {"todos": "1"} if modo_todos else {}
                return redirect(url_for("panel_encargado.encargar_insumos", **params))

            id_empleado_encargado = _parse_int(
                getattr(current_user, "db_id", None)
                or getattr(current_user, "ID_Empleado", None)
                or getattr(current_user, "id_empleado", None)
            )

            if id_empleado_encargado is None or Empleado.query.get(id_empleado_encargado) is None:
                flash("No se pudo determinar el empleado encargado para la orden.", "danger")
                params = {"todos": "1"} if modo_todos else {}
                return redirect(url_for("panel_encargado.encargar_insumos", **params))

            for datos in agrupado.values():
                proveedor = datos["proveedor"]
                por_sucursal = datos["por_sucursal"]

                for data_suc in por_sucursal.values():
                    sucursal_obj = data_suc["sucursal"]
                    items = list((data_suc.get("items_map") or {}).values())
                    items.sort(key=lambda t: _norm(getattr(t[0], "Nombre_insumo", "") or ""))

                    orden = OrdenesProveedores(
                        ID_Proveedor=proveedor.ID_Proveedor,
                        ID_Empleado_Encargado=id_empleado_encargado,
                        ID_Sucursal=sucursal_obj.ID_sucursal,
                        Fecha_Inicio=datetime.utcnow(),
                        Estado=0,
                    )
                    db.session.add(orden)
                    db.session.flush()

                    for insumo, cantidad, _ in items:
                        id_unidad = getattr(insumo, "ID_Unidad", None) or getattr(insumo, "ID_Unidad_medida", None)
                        if id_unidad is None:
                            db.session.rollback()
                            flash(f"El insumo '{getattr(insumo, 'Nombre_insumo', '')}' no tiene unidad configurada.", "danger")
                            params = {"todos": "1"} if modo_todos else {}
                            return redirect(url_for("panel_encargado.encargar_insumos", **params))

                        detalle = OrdenesProveedoresDetalle(
                            ID_Orden_Proveedor=orden.ID_Orden_Proveedor,
                            ID_Insumo=insumo.ID_Insumo,
                            ID_Unidad=id_unidad,
                            Cantidad_Solicitada=cantidad,
                            Cantidad_Recibida=0,
                        )
                        db.session.add(detalle)

                    data_suc["orden_id"] = int(orden.ID_Orden_Proveedor)
                    data_suc["items"] = items

            db.session.commit()

            for datos in agrupado.values():
                proveedor = datos["proveedor"]
                por_sucursal = datos["por_sucursal"]

                ok, err = enviar_correo_orden(proveedor, por_sucursal)
                if not ok:
                    flash(f"Correo NO enviado a {getattr(proveedor, 'Nombre_Proveedor', '')}: {err}", "danger")

            flash("Se generaron las órdenes a proveedores.", "success")
            return redirect(url_for("panel_encargado.ordenes_proveedores_encargado"))

        sucursales_q = (
            Sucursal.query
            .filter(Sucursal.estado == 1)
            .order_by(Sucursal.Descripcion)
            .all()
        )

        sucursales_ui = []
        for s in sucursales_q:
            d = ""
            if getattr(s, "direccion", None) is not None:
                d = getattr(s.direccion, "Descripcion", "") or ""
            sucursales_ui.append({"id": int(s.ID_sucursal), "nombre": s.Descripcion, "direccion": d})

        sucursal_id = _parse_int(request.args.get("sucursal_id"))
        if sucursal_id is None and sucursales_ui:
            sucursal_id = sucursales_ui[0]["id"]

        insumos_ui = _insumos_ui_unicos_por_sucursal(int(sucursal_id)) if sucursal_id is not None else []

        return render_template(
            "encargar_insumos.html",
            insumos=insumos_ui,
            sucursales=sucursales_ui,
            sucursal_defecto_id=sucursal_id,
            todos=modo_todos,
        )

    except Exception as error:
        try:
            db.session.rollback()
        except Exception:
            pass
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_encargar_insumos", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_encargar_insumos", fecha)
        flash("Error al procesar el encargo. Revisa los logs.", "danger")
        return render_template("panel_encargado.html"), 200


@panel_encargado.route("/ordenes_proveedores_encargado")
def ordenes_proveedores_encargado():
    fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        logger_.Logger.add_to_log("info", "click_ordenes_proveedores_encargado", "panel_encargado_ordenes_proveedores_encargado", fecha)

        db.session.execute(text("SELECT 1"))

        ordenes = (
            db.session.query(OrdenesProveedores)
            .order_by(OrdenesProveedores.ID_Orden_Proveedor.desc())
            .limit(300)
            .all()
        )

        return render_template("ordenes_proveedores_encargado.html", ordenes=ordenes)

    except TemplateNotFound as error:
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_ordenes_template_missing", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_ordenes_template_missing", fecha)
        flash("No se pudo abrir órdenes: falta la plantilla 'ordenes_proveedores_encargado.html'.", "danger")
        return render_template("panel_encargado.html"), 200

    except (OperationalError, DBAPIError) as error:
        try:
            db.session.rollback()
        except Exception:
            pass
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_ordenes_db", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_ordenes_db", fecha)
        flash("Base de datos apagada o sin conexión. Revisa los logs.", "danger")
        return render_template("panel_encargado.html"), 200

    except Exception as error:
        try:
            db.session.rollback()
        except Exception:
            pass
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_ordenes", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_ordenes", fecha)
        flash(f"No se pudo abrir órdenes. Error: {type(error).__name__}", "danger")
        return render_template("panel_encargado.html"), 200


@panel_encargado.route("/historial_ordenes_proveedores_encargado")
def historial_ordenes_proveedores_encargado():
    fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        logger_.Logger.add_to_log("info", "click_historial_ordenes_proveedores_encargado", "panel_encargado_historial_ordenes_proveedores_encargado", fecha)

        db.session.execute(text("SELECT 1"))

        q = db.session.query(OrdenesProveedores)

        if hasattr(OrdenesProveedores, "Estado"):
            q = q.filter(OrdenesProveedores.Estado.in_([2, 3]))

        ordenes = (
            q.order_by(OrdenesProveedores.ID_Orden_Proveedor.desc())
            .limit(300)
            .all()
        )

        return render_template("historial_ordenes_proveedores_encargado.html", ordenes=ordenes)

    except TemplateNotFound as error:
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_historial_template_missing", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_historial_template_missing", fecha)
        flash("No se pudo abrir el historial: falta la plantilla 'historial_ordenes_proveedores_encargado.html'.", "danger")
        return render_template("panel_encargado.html"), 200

    except (OperationalError, DBAPIError) as error:
        try:
            db.session.rollback()
        except Exception:
            pass
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_historial_db", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_historial_db", fecha)
        flash("Base de datos apagada o sin conexión. Revisa los logs.", "danger")
        return render_template("panel_encargado.html"), 200

    except Exception as error:
        try:
            db.session.rollback()
        except Exception:
            pass
        logger_.Logger.add_to_log("error", str(error), "panel_encargado_historial", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "panel_encargado_historial", fecha)
        flash(f"No se pudo abrir el historial. Error: {type(error).__name__}", "danger")
        return render_template("panel_encargado.html"), 200