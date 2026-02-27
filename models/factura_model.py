from models import db


class Factura(db.Model):
    __tablename__ = "Facturas"

    ID_Parametro = db.Column(db.Integer, primary_key=True)
    Numero_Factura = db.Column(db.String(19), nullable=True)
    Fecha_Emision = db.Column(db.DateTime, nullable=False)

    ID_Empleado = db.Column(db.Integer, nullable=False)
    ID_Cai = db.Column(db.Integer, nullable=False)

    ID_Usuario_ClienteF = db.Column(
        db.Integer,
        db.ForeignKey("Usuarios_cliente.ID_Usuario_ClienteF"),
        nullable=False,
        index=True,
    )

    ID_pago = db.Column(
        db.Integer,
        db.ForeignKey("pago_detalle.ID_pago"),
        nullable=False,
        index=True,
    )

    Subtotal = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    Descuento = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    Impuesto = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    Total_a_pagar = db.Column(db.Numeric(18, 2), nullable=False, default=0)

    cliente = db.relationship(
        "UsuarioCliente",
        backref=db.backref("facturas", lazy="select"),
        lazy="joined",
        foreign_keys=[ID_Usuario_ClienteF],
    )

    pago_detalle = db.relationship(
        "PagoDetalle",
        lazy="joined",
        foreign_keys=[ID_pago],
    )

    detalles = db.relationship(
        "FacturaDetalle",
        backref="factura",
        lazy="select",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Factura {self.Numero_Factura}>"


from models.pago_detalle_model import PagoDetalle  # noqa: F401
from models.factura_detalle_model import FacturaDetalle  # noqa: F401
