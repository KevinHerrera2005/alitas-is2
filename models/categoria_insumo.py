from flask import Blueprint, render_template
from models import db
from sqlalchemy import text
from flask import Blueprint, render_template, redirect, url_for
bp_categoria_insumo = Blueprint('categoria_insumo', __name__, url_prefix='/categorias')

@bp_categoria_insumo.route('/')
def listar_categorias():

    categorias = db.session.execute(text("""
        SELECT ID_Categoria, Nombre_Categoria, descripcion, estado
        FROM categorias
        ORDER BY ID_Categoria
    """)).fetchall()

    return render_template(
        'categoria_insumo.html',
        categorias=categorias
    )
@bp_categoria_insumo.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_categoria(id):
    try:
        db.session.execute(text("DELETE FROM categorias WHERE ID_Categoria = :id"), {"id": id})
        db.session.commit()
    except Exception as e:
        print("❌ Error al eliminar categoría:", e)
        db.session.rollback()

    return redirect(url_for('categoria_insumo.listar_categorias'))
