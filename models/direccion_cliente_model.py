from models import db


class DireccionDelCliente(db.Model):
    __tablename__ = "Direccion_del_cliente"

    ID_US_CO = db.Column(db.Integer, primary_key=True)
    ID_Usuario_ClienteF = db.Column(db.Integer, nullable=False)
    ID_Direccion = db.Column(db.Integer, nullable=False)
