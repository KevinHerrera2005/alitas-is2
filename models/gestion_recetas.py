from flask import render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.receta_model import Receta
from sqlalchemy import text


def gestion_receta_routes(app):
    def _sucursal_id_actual():
        sid = getattr(current_user, "id_sucursal", None) or getattr(current_user, "ID_sucursal", None)
        try:
            return int(sid) if sid is not None else None
        except Exception:
            return None

    def _es_jefe_cocina():
        if not current_user.is_authenticated:
            return False
        if getattr(current_user, "tipo", None) != "empleado":
            return False
        puesto = getattr(current_user, "id_puesto", None) or getattr(current_user, "ID_Puesto", None)
        try:
            return int(puesto) == 1
        except Exception:
            return False

    @app.route("/crud_recetas")
    @login_required
    def crud_recetas():
        if not _es_jefe_cocina():
            flash("No tienes permiso para acceder a este panel.", "danger")
            return redirect(url_for("login"))

        sid = _sucursal_id_actual()
        if sid is None:
            flash("No se pudo determinar tu sucursal.", "danger")
            return redirect(url_for("login"))

        recetas = Receta.query.filter(Receta.ID_sucursal == sid).all()

        categorias_query = db.session.execute(text("""
            SELECT id_categoria_receta, Nombre_categoria_receta
            FROM categoria_recetas
            ORDER BY id_categoria_receta
        """)).fetchall()

        categoria_por_id = {
            c.id_categoria_receta: c.Nombre_categoria_receta
            for c in categorias_query
        }

        categorias = {
            c.Nombre_categoria_receta: []
            for c in categorias_query
        }

        nombres_categorias = [c.Nombre_categoria_receta for c in categorias_query]

        for receta in recetas:
            total_costo_query = db.session.execute(text("""
                SELECT SUM(ir.precio_final) AS total
                FROM IN_RE ir
                WHERE ir.ID_Receta = :id AND ir.Activo = 1 AND ir.ID_sucursal = :sid
            """), {"id": receta.ID_Receta, "sid": sid}).scalar()

            total_costo = float(total_costo_query or 0.0)
            activo = int(receta.Estado or 0)

            categoria_nombre = categoria_por_id.get(receta.categoria, "Sin categoría")

            if categoria_nombre not in categorias:
                categorias[categoria_nombre] = []
                nombres_categorias.append(categoria_nombre)

            categorias[categoria_nombre].append({
                "id": receta.ID_Receta,
                "nombre": receta.Nombre_receta,
                "descripcion": receta.descripcion or "Sin descripción.",
                "precio": f"LPS. {total_costo:.2f}",
                "activo": activo,
            })

        return render_template(
            "crud_recetas.html",
            categorias=categorias,
            nombres_categorias=nombres_categorias
        )

    @app.route("/toggle_receta_estado", methods=["POST"])
    @login_required
    def toggle_receta_estado():
        if not _es_jefe_cocina():
            return jsonify({"success": False, "message": "No autorizado"}), 403

        sid = _sucursal_id_actual()
        if sid is None:
            return jsonify({"success": False, "message": "Sucursal inválida"}), 403

        data = request.get_json() or {}
        id_receta = data.get("id_receta")

        receta = Receta.query.get_or_404(id_receta)

        if int(getattr(receta, "ID_sucursal", -1)) != sid:
            return jsonify({"success": False, "message": "No autorizado"}), 403

        nuevo_estado = 0 if receta.Estado == 1 else 1
        receta.Estado = nuevo_estado

        db.session.add(receta)
        db.session.commit()

        return jsonify({"nuevo_estado": nuevo_estado})

    @app.route("/eliminar_receta/<int:id_receta>", methods=["DELETE"])
    @login_required
    def eliminar_receta(id_receta):
        if not _es_jefe_cocina():
            return jsonify({"success": False, "message": "No autorizado"}), 403

        sid = _sucursal_id_actual()
        if sid is None:
            return jsonify({"success": False, "message": "Sucursal inválida"}), 403

        receta = Receta.query.get_or_404(id_receta)

        if int(getattr(receta, "ID_sucursal", -1)) != sid:
            return jsonify({"success": False, "message": "No autorizado"}), 403

        try:
            db.session.execute(
                text("DELETE FROM IN_RE WHERE ID_Receta = :id AND ID_sucursal = :sid"),
                {"id": id_receta, "sid": sid}
            )

            db.session.execute(
                text("DELETE FROM recetas_precio_historico WHERE ID_Receta = :id"),
                {"id": id_receta}
            )

            resultado = db.session.execute(
                text("DELETE FROM Recetas WHERE ID_Receta = :id AND ID_sucursal = :sid"),
                {"id": id_receta, "sid": sid}
            )

            db.session.commit()

            if resultado.rowcount == 0:
                return jsonify({
                    "success": False,
                    "message": "La receta no existe o no tienes permiso."
                }), 404

            return jsonify({
                "success": True,
                "message": "Su receta se ha eliminado correctamente."
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": "Su receta no se ha podido eliminar.",
                "error": str(e)
            }), 500
    @app.route("/eliminar_categoria/<path:nombre_categoria>", methods=["DELETE"])
    @login_required
    def eliminar_categoria(nombre_categoria):
        if not _es_jefe_cocina():
            return jsonify({"success": False, "message": "No autorizado"}), 403

        nombre = (nombre_categoria or "").strip()
        if not nombre:
            return jsonify({"success": False, "message": "Categoría inválida"}), 400

        try:
            fila = db.session.execute(
                text("""
                    SELECT id_categoria_receta
                    FROM categoria_recetas
                    WHERE Nombre_categoria_receta = :n
                """),
                {"n": nombre}
            ).fetchone()

            if not fila:
                return jsonify({"success": False, "message": "Categoría no encontrada"}), 404

            id_cat = int(fila.id_categoria_receta)

            usados = db.session.execute(
                text("SELECT COUNT(1) FROM Recetas WHERE categoria = :id_cat"),
                {"id_cat": id_cat}
            ).scalar() or 0

            if int(usados) > 0:
                return jsonify({
                "success": False,
                "message": "No se puede eliminar la categoría porque tiene recetas asociadas. Primero mueve o elimina esas recetas."
                }), 409

            res = db.session.execute(
                text("DELETE FROM categoria_recetas WHERE id_categoria_receta = :id_cat"),
                {"id_cat": id_cat}
            )

            db.session.commit()

            if res.rowcount == 0:
                return jsonify({"success": False, "message": "Categoría no encontrada"}), 404

            return jsonify({"success": True, "message": "Categoría eliminada correctamente"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": "No se pudo eliminar la categoría", "error": str(e)}), 500
    
    
    
    @app.route("/jefe/ver_receta/<int:id_receta>")
    @login_required
    def jefe_ver_receta(id_receta):
        if not _es_jefe_cocina():
            flash("No tienes permiso para acceder a este panel.", "danger")
            return redirect(url_for("login"))

        sid = _sucursal_id_actual()
        if sid is None:
            flash("No se pudo determinar tu sucursal.", "danger")
            return redirect(url_for("login"))

        receta = db.session.execute(text("""
            SELECT r.Nombre_receta, r.Descripcion AS descripcion, j.Nombre AS jefe
            FROM Recetas r
            JOIN Jefe_de_cocina j ON r.ID_Jefe_de_cocina = j.ID_Jefe_de_cocina
            WHERE r.ID_Receta = :id
              AND r.ID_sucursal = :sid
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
