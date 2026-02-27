# models/metodos_money_model.py
from models import db


class MetodosMoney(db.Model):
    __tablename__ = "Metodos_money"

    ID_Metodo = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Tipo = db.Column(db.SmallInteger, nullable=False)  # 1=Efectivo, 2=Tarjeta, 3=Mixto
    Descripcion = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f"<MetodosMoney {self.ID_Metodo} {self.Nombre} (Tipo={self.Tipo})>"
