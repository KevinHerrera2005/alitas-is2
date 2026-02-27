from models import db
from sqlalchemy.dialects.mssql import TINYINT

class CategoriaInsumo(db.Model):
    __tablename__ = 'categorias'

    ID_Categoria = db.Column(db.Integer, primary_key=True)
    Nombre_categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))
    estado = db.Column(db.Integer, nullable=False, default=1)
    tipo = db.Column(TINYINT, nullable=False, default=1)

    def __repr__(self):
        return f"{self.Nombre_categoria}"
