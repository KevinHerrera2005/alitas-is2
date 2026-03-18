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
    return redirect(url_for("ver_permisos_empleado"))


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
            return redirect(url_for("ver_permisos_empleado", modulo="pantallas_acciones"))

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


@app.route("/toggle_accion_estado/<int:id_accion>", methods=["POST"])
def toggle_accion_estado(id_accion):
    accion = db.session.get(Acciones, id_accion)
    if accion:
        accion.estado = 0 if accion.estado == 1 else 1
        db.session.commit()
    return redirect(url_for("ver_permisos_empleado", modulo="acciones_admin"))


@app.route("/crear_accion_registro", methods=["GET", "POST"])
def crear_accion_registro():
    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()
        if not nombre:
            flash("El nombre de la acción es requerido.", "warning")
            return render_template("admin_accion_form.html", accion=None)
        db.session.add(Acciones(Nombre=nombre, estado=1))
        db.session.commit()
        flash("Acción creada correctamente.", "success")
        return redirect(url_for("ver_permisos_empleado", modulo="acciones_admin"))
    return render_template("admin_accion_form.html", accion=None)


@app.route("/editar_accion_registro/<int:id_accion>", methods=["GET", "POST"])
def editar_accion_registro(id_accion):
    accion = db.session.get(Acciones, id_accion)
    if not accion:
        flash("Acción no encontrada.", "danger")
        return redirect(url_for("ver_permisos_empleado", modulo="acciones_admin"))
    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()
        if not nombre:
            flash("El nombre de la acción es requerido.", "warning")
            return render_template("admin_accion_form.html", accion=accion)
        accion.Nombre = nombre
        db.session.commit()
        flash("Acción actualizada correctamente.", "success")
        return redirect(url_for("ver_permisos_empleado", modulo="acciones_admin"))
    return render_template("admin_accion_form.html", accion=accion)


@app.route("/toggle_pantalla_estado/<int:id_pantalla>", methods=["POST"])
def toggle_pantalla_estado(id_pantalla):
    pantalla = db.session.get(Pantallas, id_pantalla)
    if pantalla:
        pantalla.estado = 0 if pantalla.estado == 1 else 1
        db.session.commit()
    return redirect(url_for("ver_permisos_empleado", modulo="pantallas_admin"))


@app.route("/crear_pantalla_registro", methods=["GET", "POST"])
def crear_pantalla_registro():
    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()
        url_val = (request.form.get("url") or "").strip()
        if not nombre or not url_val:
            flash("Nombre y endpoint son requeridos.", "warning")
            return render_template("admin_pantalla_form.html", pantalla=None)
        db.session.add(Pantallas(Nombre=nombre, url=url_val, estado=1))
        db.session.commit()
        flash("Pantalla creada correctamente.", "success")
        return redirect(url_for("ver_permisos_empleado", modulo="pantallas_admin"))
    return render_template("admin_pantalla_form.html", pantalla=None)


@app.route("/editar_pantalla_registro/<int:id_pantalla>", methods=["GET", "POST"])
def editar_pantalla_registro(id_pantalla):
    pantalla = db.session.get(Pantallas, id_pantalla)
    if not pantalla:
        flash("Pantalla no encontrada.", "danger")
        return redirect(url_for("ver_permisos_empleado", modulo="pantallas_admin"))
    if request.method == "POST":
        pantalla.Nombre = (request.form.get("nombre") or "").strip()
        pantalla.url = (request.form.get("url") or "").strip()
        if not pantalla.Nombre or not pantalla.url:
            flash("Nombre y endpoint son requeridos.", "warning")
            return render_template("admin_pantalla_form.html", pantalla=pantalla)
        db.session.commit()
        flash("Pantalla actualizada correctamente.", "success")
        return redirect(url_for("ver_permisos_empleado", modulo="pantallas_admin"))
    return render_template("admin_pantalla_form.html", pantalla=pantalla)


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
