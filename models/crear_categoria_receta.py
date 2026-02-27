from flask import render_template, request, redirect, url_for, flash
from models import db
from sqlalchemy import text

def crear_categoria_receta_routes(app):
    @app.route('/crear_categoria_receta', methods=['GET', 'POST'])
    def crear_categoria_receta():
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')

            if not nombre or not descripcion:
                flash("Todos los campos son obligatorios.", "warning")
                return redirect(url_for('crear_categoria_receta'))

            try:
                existente = db.session.execute(text("""
                    SELECT COUNT(*) FROM categoria_recetas WHERE Nombre_categoria_receta = :nombre
                """), {"nombre": nombre}).scalar()

                if existente > 0:
                    flash(f"La categoría '{nombre}' ya existe.", "warning")
                    return redirect(url_for('crear_categoria_receta'))

                db.session.execute(text("""
                    INSERT INTO categoria_recetas (Nombre_categoria_receta, descripcion)
                    VALUES (:nombre, :descripcion)
                """), {"nombre": nombre, "descripcion": descripcion})

                db.session.commit()
                flash(f"✅ Categoría '{nombre}' creada correctamente.", "success")
                return redirect(url_for('crear_receta'))

            except Exception as e:
                db.session.rollback()
                flash(f"Error al crear la categoría: {e}", "danger")
                return redirect(url_for('crear_categoria_receta'))

        return render_template('crear_categoria_receta.html')
