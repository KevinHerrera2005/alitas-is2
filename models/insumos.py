from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.insumo_model import Insumo
from sqlalchemy import text

bp_insumos = Blueprint('insumos', __name__, url_prefix='/insumos')

@bp_insumos.route('/', methods=['GET'])
def listar_insumos():

    insumos = Insumo.query.all()
    return render_template('insumos.html', insumos=insumos)

@bp_insumos.route('/agregar', methods=['POST'])
def agregar_insumo():

    nombre = request.form.get('nombre')
    stock_total = request.form.get('stock_total')
    stock_minimo = request.form.get('stock_minimo')
    precio_lempiras = request.form.get('precio_lempiras')
    peso_individual = request.form.get('peso_individual')

    errores = []
    if not nombre or len(nombre.strip()) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    try:
        stock_total = float(stock_total)
        stock_minimo = float(stock_minimo)
        precio_lempiras = float(precio_lempiras)
        peso_individual = float(peso_individual)
    except ValueError:
        errores.append("Todos los valores numéricos deben ser números válidos.")
    else:
        if stock_total <= 0 or stock_minimo <= 0 or precio_lempiras <= 0 or peso_individual <= 0:
            errores.append("Los valores numéricos deben ser mayores que 0.")

    if errores:
        for e in errores:
            flash(e, 'danger')
        return redirect(url_for('insumos.listar_insumos'))

    nuevo = Insumo(
        Nombre_insumo=nombre.strip(),
        stock_total=stock_total,
        stock_minimo=stock_minimo,
        precio_lempiras=precio_lempiras,
        peso_individual=peso_individual
    )
    db.session.add(nuevo)
    db.session.commit()
    flash('✅ Insumo agregado correctamente.', 'success')
    return redirect(url_for('insumos.listar_insumos'))

@bp_insumos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_insumo(id):
    try:
        db.session.execute(text(
            "DELETE FROM IN_RE WHERE ID_Insumo = :id"
        ), {"id": id})

        db.session.execute(text(
            "DELETE FROM Insumos WHERE ID_Insumo = :id"
        ), {"id": id})

        db.session.commit()

    except Exception as e:
        print("❌ Error al eliminar insumo:", e)
        db.session.rollback()

    return redirect(url_for('insumos.listar_insumos'))


