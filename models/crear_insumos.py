from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.insumo_model import Insumo
from models.categoria_insumo_model import CategoriaInsumo
from sqlalchemy import text

bp_crear_insumo = Blueprint('crear_insumo', __name__, url_prefix='/crear_insumo')

@bp_crear_insumo.route('/', methods=['GET'])
def formulario_crear_insumo():

    unidades = db.session.execute(
        text("SELECT ID_Unidad, Nombre, abreviatura FROM Unidades_medida")
    ).fetchall()
    categorias = CategoriaInsumo.query.all()

    nombres = [n.Nombre_insumo.lower() for n in Insumo.query.all()]

    return render_template(
        'crear_insumo.html',
        unidades=unidades,
        categorias=categorias,
        nombres=nombres
    )



@bp_crear_insumo.route('/guardar', methods=['POST'])
def guardar_insumo():

    nombre = request.form.get('nombre')
    stock_total = request.form.get('stock_total')
    stock_minimo = request.form.get('stock_minimo')
    precio_lempiras = request.form.get('precio_lempiras')
    peso_individual = request.form.get('peso_individual')
    ID_Unidad = request.form.get('ID_Unidad')
    ID_Categoria = request.form.get('ID_Categoria')

    if not nombre or not ID_Unidad or not ID_Categoria:
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('crear_insumo.formulario_crear_insumo'))

    nuevo = Insumo(
        Nombre_insumo=nombre.strip(),
        stock_total=stock_total,
        stock_minimo=stock_minimo,
        precio_lempiras=precio_lempiras,
        peso_individual=peso_individual,
        ID_Unidad=ID_Unidad,
        ID_Categoria=ID_Categoria
    )

    db.session.add(nuevo)
    db.session.commit()

    flash('Insumo creado correctamente.', 'success')
    return redirect(url_for('insumos.listar_insumos'))
