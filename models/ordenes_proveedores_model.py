from datetime import datetime
from models import db


class OrdenesProveedores(db.Model):
    __tablename__ = "Ordenes_Proveedores"

    ID_Orden_Proveedor = db.Column(db.Integer, primary_key=True)

    ID_Proveedor = db.Column(
        db.Integer,
        db.ForeignKey("Proveedores.ID_Proveedor"),
        nullable=False,
    )
    ID_Empleado_Encargado = db.Column(
        db.Integer,
        db.ForeignKey("Empleado.ID_Empleado"),
        nullable=False,
    )
    ID_Sucursal = db.Column(
        db.Integer,
        db.ForeignKey("Sucursales.ID_sucursal"),
        nullable=False,
    )

    Fecha_Inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Fecha_Estimada = db.Column(db.DateTime, nullable=True)
    Fecha_Entregado = db.Column(db.DateTime, nullable=True)

    Estado = db.Column(db.SmallInteger, nullable=False, default=0)

    Numero_Factura = db.Column(db.String(14), nullable=True)

    Comentarios = db.Column(db.String(255), nullable=True)

    proveedor = db.relationship("Proveedor", lazy="joined")
    empleado = db.relationship(
        "Empleado",
        lazy="joined",
        foreign_keys=[ID_Empleado_Encargado],
    )
    sucursal = db.relationship("Sucursal", lazy="joined")

    detalles = db.relationship(
        "OrdenesProveedoresDetalle",
        back_populates="orden",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<OrdenesProveedores {self.ID_Orden_Proveedor}>"


class OrdenesProveedoresDetalle(db.Model):
    __tablename__ = "Ordenes_Proveedores_Detalle"

    ID_Detalle = db.Column(db.Integer, primary_key=True)

    ID_Orden_Proveedor = db.Column(
        db.Integer,
        db.ForeignKey("Ordenes_Proveedores.ID_Orden_Proveedor"),
        nullable=False,
    )
    ID_Insumo = db.Column(
        db.Integer,
        db.ForeignKey("Insumos.ID_Insumo"),
        nullable=False,
    )

    ID_Unidad = db.Column(
        db.Integer,
        db.ForeignKey("Unidades_medida.ID_Unidad"),
        nullable=False,
    )

    ID_Unidad_Recibida = db.Column(
        db.Integer,
        db.ForeignKey("Unidades_medida.ID_Unidad"),
        nullable=True,
    )

    Cantidad_Solicitada = db.Column(db.Float, nullable=False)
    Cantidad_Recibida = db.Column(db.Float, nullable=True)

    orden = db.relationship("OrdenesProveedores", back_populates="detalles")
    insumo = db.relationship("Insumo", lazy="joined")
    unidad = db.relationship("Unidades_medida", lazy="joined", foreign_keys=[ID_Unidad])
    unidad_recibida = db.relationship(
        "Unidades_medida", lazy="joined", foreign_keys=[ID_Unidad_Recibida]
    )

    def __repr__(self):
        return f"<OrdenesProveedoresDetalle {self.ID_Detalle}>"
