from models import db


class FacturaDetalle(db.Model):
    __tablename__ = "Factura_Detalle"

    ID_Detalle = db.Column(db.Integer, primary_key=True)
    ID_Parametro = db.Column(
        db.Integer,
        db.ForeignKey("Facturas.ID_Parametro"),
        nullable=False,
    )
    ID_IN_RE = db.Column(
        db.Integer,
        db.ForeignKey("IN_RE.ID_IN_RE"),
        nullable=False,
    )
    Descripcion = db.Column(db.String(100), nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False)
    Precio_unitario = db.Column(db.Numeric(18, 2), nullable=False)
    Subtotal_linea = db.Column(db.Numeric(18, 2), nullable=False)
    Impuesto_linea = db.Column(db.Numeric(18, 2), nullable=False)
