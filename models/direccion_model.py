# models/direccion_model.py

from models import db

class Direccion(db.Model):
    __tablename__ = "Direcciones"   

    ID_Direccion = db.Column(db.Integer, primary_key=True)
    Descripcion  = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return f"<Direccion {self.ID_Direccion} - {self.Descripcion}>"
