from models import db
from models.receta_model import Receta  


class RecetaPrecioHistorico(db.Model):
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#da0707")
        return super().render(template, **kwargs)
    create_template = "admin/model/impuesto_create.html"
    edit_template = "admin/model/impuesto_edit.html"
    __tablename__ = "recetas_precio_historico"

    ID_Receta_precio_historico = db.Column(db.Integer, primary_key=True)

    ID_Receta = db.Column(
        db.Integer,
        db.ForeignKey("Recetas.ID_Receta"),
        nullable=False
    )

    Costo = db.Column(db.Numeric(10, 2), nullable=False)
    Fecha_inicio = db.Column(db.Date, nullable=False)
    Fecha_Fin = db.Column(db.Date, nullable=True)

    receta = db.relationship(
        Receta,
        backref="historial_precios",
        lazy="joined",
    )

    @property
    def nombre_receta(self):
        """
        Devuelve el nombre de la receta asociada a este registro histórico.
        Se usa en el admin para mostrar la columna 'Receta'.
        """
        if self.receta is not None:
            return self.receta.Nombre_receta
        return "-"
