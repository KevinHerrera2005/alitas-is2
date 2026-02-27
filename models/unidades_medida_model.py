from models import db

class Unidades_medida(db.Model):
    __tablename__ = 'Unidades_medida'

    ID_Unidad = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    abreviatura = db.Column(db.String(10), nullable=True)
    Tipo = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"{self.Nombre}"
