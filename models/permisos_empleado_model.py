from models import db

class PermisosEmpleado(db.Model):
    __tablename__ = "Permisos_Empleado"

    ID_Permiso_Empleado = db.Column(db.Integer, primary_key=True)
    ID_Empleado = db.Column(
        db.Integer,
        db.ForeignKey("Empleado.ID_Empleado"),
        nullable=False
    )
    ID_Permiso_Puesto = db.Column(
        db.Integer,
        db.ForeignKey("Permisos_Puesto.ID_Permiso_Puesto"),
        nullable=False
    )
    estado = db.Column(db.Integer, nullable=False, default=1)

    empleado = db.relationship("Empleado", backref="permisos_empleado", lazy=True)
    permiso_puesto = db.relationship("PermisosPuesto", backref="permisos_empleado", lazy=True)

    def __repr__(self):
        return f"{self.ID_Permiso_Empleado}"