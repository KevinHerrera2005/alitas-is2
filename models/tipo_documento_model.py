from models import db

class TipoDocumento(db.Model):
    __tablename__ = "Tipo_documentos"

    tipo_doc = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.SmallInteger, nullable=False)          # 1=dni, 2=rtn, 3=pasaporte, 4=otro
    numero_documento = db.Column(db.String(20), nullable=False)  
