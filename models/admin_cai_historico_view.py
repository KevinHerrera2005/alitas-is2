from flask_admin.contrib.sqla import ModelView
from models.cai_historico_model import CAIHistorico
from models.sucursal_model import Sucursal


class CAIHistoricoAdmin(ModelView):
    
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_default_sort = ("Fecha_Registro", True)

    column_list = (
        "Fecha_Registro",
        "ID_Cai",
        "Fecha_Emision",
        "Fecha_Final",
        "Rango_Inicial",
        "Rango_Final",
        "Secuencia",
        "estado",
        "ID_sucursal",
    )

    column_labels = {
        "Fecha_Registro": "Fecha de registro",
        "ID_Cai": "ID CAI",
        "Fecha_Emision": "Fecha de emisión",
        "Fecha_Final": "Fecha final",
        "Rango_Inicial": "Rango inicial",
        "Rango_Final": "Rango final",
        "Secuencia": "Secuencia",
        "estado": "Estado",
        "ID_sucursal": "Sucursal",
    }

    column_formatters = {
        "Fecha_Registro": lambda v, c, m, p: (
            m.Fecha_Registro.strftime("%Y-%m-%d") if m.Fecha_Registro else ""
        ),
        "estado": lambda v, c, m, p: "Activo" if m.estado == 1 else "Inactivo",
        "ID_sucursal": lambda v, c, m, p: (
            (Sucursal.query.get(m.ID_sucursal).Descripcion)
            if Sucursal.query.get(m.ID_sucursal)
            else m.ID_sucursal
        ),
    }
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)