from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from sqlalchemy import and_
from Main import app, db
from .permisos_empleado_model import PermisosEmpleado
from .empleado_model import Empleado, Puesto
from .permisos_puesto_model import PermisosPuesto
from .Pantallas_model import Pantallas
from .pantallas_acciones_model import PantallasAcciones
from .Acciones_model import Acciones
from .estado_pantalla_empleado_model import EstadoPantallaEmpleado
from .sucursal_model import Sucursal


@app.route("/ver_permisos_de_empleados", methods=["GET", "POST"])
def ver_permisos_empleado():
    from models.permisos_mixin import endpoint_accesible
    if not current_user.is_authenticated or getattr(current_user, "tipo", None) != "empleado" or not endpoint_accesible("ver_permisos_empleado"):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))
    empleados = (
        db.session.query(
            Empleado.ID_Empleado.label("id_empleado"),
            Empleado.Nombre.label("nombre"),
            Empleado.Apellido.label("apellido"),
            Empleado.ID_Puesto.label("id_puesto"),
            Puesto.Nombre_Puesto.label("puesto")
        )
        .join(Puesto, Puesto.ID_Puesto == Empleado.ID_Puesto)
        .filter(Empleado.estado == 1)
        .order_by(Empleado.Nombre, Empleado.Apellido)
        .all()
    )

    empleado_id = request.args.get("empleado_id", type=int)

    if not empleado_id and empleados:
        empleado_id = empleados[0].id_empleado

    if request.method == "POST":
        empleado_id = request.form.get("empleado_id", type=int)

        if not empleado_id:
            flash("Selecciona un empleado.", "warning")
            return redirect(url_for("ver_permisos_empleado"))

        empleado_seleccionado = (
            db.session.query(
                Empleado.ID_Empleado.label("id_empleado"),
                Empleado.ID_Puesto.label("id_puesto"),
            )
            .filter(Empleado.ID_Empleado == empleado_id, Empleado.estado == 1)
            .first()
        )

        if not empleado_seleccionado:
            flash("El empleado no existe o está inactivo.", "danger")
            return redirect(url_for("ver_permisos_empleado"))

        permisos_base = (
            db.session.query(
                PermisosPuesto.ID_Permiso_Puesto,
                Pantallas.ID_Pantalla.label("id_pantalla")
            )
            .join(PantallasAcciones, PantallasAcciones.ID_Pantalla_Accion == PermisosPuesto.ID_Pantalla_Accion)
            .join(Pantallas, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla)
            .filter(
                PermisosPuesto.ID_Puesto == empleado_seleccionado.id_puesto,
                Pantallas.estado == 1,
                PantallasAcciones.estado == 1
            )
            .all()
        )

        ids_permisos = [p.ID_Permiso_Puesto for p in permisos_base]

        permisos_existentes = {}
        if ids_permisos:
            permisos_existentes = {
                p.ID_Permiso_Puesto: p
                for p in db.session.query(PermisosEmpleado)
                .filter(
                    PermisosEmpleado.ID_Empleado == empleado_id,
                    PermisosEmpleado.ID_Permiso_Puesto.in_(ids_permisos)
                )
                .all()
            }

        # Guardar estado individual de acciones
        # Si la pantalla está inactiva, no se tocan los PermisosEmpleado para
        # que al reactivarla conserven su estado anterior.
        pantallas_activas = {
            id_p
            for id_p in {p.id_pantalla for p in permisos_base}
            if request.form.get(f"pantalla_activa_{id_p}") == "1"
        }

        for permiso in permisos_base:
            if permiso.id_pantalla not in pantallas_activas:
                continue  # pantalla inactiva → conservar estado actual de las acciones

            nuevo_estado = 1 if request.form.get(f"permiso_{permiso.ID_Permiso_Puesto}") == "1" else 0
            permiso_empleado = permisos_existentes.get(permiso.ID_Permiso_Puesto)
            if permiso_empleado:
                permiso_empleado.estado = nuevo_estado
            else:
                db.session.add(PermisosEmpleado(
                    ID_Empleado=empleado_id,
                    ID_Permiso_Puesto=permiso.ID_Permiso_Puesto,
                    estado=nuevo_estado
                ))

        # Guardar estado de pantalla (independiente de las acciones)
        ids_pantallas = list({p.id_pantalla for p in permisos_base})
        estados_pantalla_existentes = {}
        if ids_pantallas:
            estados_pantalla_existentes = {
                e.ID_Pantalla: e
                for e in db.session.query(EstadoPantallaEmpleado)
                .filter(
                    EstadoPantallaEmpleado.ID_Empleado == empleado_id,
                    EstadoPantallaEmpleado.ID_Pantalla.in_(ids_pantallas)
                )
                .all()
            }
        for id_pantalla in ids_pantallas:
            activa = 1 if request.form.get(f"pantalla_activa_{id_pantalla}") == "1" else 0
            registro = estados_pantalla_existentes.get(id_pantalla)
            if registro:
                registro.activa = activa
            else:
                db.session.add(EstadoPantallaEmpleado(
                    ID_Empleado=empleado_id,
                    ID_Pantalla=id_pantalla,
                    activa=activa
                ))

        db.session.commit()
        flash("Permisos actualizados correctamente.", "success")
        return redirect(url_for("ver_permisos_empleado", empleado_id=empleado_id, modulo="permisos_empleado"))

    # --- GET ---
    empleado_seleccionado = None
    permisos_agrupados = []
    total_permisos = 0
    permisos_activos = 0

    if empleado_id:
        empleado_seleccionado = (
            db.session.query(
                Empleado.ID_Empleado.label("id_empleado"),
                Empleado.Nombre.label("nombre"),
                Empleado.Apellido.label("apellido"),
                Empleado.ID_Puesto.label("id_puesto"),
                Puesto.Nombre_Puesto.label("puesto")
            )
            .join(Puesto, Puesto.ID_Puesto == Empleado.ID_Puesto)
            .filter(Empleado.ID_Empleado == empleado_id, Empleado.estado == 1)
            .first()
        )

        if empleado_seleccionado:
            permisos = (
                db.session.query(
                    PermisosPuesto.ID_Permiso_Puesto.label("id_permiso_puesto"),
                    Pantallas.ID_Pantalla.label("id_pantalla"),
                    Pantallas.Nombre.label("pantalla"),
                    Acciones.Nombre.label("accion"),
                    PermisosEmpleado.estado.label("estado_empleado"),
                    PermisosPuesto.estado.label("estado_puesto")
                )
                .join(PantallasAcciones, PantallasAcciones.ID_Pantalla_Accion == PermisosPuesto.ID_Pantalla_Accion)
                .join(Pantallas, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla)
                .join(Acciones, Acciones.ID_Accion == PantallasAcciones.ID_Accion)
                .outerjoin(
                    PermisosEmpleado,
                    and_(
                        PermisosEmpleado.ID_Permiso_Puesto == PermisosPuesto.ID_Permiso_Puesto,
                        PermisosEmpleado.ID_Empleado == empleado_id
                    )
                )
                .filter(
                    PermisosPuesto.ID_Puesto == empleado_seleccionado.id_puesto,
                    Pantallas.estado == 1,
                    PantallasAcciones.estado == 1
                )
                .order_by(Pantallas.Nombre, Acciones.Nombre)
                .all()
            )

            # Cargar estados de pantalla guardados explícitamente
            ids_pantallas_vistas = list({p.id_pantalla for p in permisos})
            estados_pantalla = {}
            if ids_pantallas_vistas:
                estados_pantalla = {
                    e.ID_Pantalla: e.activa
                    for e in db.session.query(EstadoPantallaEmpleado)
                    .filter(
                        EstadoPantallaEmpleado.ID_Empleado == empleado_id,
                        EstadoPantallaEmpleado.ID_Pantalla.in_(ids_pantallas_vistas)
                    )
                    .all()
                }

            grupos = {}
            for permiso in permisos:
                clave = permiso.pantalla
                if clave not in grupos:
                    grupos[clave] = {"id_pantalla": permiso.id_pantalla, "permisos": []}

                estado_actual = permiso.estado_empleado
                if estado_actual is None:
                    estado_actual = permiso.estado_puesto

                grupos[clave]["permisos"].append({
                    "id_permiso_puesto": permiso.id_permiso_puesto,
                    "accion": permiso.accion,
                    "estado": estado_actual
                })

            permisos_agrupados = [
                {
                    "pantalla": pantalla,
                    "id_pantalla": data["id_pantalla"],
                    # Usar estado guardado explícitamente; si no existe, default activa=True
                    "pantalla_activa": bool(estados_pantalla.get(data["id_pantalla"], 1)),
                    "permisos": data["permisos"]
                }
                for pantalla, data in grupos.items()
            ]

            total_permisos = sum(len(g["permisos"]) for g in permisos_agrupados)
            permisos_activos = sum(
                1
                for g in permisos_agrupados
                for p in g["permisos"]
                if p["estado"] == 1
            )

    modulo = request.args.get("modulo", "permisos_empleado")

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

    from models.permisos_mixin import pantallas_del_empleado_actual
    pantallas_permitidas = pantallas_del_empleado_actual() or set()

    return render_template(
        "permisos_de_los_empleados.html",
        modulo=modulo,
        # Módulo empleado
        empleados=empleados,
        empleado_id=empleado_id,
        empleado_seleccionado=empleado_seleccionado,
        permisos_agrupados=permisos_agrupados,
        total_permisos=total_permisos,
        permisos_activos=permisos_activos,
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
        todas_acciones=todas_acciones
    )


@app.route("/crear_permisos_del_empleado", methods=["GET", "POST"])
def crear_permisos():
    return redirect(url_for("ver_permisos_empleado"))
