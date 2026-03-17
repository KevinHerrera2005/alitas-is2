from models import db

class PermisosPuesto(db.Model):
    __tablename__ = "Permisos_Puesto"
    __table_args__ = {"implicit_returning": False}

    ID_Permiso_Puesto = db.Column(db.Integer, primary_key=True)
    ID_Puesto = db.Column(
        db.Integer,
        db.ForeignKey("Puesto.ID_Puesto"),
        nullable=False
    )
    ID_Pantalla_Accion = db.Column(
        db.Integer,
        db.ForeignKey("Pantallas_Acciones.ID_Pantalla_Accion"),
        nullable=False
    )
    estado = db.Column(db.Integer, nullable=False, default=1)

    puesto = db.relationship("Puesto", backref="permisos_puesto", lazy=True)
    pantalla_accion = db.relationship("PantallasAcciones", backref="permisos_puesto", lazy=True)

    def __repr__(self):
        return f"{self.ID_Permiso_Puesto}"