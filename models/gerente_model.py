from models import db
from flask_login import UserMixin   

class Gerente(db.Model, UserMixin):
    __tablename__ = 'Gerentes'

    ID_gerente = db.Column(db.Integer, primary_key=True)
    Username   = db.Column(db.String(50), nullable=False)
    Password   = db.Column(db.String(50), nullable=False)

    ID_sucursal = db.Column(
        db.Integer,
        db.ForeignKey('Sucursales.ID_sucursal'),
        nullable=False
    )

    ID_Puesto = db.Column(
        db.Integer,
        db.ForeignKey('Puesto.ID_Puesto'),
        nullable=True
    )

    def get_id(self):
        return str(self.ID_gerente)

    @property
    def tipo(self):
        return "gerente"
