from datetime import datetime
from models import db


class HistorialOrdenesRepartidor(db.Model):
    __tablename__ = "historial_ordenes_repartidor"

    ID_Historial = db.Column(db.Integer, primary_key=True)
    ID_Orden = db.Column(db.Integer, nullable=False, unique=True)
    ID_Repartidor = db.Column(
        db.Integer,
        db.ForeignKey("Empleado.ID_Empleado"),
        nullable=False,
    )
    Estado_Final = db.Column(db.SmallInteger, nullable=False)
    Fecha_Finalizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Observacion = db.Column(db.String(300), nullable=True)

    repartidor = db.relationship("Empleado", lazy="joined")

    def __repr__(self):
        return f"<HistorialOrdenesRepartidor {self.ID_Historial}>"
