from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.receta_model import Receta
from models.usuario_cliente_model import UsuarioCliente
from sqlalchemy import text

pagina_principal_bp = Blueprint("pagina_principal_bp", __name__)


def _cliente_id():
    cid = session.get("cliente_id")
    if cid is not None:
        try:
            return int(cid)
        except Exception:
            return None

    if getattr(current_user, "is_authenticated", False):
        v = getattr(current_user, "ID_Usuario_ClienteF", None) or getattr(current_user, "db_id", None) or getattr(current_user, "id", None)
        if v is not None:
            try:
                return int(v)
            except Exception:
                return None

    return None


def _cliente_sucursal_id():
    cid = _cliente_id()
    if cid is None:
        return None

    cliente = UsuarioCliente.query.get(cid)
    if not cliente:
        return None

    sid = getattr(cliente, "ID_sucursal", None) or getattr(cliente, "id_sucursal", None)
    if sid is None:
        return None

    try:
        return int(sid)
    except Exception:
        return None


@pagina_principal_bp.route("/menu")
@login_required
def menu():
    sid = _cliente_sucursal_id()
    if sid is None:
        flash("No se pudo determinar tu sucursal.", "danger")
        return redirect(url_for("login"))

    categorias_query = db.session.execute(text("""
        SELECT id_categoria_receta, Nombre_categoria_receta
        FROM categoria_recetas
        ORDER BY Nombre_categoria_receta
    """)).fetchall()

    categorias = {c.Nombre_categoria_receta: [] for c in categorias_query}

    recetas = Receta.query.filter(
        Receta.Estado == 1,
        Receta.ID_sucursal == sid
    ).all()

    for receta in recetas:
        total_costo = db.session.execute(text("""
            SELECT 
                SUM((i.precio_lempiras / NULLIF(i.peso_individual, 0)) * ir.cantidad_usada) AS total
            FROM IN_RE ir
            JOIN Insumos i ON i.ID_Insumo = ir.ID_Insumo
            WHERE ir.ID_Receta = :id_receta
              AND ir.Activo = 1
              AND ir.ID_sucursal = :sid
        """), {"id_receta": receta.ID_Receta, "sid": sid}).scalar() or 0

        categoria_nombre = db.session.execute(text("""
            SELECT Nombre_categoria_receta 
            FROM categoria_recetas 
            WHERE id_categoria_receta = :id
        """), {"id": receta.categoria}).scalar() or "Sin categoría"

        if categoria_nombre not in categorias:
            categorias[categoria_nombre] = []

        id_in_re = db.session.execute(text("""
            SELECT TOP 1 ID_IN_RE
            FROM IN_RE
            WHERE ID_Receta = :id_receta
              AND Activo = 1
              AND ID_sucursal = :sid
            ORDER BY ID_IN_RE
        """), {"id_receta": receta.ID_Receta, "sid": sid}).scalar()

        if id_in_re is None:
            continue

        categorias[categoria_nombre].append({
            "ID_IN_RE": id_in_re,
            "nombre": receta.Nombre_receta,
            "descripcion": receta.descripcion or "Platillo especial del día",
            "precio": f"LPS. {float(total_costo):.2f}",
        })

    return render_template("menu.html", categorias=categorias)


@pagina_principal_bp.route("/ver_receta/<int:id_receta>")
@login_required
def ver_receta(id_receta):
    sid = _cliente_sucursal_id()
    if sid is None:
        flash("No se pudo determinar tu sucursal.", "danger")
        return redirect(url_for("login"))

    receta = db.session.execute(text("""
        SELECT r.Nombre_receta, r.Descripcion AS descripcion, j.Nombre AS jefe
        FROM Recetas r
        JOIN Jefe_de_cocina j ON r.ID_Jefe_de_cocina = j.ID_Jefe_de_cocina
        WHERE r.ID_Receta = :id
          AND r.ID_sucursal = :sid
          AND r.Estado = 1
    """), {"id": id_receta, "sid": sid}).fetchone()

    if not receta:
        return render_template("ver_receta.html", error="Receta no encontrada")

    ingredientes = db.session.execute(text("""
        SELECT 
            i.Nombre_insumo,
            ir.cantidad_usada,
            u.Nombre_Unidad
        FROM IN_RE ir
        JOIN Insumos i ON i.ID_Insumo = ir.ID_Insumo
        JOIN Unidades_Conversion u ON u.ID_Unidad = ir.ID_Unidad
        WHERE ir.ID_Receta = :id
          AND ir.Activo = 1
          AND ir.ID_sucursal = :sid
    """), {"id": id_receta, "sid": sid}).fetchall()

    return render_template("ver_receta.html", receta=receta, ingredientes=ingredientes)
