from models import db


class PagoDetalle(db.Model):
    __tablename__ = "pago_detalle"

    ID_pago = db.Column(db.Integer, primary_key=True)
    ID_Metodo = db.Column(
        db.Integer,
        db.ForeignKey("Metodos_money.ID_Metodo"),
        nullable=False,
        index=True,
    )
    Efectivo = db.Column(db.Numeric(18, 2), nullable=True)
    Numero_tarjeta = db.Column(db.String(4), nullable=True)

    metodo = db.relationship("MetodosMoney", lazy="joined")

    def __repr__(self):
        return f"<PagoDetalle {self.ID_pago}>"
