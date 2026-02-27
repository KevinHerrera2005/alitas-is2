from models import db


class EmpleadoDocumento(db.Model):
    __tablename__ = "Empleado_documento"

    ID_empleado_documento = db.Column(db.Integer, primary_key=True)

    tipo_doc = db.Column(
        db.Integer,
        db.ForeignKey("Tipo_documentos.tipo_doc"),
        nullable=False,
    )

    ID_Empleado = db.Column(
        db.Integer,
        db.ForeignKey("Empleado.ID_Empleado"),
        nullable=False,
    )

    empleado = db.relationship(
        "Empleado",
        backref="documentos",
        lazy=True,
    )
