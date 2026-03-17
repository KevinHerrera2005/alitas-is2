from models import db

class PantallasAcciones(db.Model):
    __tablename__ = "Pantallas_Acciones"

    ID_Pantalla_Accion = db.Column(db.Integer, primary_key=True)
    ID_Accion = db.Column(db.Integer, db.ForeignKey("Acciones.ID_Accion"), nullable=False)
    ID_Pantalla = db.Column(db.Integer, db.ForeignKey("Pantallas.ID_Pantalla"), nullable=False)
    estado = db.Column(db.Integer, default=1, nullable=False)

    accion = db.relationship("Acciones", backref="pantallas_acciones", lazy=True)
    pantalla = db.relationship("Pantallas", backref="pantallas_acciones", lazy=True)

    def __repr__(self):
        return f"{self.ID_Pantalla_Accion}"