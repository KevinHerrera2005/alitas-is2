from models import db


class Proveedor(db.Model):
    __tablename__ = "Proveedores"
    __table_args__ = {"implicit_returning": False}

    ID_Proveedor = db.Column(db.Integer, primary_key=True)
    Telefono = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Integer, nullable=False, default=1)
    Nombre_Proveedor = db.Column(db.String(50), nullable=False)

    insumos_rel = db.relationship(
        "ProveedorInsumo",
        backref="proveedor",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return (self.Nombre_Proveedor or "").strip() or "Proveedor"

    def __repr__(self):
        return self.__str__()


class ProveedorInsumo(db.Model):
    __tablename__ = "Proveedor_Insumo"
    __table_args__ = {"implicit_returning": False}

    ID_Proveedor_Insumo = db.Column(db.Integer, primary_key=True)
    ID_Proveedor = db.Column(
        db.Integer,
        db.ForeignKey("Proveedores.ID_Proveedor"),
        nullable=False,
    )
    ID_Insumo = db.Column(
        db.Integer,
        db.ForeignKey("Insumos.ID_Insumo"),
        nullable=False,
    )
    Activo = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<ProveedorInsumo {self.ID_Proveedor_Insumo}>"
