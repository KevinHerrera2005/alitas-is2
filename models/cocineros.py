from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from sqlalchemy import text

bp_cocineros = Blueprint("bp_cocineros", __name__, url_prefix="/cocineros")


@bp_cocineros.route("/")
def listar_cocineros():
    cocineros = db.session.execute(text("""
        SELECT ID_cocinero, Nombre, apellido, descripcion, activo
        FROM cocineros
        ORDER BY Nombre
    """)).fetchall()

    return render_template("cocineros.html", cocineros=cocineros)


@bp_cocineros.route("/toggle/<int:id>", methods=["POST"])
def toggle_estado(id):
    estado = db.session.execute(text("""
        SELECT activo FROM cocineros WHERE ID_cocinero = :id
    """), {"id": id}).fetchone()

    nuevo_estado = 0 if estado.activo == 1 else 1

    db.session.execute(text("""
        UPDATE cocineros SET activo = :nuevo WHERE ID_cocinero = :id
    """), {"nuevo": nuevo_estado, "id": id})

    db.session.commit()

    return redirect(url_for("bp_cocineros.listar_cocineros"))

