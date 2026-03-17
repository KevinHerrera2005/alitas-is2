from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from Main import app, db
from .pantallas_acciones_model import PantallasAcciones
from .Pantallas_model import Pantallas
from .Acciones_model import Acciones
from .permisos_puesto_model import PermisosPuesto
from .permisos_empleado_model import PermisosEmpleado


def _borrar_pantallas_acciones_por_ids(ids_pantalla_accion):
    """Elimina en cascada: PermisosEmpleado → PermisosPuesto → PantallasAcciones."""
    if not ids_pantalla_accion:
        return
    ids_permiso_puesto = [r[0] for r in db.session.query(PermisosPuesto.ID_Permiso_Puesto).filter(
        PermisosPuesto.ID_Pantalla_Accion.in_(ids_pantalla_accion)
    ).all()]
    if ids_permiso_puesto:
        db.session.query(PermisosEmpleado).filter(
            PermisosEmpleado.ID_Permiso_Puesto.in_(ids_permiso_puesto)
        ).delete(synchronize_session=False)
        db.session.query(PermisosPuesto).filter(
            PermisosPuesto.ID_Permiso_Puesto.in_(ids_permiso_puesto)
        ).delete(synchronize_session=False)
    db.session.query(PantallasAcciones).filter(
        PantallasAcciones.ID_Pantalla_Accion.in_(ids_pantalla_accion)
    ).delete(synchronize_session=False)


@app.route("/panel_admin", methods=["GET"])
def panel_admin():
    from models.permisos_mixin import pantallas_del_empleado_actual
    pantallas_permitidas = pantallas_del_empleado_actual() or set()
    return render_template("panel_admin.html", pantallas_permitidas=pantallas_permitidas)


@app.route("/ver_pantallasacciones", methods=["GET", "POST"])
def ver_pantallas_acciones():
    from models.permisos_mixin import endpoint_accesible
    if not current_user.is_authenticated or getattr(current_user, "tipo", None) != "empleado" or not endpoint_accesible("ver_pantallas_acciones"):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        eliminar = request.form.get("eliminar")
        if eliminar:
            ids = [r[0] for r in db.session.query(PantallasAcciones.ID_Pantalla_Accion).filter(
                PantallasAcciones.ID_Pantalla == int(eliminar)
            ).all()]
            _borrar_pantallas_acciones_por_ids(ids)
            db.session.commit()
            flash("Pantalla eliminada correctamente", "success")
            return redirect(url_for("ver_pantallas_acciones"))

    registro_pantalla = db.session.query(
        Pantallas.Nombre,
        Pantallas.ID_Pantalla
    ).join(
        PantallasAcciones,
        Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla
    ).distinct().all()
    return render_template("pantallas_acciones.html", nombre_pantalla=registro_pantalla)


@app.route("/ver_acciones_pantalla/<int:id_pantalla>", methods=["GET"])
def ver_acciones_pantalla(id_pantalla):
    pantalla = db.session.get(Pantallas, id_pantalla)

    acciones = db.session.query(
        Acciones.Nombre,
        PantallasAcciones.ID_Pantalla_Accion
    ).join(
        PantallasAcciones, PantallasAcciones.ID_Accion == Acciones.ID_Accion
    ).filter(
        PantallasAcciones.ID_Pantalla == id_pantalla
    ).all()

    return render_template("ver_acciones_pantalla.html", pantalla=pantalla, acciones=acciones)


@app.route("/editar_pantalla_accion/<int:id_pantalla>", methods=["GET", "POST"])
def editar_pantalla_accion(id_pantalla):
    pantalla = db.session.get(Pantallas, id_pantalla)

    todas_acciones = db.session.query(Acciones.ID_Accion, Acciones.Nombre).all()

    asignadas_ids = {r[0] for r in db.session.query(PantallasAcciones.ID_Accion).filter(
        PantallasAcciones.ID_Pantalla == id_pantalla
    ).all()}

    if request.method == "POST":
        seleccionadas = set(int(x) for x in request.form.getlist("acciones"))

        # Quitar las que se desmarcaron (con cascade)
        a_quitar = asignadas_ids - seleccionadas
        if a_quitar:
            ids_pa = [r[0] for r in db.session.query(PantallasAcciones.ID_Pantalla_Accion).filter(
                PantallasAcciones.ID_Pantalla == id_pantalla,
                PantallasAcciones.ID_Accion.in_(a_quitar)
            ).all()]
            _borrar_pantallas_acciones_por_ids(ids_pa)

        # Agregar las nuevas
        a_agregar = seleccionadas - asignadas_ids
        for id_accion in a_agregar:
            db.session.add(PantallasAcciones(
                ID_Pantalla=id_pantalla,
                ID_Accion=id_accion,
                estado=1
            ))

        db.session.commit()
        flash("Pantalla actualizada correctamente", "success")
        return redirect(url_for("ver_pantallas_acciones"))

    return render_template(
        "editar_pantalla_accion.html",
        pantalla=pantalla,
        todas_acciones=todas_acciones,
        asignadas_ids=asignadas_ids
    )


@app.route("/crear_pantalla_accion", methods=["GET", "POST"])
def crear_pantalla():
    acciones = db.session.query(Acciones.ID_Accion, Acciones.Nombre).all()
    pantallas = db.session.query(Pantallas.ID_Pantalla, Pantallas.Nombre).all()
    if request.method == "POST":
        pantalla = request.form.get("pantalla")
        accion = request.form.getlist("acciones")

        for id_de_accion in accion:
            if id_de_accion != "":
                db.session.add(PantallasAcciones(
                    ID_Pantalla=int(pantalla),
                    ID_Accion=int(id_de_accion),
                    estado=1
                ))
        db.session.commit()
        return redirect(url_for("ver_pantallas_acciones"))
    return render_template("crear_pantalla_accion.html", pantalla_opcion=pantallas, acciones=acciones)
