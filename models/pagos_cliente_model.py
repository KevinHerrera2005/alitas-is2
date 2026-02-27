from models import db


class PagosCliente(db.Model):
    __tablename__ = "Pagos_cliente"

    ID_Pago = db.Column(db.Integer, primary_key=True)

    ID_Usuario_ClienteF = db.Column(
        db.Integer,
        db.ForeignKey("Usuarios_cliente.ID_Usuario_ClienteF"),
        nullable=False,
    )

    ID_Metodo = db.Column(
        db.Integer,
        db.ForeignKey("Metodos_money.ID_Metodo"),
        nullable=False,
    )

    Cantidad = db.Column(db.Numeric(10, 2), nullable=True)  # para mixto/efectivo
    Numero_tarjeta = db.Column(db.String(4), nullable=True)  
    a_nombre_de = db.Column(db.String(50), nullable=True)

    cliente = db.relationship(
        "UsuarioCliente",
        backref=db.backref("pagos_cliente", lazy=True),
    )

    metodo = db.relationship("MetodosMoney", lazy=True)

    def __repr__(self) -> str:
        return f"<PagoCliente {self.ID_Pago} cli={self.ID_Usuario_ClienteF} metodo={self.ID_Metodo}>"
