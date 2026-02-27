from models import db
from sqlalchemy import event, inspect
from models.usuario_cliente_model import UsuarioCliente


class Puesto(db.Model):
    __tablename__ = "Puesto"

    ID_Puesto = db.Column(db.Integer, primary_key=True)
    Nombre_Puesto = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Integer, nullable=False, default=1)


class Empleado(db.Model):
    __tablename__ = "Empleado"

    ID_Empleado = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Apellido = db.Column(db.String(100), nullable=False)
    Username = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Telefono = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(200), nullable=True)

    ID_Puesto = db.Column(
        db.Integer,
        db.ForeignKey("Puesto.ID_Puesto"),
        nullable=False,
    )
    puesto = db.relationship("Puesto", backref="empleados", lazy=True)

    ID_sucursal = db.Column(
        db.Integer,
        db.ForeignKey("Sucursales.ID_sucursal"),
        nullable=False,
    )
    sucursal = db.relationship("Sucursal", backref="empleados", lazy=True)

    estado = db.Column(db.Integer, nullable=False, default=1)
@event.listens_for(Empleado, "after_update")
def sincronizar_sucursal_clientes(mapper, connection, target):
    state = inspect(target)
    if target.ID_Empleado != 20:
        return
    if not state.attrs.ID_sucursal.history.has_changes():
        return
    nueva_sucursal = target.ID_sucursal
    connection.execute(
        UsuarioCliente.__table__.update().values(ID_sucursal=nueva_sucursal)
    )
