from models import db


class Sucursal(db.Model):
    __tablename__ = "Sucursales"
    __table_args__ = {"implicit_returning": False}

    ID_sucursal = db.Column(db.Integer, primary_key=True)
    Descripcion = db.Column(db.String(255), nullable=False)

    ID_Direccion = db.Column(
        db.Integer,
        db.ForeignKey("Direcciones.ID_Direccion"),
        nullable=False,
    )

    estado = db.Column(db.SmallInteger, nullable=False, default=1)

    direccion = db.relationship("Direccion", lazy="joined")

    def __str__(self):
        return (self.Descripcion or "").strip() or "Sucursal"

    def __repr__(self):
        return self.__str__()
