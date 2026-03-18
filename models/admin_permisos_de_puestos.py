from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from Main import app, db
from .permisos_puesto_model import PermisosPuesto
from .pantallas_acciones_model import PantallasAcciones
from .Pantallas_model import Pantallas
from .empleado_model import Puesto
from .Acciones_model import Acciones
from .permisos_empleado_model import PermisosEmpleado


def _borrar_permisos_puesto_por_ids(ids_permiso_puesto):
    """Borra PermisosEmpleado dependientes y luego los PermisosPuesto indicados."""
    if not ids_permiso_puesto:
        return
    db.session.query(PermisosEmpleado).filter(
        PermisosEmpleado.ID_Permiso_Puesto.in_(ids_permiso_puesto)
    ).delete(synchronize_session=False)
    db.session.query(PermisosPuesto).filter(
        PermisosPuesto.ID_Permiso_Puesto.in_(ids_permiso_puesto)
    ).delete(synchronize_session=False)


@app.route("/ver_permisospuesto", methods=["GET", "POST"])
def ver_permisos_puesto():
    from models.permisos_mixin import endpoint_accesible
    if not current_user.is_authenticated or getattr(current_user, "tipo", None) != "empleado" or not endpoint_accesible("ver_permisos_puesto"):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        eliminar = request.form.get("eliminar")
        if eliminar:
            ids = [r[0] for r in db.session.query(PermisosPuesto.ID_Permiso_Puesto).filter(
                PermisosPuesto.ID_Puesto == int(eliminar)
            ).all()]
            _borrar_permisos_puesto_por_ids(ids)
            db.session.commit()
            flash("Permisos del puesto eliminados correctamente", "success")
            return redirect(url_for("ver_permisos_empleado", modulo="permisos_puesto"))

    registro_permisos_puestos = db.session.query(
        Puesto.Nombre_Puesto,
        Puesto.ID_Puesto
    ).join(
        PermisosPuesto, Puesto.ID_Puesto == PermisosPuesto.ID_Puesto
    ).distinct().all()

    return render_template("permisos_del_puesto.html", registro_permisos_puestos=registro_permisos_puestos)


@app.route("/ver_acciones_puesto/<int:id_puesto>", methods=["GET"])
def ver_acciones_puesto(id_puesto):
    puesto = db.session.get(Puesto, id_puesto)

    resultados = db.session.query(
        Pantallas.Nombre,
        Acciones.Nombre
    ).select_from(PermisosPuesto).join(
        PantallasAcciones, PantallasAcciones.ID_Pantalla_Accion == PermisosPuesto.ID_Pantalla_Accion
    ).join(
        Pantallas, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla
    ).join(
        Acciones, Acciones.ID_Accion == PantallasAcciones.ID_Accion
    ).filter(
        PermisosPuesto.ID_Puesto == id_puesto
    ).all()

    pantallas_dict = {}
    for nombre_pantalla, nombre_accion in resultados:
        if nombre_pantalla not in pantallas_dict:
            pantallas_dict[nombre_pantalla] = []
        pantallas_dict[nombre_pantalla].append(nombre_accion)

    return render_template("ver_acciones_puesto.html", puesto=puesto, pantallas=pantallas_dict)


@app.route("/editar_permisos_puesto/<int:id_puesto>", methods=["GET", "POST"])
def editar_permisos_puesto(id_puesto):
    puesto = db.session.get(Puesto, id_puesto)

    pantallas_disponibles = db.session.query(Pantallas.ID_Pantalla, Pantallas.Nombre).join(
        PantallasAcciones, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla
    ).distinct().all()

    pantallas_asignadas_ids = {
        r[0] for r in db.session.query(PantallasAcciones.ID_Pantalla).join(
            PermisosPuesto, PermisosPuesto.ID_Pantalla_Accion == PantallasAcciones.ID_Pantalla_Accion
        ).filter(PermisosPuesto.ID_Puesto == id_puesto).distinct().all()
    }

    if request.method == "POST":
        pantallas_seleccionadas = request.form.getlist("pantallas")

        ids = [r[0] for r in db.session.query(PermisosPuesto.ID_Permiso_Puesto).filter(
            PermisosPuesto.ID_Puesto == id_puesto
        ).all()]
        _borrar_permisos_puesto_por_ids(ids)

        for id_pantalla in pantallas_seleccionadas:
            acciones = db.session.query(PantallasAcciones).filter(
                PantallasAcciones.ID_Pantalla == int(id_pantalla)
            ).all()
            for accion in acciones:
                db.session.add(PermisosPuesto(
                    ID_Puesto=id_puesto,
                    ID_Pantalla_Accion=accion.ID_Pantalla_Accion
                ))

        db.session.commit()
        flash("Permisos actualizados correctamente", "success")
        return redirect(url_for("ver_permisos_puesto"))

    return render_template(
        "editar_permisos_puesto.html",
        puesto=puesto,
        pantallas_disponibles=pantallas_disponibles,
        pantallas_asignadas_ids=pantallas_asignadas_ids
    )


@app.route("/crear_permisos_puesto", methods=["GET", "POST"])
def crear_permisos_puesto():
    puestos = db.session.query(Puesto.ID_Puesto, Puesto.Nombre_Puesto).all()
    pantalla_accion = db.session.query(Pantallas.ID_Pantalla, Pantallas.Nombre).join(
        PantallasAcciones, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla
    ).distinct().all()

    if request.method == "POST":
        puesto = request.form.get("puesto")
        pantallas_seleccionadas = request.form.getlist("pantalla_accion")

        for id_pantalla in pantallas_seleccionadas:
            if id_pantalla != "":
                acciones_de_pantalla = db.session.query(PantallasAcciones).filter(
                    PantallasAcciones.ID_Pantalla == int(id_pantalla)
                ).all()
                for accion in acciones_de_pantalla:
                    db.session.add(PermisosPuesto(
                        ID_Puesto=int(puesto),
                        ID_Pantalla_Accion=accion.ID_Pantalla_Accion
                    ))
        db.session.commit()
        return redirect(url_for("ver_permisos_puesto"))

    return render_template("crear_permisos_puesto.html", puestos=puestos, pantalla_accion=pantalla_accion)
