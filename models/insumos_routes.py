from flask import Blueprint, render_template
from models.insumo_model import Insumo

insumos_routes = Blueprint('insumos_routes', __name__)

@insumos_routes.route('/insumos')
def listar_insumos():
    insumos = Insumo.query.all()
    return render_template('insumos.html', insumos=insumos)
