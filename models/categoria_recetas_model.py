from models import db

class Categoria_recetas(db.Model):
    __tablename__ = 'Categoria_recetas'

    id_categoria_receta = db.Column(db.Integer, primary_key=True)
    Nombre_categoria_receta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(400), nullable=True)
