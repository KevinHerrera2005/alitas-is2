from models import db


class IN_RE(db.Model):
    __tablename__ = "IN_RE"
    __table_args__ = {"implicit_returning": False}

    ID_IN_RE = db.Column(db.Integer, primary_key=True)

    Activo = db.Column(db.Integer, nullable=False, default=1)

    ID_sucursal = db.Column(
        db.Integer,
        db.ForeignKey("Sucursales.ID_sucursal"),
        nullable=False,
    )

    ID_Insumo = db.Column(
        db.Integer,
        db.ForeignKey("Insumos.ID_Insumo"),
        nullable=False,
    )

    ID_Receta = db.Column(
        db.Integer,
        db.ForeignKey("Recetas.ID_Receta"),
        nullable=False,
    )

    cantidad_usada = db.Column(db.Numeric(18, 3), nullable=False)

    precio_final = db.Column(db.Numeric(18, 2), nullable=False)

    ID_Unidad = db.Column(
        db.Integer,
        db.ForeignKey("Unidades_medida.ID_Unidad"),
        nullable=False,
    )

    insumo = db.relationship("Insumo", lazy="joined")
    unidad = db.relationship("Unidades_medida", lazy="joined")
    receta = db.relationship("Receta", lazy="joined")
