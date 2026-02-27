from models import db
from models.in_re_model import IN_RE


class Carrito(db.Model):
    __tablename__ = "Carrito"

    ID_Carrito = db.Column(db.Integer, primary_key=True)
    ID_Usuario_ClienteF = db.Column(
        db.Integer,
        db.ForeignKey("Usuarios_cliente.ID_Usuario_ClienteF"),
        nullable=False,
    )
    ID_IN_RE = db.Column(
        db.Integer,
        db.ForeignKey("IN_RE.ID_IN_RE"),
        nullable=False,
    )
    Cantidad = db.Column(db.Integer, nullable=False, default=1)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    in_re = db.relationship(
        "IN_RE",
        primaryjoin="Carrito.ID_IN_RE == IN_RE.ID_IN_RE",
        lazy=True,
    )
