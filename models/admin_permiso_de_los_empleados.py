from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from sqlalchemy import and_
from Main import app, db
from .empleado_model import Empleado, Puesto
from .permisos_puesto_model import PermisosPuesto
from .Pantallas_model import Pantallas
from .pantallas_acciones_model import PantallasAcciones
from .Acciones_model import Acciones
from .sucursal_model import Sucursal


@app.route("/ver_permisos_de_empleados", methods=["GET"])
def ver_permisos_empleado():
    from models.permisos_mixin import es_admin_panel
    if not current_user.is_authenticated or not es_admin_panel():
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))

    modulo = request.args.get("modulo", "permisos_puesto")

    # ── Módulo Permisos por Puesto: todos los puestos + permisos agrupados ──
    todos_puestos = (
        db.session.query(Puesto.ID_Puesto, Puesto.Nombre_Puesto)
        .order_by(Puesto.Nombre_Puesto)
        .all()
    )

    puesto_id = request.args.get("puesto_id", type=int)
    if not puesto_id and todos_puestos:
        puesto_id = todos_puestos[0].ID_Puesto

    puesto_seleccionado = db.session.get(Puesto, puesto_id) if puesto_id else None

    permisos_puesto_agrupados = []
    if puesto_seleccionado:
        todas_pa = (
            db.session.query(
                PantallasAcciones.ID_Pantalla_Accion,
                Pantallas.ID_Pantalla.label("id_pantalla"),
                Pantallas.Nombre.label("pantalla"),
                Acciones.Nombre.label("accion"),
                PermisosPuesto.estado.label("estado_puesto")
            )
            .join(Pantallas, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla)
            .join(Acciones, Acciones.ID_Accion == PantallasAcciones.ID_Accion)
            .outerjoin(
                PermisosPuesto,
                and_(
                    PermisosPuesto.ID_Pantalla_Accion == PantallasAcciones.ID_Pantalla_Accion,
                    PermisosPuesto.ID_Puesto == puesto_id
                )
            )
            .filter(PantallasAcciones.estado == 1, Pantallas.estado == 1)
            .order_by(Pantallas.Nombre, Acciones.Nombre)
            .all()
        )
        grupos_p = {}
        for pa in todas_pa:
            if pa.pantalla not in grupos_p:
                grupos_p[pa.pantalla] = {"id_pantalla": pa.id_pantalla, "acciones": []}
            grupos_p[pa.pantalla]["acciones"].append({
                "id_pantalla_accion": pa.ID_Pantalla_Accion,
                "accion": pa.accion,
                "estado": pa.estado_puesto if pa.estado_puesto is not None else 0
            })
        permisos_puesto_agrupados = [
            {"pantalla": p, "id_pantalla": d["id_pantalla"], "acciones": d["acciones"]}
            for p, d in grupos_p.items()
        ]

    # ── Módulo Asignación de Empleados ──
    todos_empleados_asignacion = (
        db.session.query(
            Empleado.ID_Empleado,
            Empleado.Nombre,
            Empleado.Apellido,
            Empleado.ID_Puesto,
            Puesto.Nombre_Puesto
        )
        .join(Puesto, Puesto.ID_Puesto == Empleado.ID_Puesto)
        .filter(Empleado.estado == 1)
        .order_by(Empleado.Nombre, Empleado.Apellido)
        .all()
    )

    todas_sucursales = (
        db.session.query(Sucursal.ID_sucursal, Sucursal.Descripcion)
        .filter(Sucursal.estado == 1)
        .order_by(Sucursal.Descripcion)
        .all()
    )

    # ── Módulo Pantallas & Acciones ──
    nombre_pantalla = db.session.query(
        Pantallas.Nombre,
        Pantallas.ID_Pantalla
    ).join(
        PantallasAcciones,
        Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla
    ).distinct().all()

    # ── Módulo Pantallas Admin ──
    todas_pantallas = db.session.query(
        Pantallas.ID_Pantalla,
        Pantallas.Nombre,
        Pantallas.url,
        Pantallas.estado
    ).order_by(Pantallas.Nombre).all()

    # ── Módulo Acciones Admin ──
    todas_acciones = db.session.query(
        Acciones.ID_Accion,
        Acciones.Nombre,
        Acciones.estado
    ).order_by(Acciones.Nombre).all()

    from models.permisos_mixin import pantallas_del_empleado_actual, es_admin_panel

    # Admin ve todo; el resto solo ve lo que su puesto permite
    class _AllSet:
        def __contains__(self, item): return True
        def __bool__(self): return True

    pantallas_permitidas = _AllSet() if es_admin_panel() else (pantallas_del_empleado_actual() or set())

    # Módulo Vistas: pantallas activas con URL válida, excluyendo las internas del sistema
    from flask import url_for as _url_for, current_app
    _EXCLUIR_ENDPOINTS = {
        'acciones.index_view',
        'impuesto_tasa_historica.index_view',
        'carrito.index_view',
        'usuarios_cliente.index_view',
        'empleado_documento.index_view',
        'pantallas.index_view',
        # Paneles específicos de puesto (no relevantes para el admin)
        'panel_contador.panel',
        'login_jefe.panel_jefe',
        'ver_pantallas_acciones',
        'ver_permisos_puesto',
        'ver_permisos_empleado',
        'puestos.index_view',
    }
    # Renombres manuales para endpoints que no están en Flask-Admin
    _RENOMBRAR_ENDPOINTS = {
        'crud_recetas': 'Recetas',
    }
    # Construir mapeo endpoint → nombre de display desde Flask-Admin
    _endpoint_nombres = {}
    try:
        _admin_obj = current_app.extensions.get('admin')
        _admin_inst = (_admin_obj[0] if isinstance(_admin_obj, list) else _admin_obj)
        for _v in _admin_inst._views:
            if _v.endpoint and getattr(_v, 'name', None):
                _endpoint_nombres[_v.endpoint + '.index_view'] = _v.name
    except Exception:
        pass

    vistas_pantallas = []
    for p in todas_pantallas:
        if p.estado == 1 and p.url and p.url not in _EXCLUIR_ENDPOINTS:
            try:
                href = _url_for(p.url)
            except Exception:
                href = None
            if href:
                nombre_display = (
                    _endpoint_nombres.get(p.url)
                    or _RENOMBRAR_ENDPOINTS.get(p.url)
                    or p.Nombre
                )
                vistas_pantallas.append({"nombre": nombre_display, "href": href})

    return render_template(
        "permisos_de_los_empleados.html",
        modulo=modulo,
        # Módulo permisos_puesto
        todos_puestos=todos_puestos,
        puesto_id=puesto_id,
        puesto_seleccionado=puesto_seleccionado,
        permisos_puesto_agrupados=permisos_puesto_agrupados,
        # Módulo asignacion_empleados
        todos_empleados_asignacion=todos_empleados_asignacion,
        todas_sucursales=todas_sucursales,
        # Módulos generales
        pantallas_permitidas=pantallas_permitidas,
        nombre_pantalla=nombre_pantalla,
        todas_pantallas=todas_pantallas,
        todas_acciones=todas_acciones,
        # Módulo Vistas
        vistas_pantallas=vistas_pantallas,
    )


@app.route("/crear_permisos_del_empleado", methods=["GET", "POST"])
def crear_permisos():
    return redirect(url_for("ver_permisos_empleado"))
