from models import db


class OrdenEntrega(db.Model):
    __tablename__ = "Orden_Entrega"

    ID_Orden_Entrega = db.Column(db.Integer, primary_key=True)

    ID_Parametro = db.Column(
        db.Integer,
        db.ForeignKey("Facturas.ID_Parametro"),
        nullable=False,
    )

    ID_Usuario_ClienteF = db.Column(
        db.Integer,
        db.ForeignKey("Usuarios_cliente.ID_Usuario_ClienteF"),
        nullable=False,
    )

    ID_US_CO = db.Column(
        db.Integer,
        db.ForeignKey("Direccion_del_cliente.ID_US_CO"),
        nullable=False,
    )

    ID_Direccion = db.Column(
        db.Integer,
        db.ForeignKey("Direcciones.ID_Direccion"),
        nullable=False,
    )

    ID_sucursal = db.Column(
        db.Integer,
        db.ForeignKey("Sucursales.ID_sucursal"),
        nullable=False,
    )

    ID_Empleado_Repartidor = db.Column(
        db.Integer,
        db.ForeignKey("Empleado.ID_Empleado"),
        nullable=False,
    )

    Numero_Factura = db.Column(
        db.String(19),
        nullable=False,
    )

    nombre = db.Column(
        db.String(50),
        nullable=False,
    )

    apellido = db.Column(
        db.String(50),
        nullable=False,
    )

    descripcion = db.Column(
        db.String(255),
        nullable=False,
    )

    telefono = db.Column(
        db.String(50),
        nullable=False,
    )

    estado = db.Column(db.SmallInteger, nullable=False, default=0)
    Motivo_Cancelacion = db.Column(db.String(255), nullable=True)

    Fecha_Creacion = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    factura = db.relationship(
        "Factura",
        primaryjoin="OrdenEntrega.ID_Parametro == Factura.ID_Parametro",
        lazy=True,
    )

    cliente = db.relationship(
        "UsuarioCliente",
        primaryjoin="OrdenEntrega.ID_Usuario_ClienteF == UsuarioCliente.ID_Usuario_ClienteF",
        lazy=True,
    )

    direccion_cliente = db.relationship(
        "DireccionDelCliente",
        primaryjoin="OrdenEntrega.ID_US_CO == DireccionDelCliente.ID_US_CO",
        lazy=True,
    )

    direccion = db.relationship(
        "Direccion",
        primaryjoin="OrdenEntrega.ID_Direccion == Direccion.ID_Direccion",
        lazy=True,
    )

    repartidor = db.relationship(
        "Empleado",
        primaryjoin="OrdenEntrega.ID_Empleado_Repartidor == Empleado.ID_Empleado",
        lazy=True,
    )

    sucursal_rel = db.relationship(
        "Sucursal",
        primaryjoin="OrdenEntrega.ID_sucursal == Sucursal.ID_sucursal",
        lazy=True,
    )

    def __repr__(self):
        return f"<OrdenEntrega {self.ID_Orden_Entrega}>"
