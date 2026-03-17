from models import db


class EstadoPantallaEmpleado(db.Model):
    __tablename__ = "Estado_Pantalla_Empleado"
    __table_args__ = {"implicit_returning": False}

    ID_Estado = db.Column(db.Integer, primary_key=True)
    ID_Empleado = db.Column(db.Integer, db.ForeignKey("Empleado.ID_Empleado"), nullable=False)
    ID_Pantalla = db.Column(db.Integer, db.ForeignKey("Pantallas.ID_Pantalla"), nullable=False)
    activa = db.Column(db.Integer, nullable=False, default=1)

    empleado = db.relationship("Empleado", backref="estados_pantalla", lazy=True)
    pantalla = db.relationship("Pantallas", backref="estados_empleado", lazy=True)
