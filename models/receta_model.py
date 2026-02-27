from models import db


class Receta(db.Model):
    __tablename__ = "Recetas"

    ID_Receta = db.Column(db.Integer, primary_key=True)
    ID_Jefe_de_cocina = db.Column(db.Integer, nullable=False)
    ID_sucursal = db.Column(db.Integer, db.ForeignKey("Sucursales.ID_sucursal"), nullable=False)

    Nombre_receta = db.Column(db.String(50), nullable=False)
    Estado = db.Column(db.Integer, nullable=False, default=1)
    descripcion = db.Column(db.String(200))
    categoria = db.Column(db.Integer)
    descripcion_cliente = db.Column(db.String(500), nullable=True)

    sucursal = db.relationship("Sucursal", lazy="joined")
