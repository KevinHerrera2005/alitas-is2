from models import db


class ImpuestoTasaHistorica(db.Model):
    

    __tablename__ = "Impuesto_tasa_historica"

    ID_Impuesto_historico = db.Column(db.Integer, primary_key=True)
    ID_Impuesto = db.Column(
        db.Integer,
        db.ForeignKey("Impuestos.ID_Impuesto"),
        nullable=False,
    )
    fecha_inicio = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.getdate(),
    )
    fecha_fin = db.Column(db.DateTime, nullable=True)
    tasa = db.Column(db.Numeric(10, 2), nullable=False)

    impuesto = db.relationship("Impuesto", backref="tasas_historicas", lazy=True)

    @property
    def nombre_impuesto(self):
        if self.impuesto:
            return self.impuesto.Nombre_Impuesto
        return None
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#000000")
        return super().render(template, **kwargs)