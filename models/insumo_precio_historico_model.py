from models import db
from sqlalchemy.ext.hybrid import hybrid_property


class InsumoPrecioHistorico(db.Model):
    __tablename__ = "Insumo_Precio_historico"

    ID_Insumo_precio_historico = db.Column(db.Integer, primary_key=True)
    ID_Insumo = db.Column(db.Integer, db.ForeignKey("Insumos.ID_Insumo"), nullable=False)

    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)   
    Precio = db.Column(db.Numeric(18, 2), nullable=False)

    insumo = db.relationship("Insumo", lazy="joined")

    @hybrid_property
    def nombre_insumo(self):
        return self.insumo.Nombre_insumo if self.insumo else None
