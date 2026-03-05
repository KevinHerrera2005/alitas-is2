from mensajes_logs import logger_
from datetime import datetime
import traceback


from flask import render_template, jsonify, request, redirect, url_for, flash
from flask_login import current_user
from models import db
from models.receta_model import Receta
from sqlalchemy import text

def gestion_receta_routes(app):
    def _sucursal_id_actual():
        sid = getattr(current_user, "id_sucursal", None) or getattr(current_user, "ID_sucursal", None)
        return int(sid) if sid is not None else None

    def _es_jefe_cocina():
        if not current_user.is_authenticated:
            return False
        if getattr(current_user, "tipo", None) != "empleado":
            return False
        puesto = getattr(current_user, "id_puesto", None) or getattr(current_user, "ID_Puesto", None)
        return int(puesto) == 1

    # este boton es para abrir el listado de recetas desde el panel del jefe de cocina
    @app.route("/crud_recetas")
    def crud_recetas(*args,**kwargs):
        try:

            sid = _sucursal_id_actual()


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
        except Exception as error:
                fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
                logger_.Logger.add_to_log("error", str(error), "listado_recetas(boton del panel)", fecha)
                logger_.Logger.add_to_log("error", traceback.format_exc(), "listado_recetas(boton del panel)", fecha)
                return "esto es un error", 501
    # este boton es para cambiar el estado de la receta entre activo e inactivo
    @app.route("/toggle_receta_estado", methods=["POST"])
    def toggle_receta_estado(*args,**kwargs):
        try:

            sid = _sucursal_id_actual()

            data = request.get_json(silent=True) or {}
            id_receta = data.get("id_receta")


            receta = Receta.query.get(id_receta)


            nuevo_estado = 0 if receta.Estado == 1 else 1
            receta.Estado = nuevo_estado

            db.session.add(receta)
            db.session.commit()

            return jsonify({"success": True, "nuevo_estado": nuevo_estado}), 200
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "gestion_recetas_boton_activar_desactivar_receta", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "gestion_recetas_boton_activar_desactivar_receta", fecha)
            return "esto es un error", 501

    # este boton es para borrar una receta
    @app.route("/eliminar_receta/<int:id_receta>", methods=["DELETE"])
    def eliminar_receta(id_receta,*args,**kwargs):
        try:

            sid = _sucursal_id_actual()

            receta = Receta.query.get(id_receta)

            if not receta:
                return jsonify({"success": False, "message": "La receta no existe."}), 404


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

        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "gestion_recetas_borrar_una_receta", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "gestion_recetas_borrar_una_receta", fecha)
            return "esto es un error", 501
        
    # este boton es para borrar una categoria de recetas
    @app.route("/eliminar_categoria/<path:nombre_categoria>", methods=["DELETE"])
    def eliminar_categoria(nombre_categoria,*args,**kwargs):
        try:

            nombre = (nombre_categoria or "").strip()
            if not nombre:
                return jsonify({"success": False, "message": "Categoría inválida"}), 400

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
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "gestion_recetas_borrar_una_categoria", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "gestion_recetas_borrar_una_categoria", fecha)
            return "esto es un error", 501
        

    # este boton es para ver los ingredientes y detalles de una receta
    @app.route("/jefe/ver_receta/<int:id_receta>")
    def jefe_ver_receta(id_receta,*args,**kwargs):
        try:

            sid = _sucursal_id_actual()

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
        except Exception as error:
            fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
            logger_.Logger.add_to_log("error", str(error), "gestion_recetas_ver_ingredientes", fecha)
            logger_.Logger.add_to_log("error", traceback.format_exc(), "gestion_recetas_ver_ingredientes", fecha)
            return "esto es un error", 501