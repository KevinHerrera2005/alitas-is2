from datetime import datetime

from models import db
from models.cai_model import CAI


class CAIHistorico(db.Model):
    __tablename__ = "CAI_Historico"

    ID_Cai_Historico = db.Column(db.Integer, primary_key=True)
    ID_Cai = db.Column(db.Integer, db.ForeignKey("CAI.ID_Cai"), nullable=False)

    Fecha_Registro = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    Fecha_Emision = db.Column(db.Date, nullable=False)
    Fecha_Final = db.Column(db.Date, nullable=False)
    Rango_Inicial = db.Column(db.Integer, nullable=False)
    Rango_Final = db.Column(db.Integer, nullable=False)
    Secuencia = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.SmallInteger, nullable=False)
    ID_sucursal = db.Column(db.Integer, nullable=False)

    cai = db.relationship(CAI, backref="historicos")

    def __repr__(self):
        return f"<CAIHistorico CAI={self.ID_Cai} sec={self.Secuencia}>"



def registrar_cai_historico(cai_obj: CAI, session=None):
    """
    Helper general:
    Llama esto cada vez que cambies la Secuencia de un CAI
    (por admin o por impresión de facturas).
    """
    if session is None:
        session = db.session

    hist = CAIHistorico(
        ID_Cai=cai_obj.ID_Cai,
        Fecha_Emision=cai_obj.Fecha_Emision,
        Fecha_Final=cai_obj.Fecha_Final,
        Rango_Inicial=cai_obj.Rango_Inicial,
        Rango_Final=cai_obj.Rango_Final,
        Secuencia=cai_obj.Secuencia,
        estado=cai_obj.estado,
        ID_sucursal=cai_obj.ID_sucursal,
    )
    session.add(hist)
