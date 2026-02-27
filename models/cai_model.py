from models import db


class CAI(db.Model):
    __tablename__ = "CAI"
    __table_args__ = {"implicit_returning": False}

    ID_Cai = db.Column(db.Integer, primary_key=True)
    num_cai = db.Column(db.String(37), nullable=True)
    Fecha_Emision = db.Column(db.Date, nullable=False)
    Fecha_Final = db.Column(db.Date, nullable=False)
    Rango_Inicial = db.Column(db.Integer, nullable=False)
    Rango_Final = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.SmallInteger, nullable=False, default=1)
    ID_sucursal = db.Column(db.Integer, nullable=False)
    Secuencia = db.Column(db.Integer, nullable=False)
