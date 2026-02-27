from flask import flash, redirect, url_for
from models.login_crear_usuario import db  
from sqlalchemy import text


def validar_y_calcular_costo(id_insumo, cantidad, id_unidad_ingresada):
    
    insumo = db.session.execute(
        text(f"SELECT * FROM Insumos WHERE ID_Insumo = {id_insumo}")
    ).fetchone()

    if not insumo:
        flash("El insumo seleccionado no existe.", "danger")
        return redirect(url_for('gestion_recetas')), None

    
    unidad_ingresada = db.session.execute(
        text(f"SELECT Equivalente, Nombre_Unidad FROM Unidades_Conversion WHERE ID_Unidad = {id_unidad_ingresada}")
    ).fetchone()

    unidad_base = db.session.execute(
        text(f"SELECT Equivalente, Nombre_Unidad FROM Unidades_Conversion WHERE ID_Unidad = {insumo.ID_Unidad}")
    ).fetchone()

    
    if not unidad_ingresada or not unidad_base:
        flash("Error al obtener las unidades de medida.", "danger")
        return redirect(url_for('gestion_recetas')), None

    
    cantidad_convertida = cantidad * (unidad_ingresada.Equivalente / unidad_base.Equivalente)

    
    if cantidad <= 0:
        flash("La cantidad no puede ser menor o igual a cero.", "warning")
        return redirect(url_for('gestion_recetas')), None

    
    if cantidad_convertida > insumo.Stock_total:
        flash(
            f"No hay suficiente stock disponible. Stock actual: {insumo.Stock_total} {unidad_base.Nombre_Unidad}",
            "danger"
        )
        return redirect(url_for('gestion_recetas')), None

    
    if insumo.peso_individual and insumo.peso_individual > 0:
        precio_unitario = insumo.precio_lempiras / insumo.peso_individual
        costo_usado = round(precio_unitario * cantidad_convertida, 2)
    else:
        costo_usado = 0

    
    return None, {"cantidad_convertida": cantidad_convertida, "costo_usado": costo_usado}
