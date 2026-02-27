from models import db

class InRe(db.Model):
    __tablename__ = 'IN_RE'
    __table_args__ = {'extend_existing': True}

    ID_IN_RE = db.Column(db.Integer, primary_key=True)
    ID_Insumo = db.Column(db.Integer, nullable=False)
    ID_Receta = db.Column(db.Integer, nullable=False)
    cantidad_usada = db.Column(db.Float, nullable=False)
    ID_Unidad = db.Column(db.Integer, nullable=True)
    precio_final = db.Column(db.Float, nullable=True)
    Activo = db.Column(db.SmallInteger, nullable=False)
