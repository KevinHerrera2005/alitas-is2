from models import db


class ParametroSAR(db.Model):
    __tablename__ = "Parametros_SAR"
    __table_args__ = {"implicit_returning": False}

    ID_Parametro = db.Column(db.Integer, primary_key=True)
    Parametro = db.Column(db.String(50), nullable=False, unique=True)
    Valor = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<ParametroSAR {self.ID_Parametro} - {self.Parametro}={self.Valor}>"
