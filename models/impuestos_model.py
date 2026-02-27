from models import db
from models.categoria_insumo_model import CategoriaInsumo

FK_CATEGORIA = f"{CategoriaInsumo.__tablename__}.ID_Categoria"


class Impuesto(db.Model):
    __tablename__ = "Impuestos"
    __table_args__ = {"implicit_returning": False}
    ID_Impuesto = db.Column(db.Integer, primary_key=True)
    Nombre_Impuesto = db.Column(db.String(50), nullable=False)
    tasa = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.String(50), nullable=False)
    ID_Categoria = db.Column(
        db.Integer,
        db.ForeignKey(FK_CATEGORIA),
        nullable=False,
    )
    activo = db.Column(db.SmallInteger, nullable=False, default=1)

    categorias_rel = db.relationship(
        "ImpuestoCategoria",
        backref="impuesto",
        lazy=True,
    )


class ImpuestoCategoria(db.Model):
    __tablename__ = "Impuesto_Categoria"

    ID_Impuesto_Categoria = db.Column(db.Integer, primary_key=True)
    ID_Impuesto = db.Column(
        db.Integer,
        db.ForeignKey("Impuestos.ID_Impuesto"),
        nullable=False,
    )
    ID_Categoria = db.Column(
        db.Integer,
        db.ForeignKey(FK_CATEGORIA),
        nullable=False,
    )
    Activo = db.Column(db.SmallInteger, nullable=False, default=1)

    categoria = db.relationship(
        "CategoriaInsumo",
        primaryjoin="ImpuestoCategoria.ID_Categoria == CategoriaInsumo.ID_Categoria",
        lazy=True,
    )
