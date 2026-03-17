from models import db

class Acciones(db.Model):
    __tablename__="Acciones"
    
    ID_Accion = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Integer, nullable= False)
    
    def __repr__(self):
        return f"{self.Nombre}"