from datetime import datetime

from sqlalchemy import event, inspect, text

from models.insumo_precio_historico_model import InsumoPrecioHistorico
from models import db


class Insumo(db.Model):
    __tablename__ = "Insumos"

    ID_Insumo = db.Column(db.Integer, primary_key=True)
    Nombre_insumo = db.Column(db.String(50), nullable=False)

    stock_total = db.Column(db.Float)
    stock_minimo = db.Column(db.Float)
    stock_maximo = db.Column(db.Float)

    precio_base = db.Column(db.Float)
    precio_lempiras = db.Column(db.Float)

    peso_individual = db.Column(db.Float)

    ID_sucursal = db.Column(db.Integer, db.ForeignKey("Sucursales.ID_sucursal"), nullable=False)
    sucursal = db.relationship("Sucursal", lazy="joined")

    ID_Unidad = db.Column(db.Integer, db.ForeignKey("Unidades_medida.ID_Unidad"))
    unidad = db.relationship("Unidades_medida", lazy="joined")

    ID_Categoria = db.Column(db.Integer, db.ForeignKey("categorias.ID_Categoria"))
    categoria = db.relationship("CategoriaInsumo", lazy="joined")


@event.listens_for(Insumo, "before_insert")
def calcular_precios_antes_insert(mapper, connection, target):
    base = target.precio_base
    final = target.precio_lempiras

    if base is None and final is not None:
        base = final
        target.precio_base = final

    if base is None:
        raise ValueError("Debes indicar el precio base del insumo.")

    tasa_total = 0.0

    if target.ID_Categoria is not None:
        resultado = connection.execute(
            text(
                """
                SELECT SUM(CAST(i.tasa AS FLOAT))
                FROM Impuestos AS i
                INNER JOIN Impuesto_Categoria AS ic
                    ON ic.ID_Impuesto = i.ID_Impuesto
                WHERE ic.ID_Categoria = :cat
                  AND ic.Activo = 1
                  AND i.activo = 1
                """
            ),
            {"cat": target.ID_Categoria},
        ).scalar()

        if resultado is not None:
            tasa_total = float(resultado)

    factor = 1.0 + (tasa_total / 100.0)
    target.precio_lempiras = float(base) * factor


@event.listens_for(Insumo, "after_insert")
def crear_historial_inicial_insumo(mapper, connection, target):
    connection.execute(
        InsumoPrecioHistorico.__table__.insert().values(
            ID_Insumo=target.ID_Insumo,
            fecha_inicio=datetime.now(),
            fecha_fin=None,
            Precio=target.precio_lempiras,
        )
    )


@event.listens_for(Insumo, "before_update")
def recalcular_y_registrar_precio_insumo(mapper, connection, target):
    state = inspect(target)

    base_changed = state.attrs.precio_base.history.has_changes()
    cat_changed = state.attrs.ID_Categoria.history.has_changes()

    if base_changed or cat_changed:
        base = target.precio_base
        if base is None:
            base = 0

        tasa_total = 0.0

        if target.ID_Categoria is not None:
            resultado = connection.execute(
                text(
                    """
                    SELECT SUM(CAST(i.tasa AS FLOAT))
                    FROM Impuestos AS i
                    INNER JOIN Impuesto_Categoria AS ic
                        ON ic.ID_Impuesto = i.ID_Impuesto
                    WHERE ic.ID_Categoria = :cat
                      AND ic.Activo = 1
                      AND i.activo = 1
                    """
                ),
                {"cat": target.ID_Categoria},
            ).scalar()

            if resultado is not None:
                tasa_total = float(resultado)

        factor = 1.0 + (tasa_total / 100.0)
        target.precio_lempiras = float(base) * factor

    hist_final = state.attrs.precio_lempiras.history

    if not hist_final.has_changes():
        return

    nuevo_precio = hist_final.added[0] if hist_final.added else target.precio_lempiras

    connection.execute(
        InsumoPrecioHistorico.__table__.update()
        .where(
            (InsumoPrecioHistorico.ID_Insumo == target.ID_Insumo)
            & (InsumoPrecioHistorico.fecha_fin.is_(None))
        )
        .values(fecha_fin=datetime.now())
    )

    connection.execute(
        InsumoPrecioHistorico.__table__.insert().values(
            ID_Insumo=target.ID_Insumo,
            fecha_inicio=datetime.now(),
            fecha_fin=None,
            Precio=nuevo_precio,
        )
    )
