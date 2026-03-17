from models import db
from sqlalchemy.orm import relationship
class Pantallas(db.Model):
    __tablename__ = "Pantallas"

    ID_Pantalla = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Integer, nullable=False, default=1)
    url = db.Column(db.String(150), nullable=False)
    def __repr__(self):
        return f"{self.Nombre}"