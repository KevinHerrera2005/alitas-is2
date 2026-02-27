from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from sqlalchemy import text

bp_crear_categoria_insumo = Blueprint(
    'crear_categoria_insumo',
    __name__,
    url_prefix='/crear_categoria_insumo'
)

@bp_crear_categoria_insumo.route('/', methods=['GET', 'POST'])
def formulario_crear_categoria_insumo():

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        if not nombre or not descripcion:
            flash("Completa todos los campos", "warning")
            return redirect(url_for('crear_categoria_insumo.formulario_crear_categoria_insumo'))

        try:
            db.session.execute(text("""
                INSERT INTO categorias (Nombre_Categoria, descripcion, estado)
                VALUES (:nombre, :descripcion, 1)
            """), {
                "nombre": nombre,
                "descripcion": descripcion
            })

            db.session.commit()
            flash("Categoría agregada correctamente", "success")
            return redirect(url_for('categoria_insumo.listar_categorias'))

        except Exception as e:
            print("❌ Error al crear categoría:", e)
            db.session.rollback()
            flash("Error al crear categoría", "danger")

    return render_template('crear_categoria_insumo.html')
