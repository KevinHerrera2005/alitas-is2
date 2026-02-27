from . import db


class MetodoPago(db.Model):
    __tablename__ = "Metodo_de_pago"
    __table_args__ = {"extend_existing": True}

    ID_Metodo_de_pago = db.Column(db.Integer, primary_key=True)
    Tipo = db.Column(db.SmallInteger, nullable=False)
    Numero_Tarjeta = db.Column(db.String(255))
    Codigo_seguridad = db.Column(db.String(255))
    Fecha_vencimiento = db.Column(db.String(7))
    ID_Usuario_ClienteF = db.Column(
        db.Integer,
        db.ForeignKey("Usuarios_cliente.ID_Usuario_ClienteF"),
        nullable=False,
    )
