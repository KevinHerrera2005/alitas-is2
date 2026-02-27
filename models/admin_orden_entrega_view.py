from datetime import datetime

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import request
from wtforms import SelectField, TextAreaField
from wtforms.validators import ValidationError
from sqlalchemy import inspect as sa_inspect

from models import db
from models.orden_entrega_model import OrdenEntrega
from models.historial_ordenes_repartidor_model import HistorialOrdenesRepartidor
from models.empleado_model import Empleado
from models.usuario_cliente_model import UsuarioCliente


class OrdenEntregaAdmin(ModelView):
    can_create = False
    can_delete = False
    can_view_details = True

    can_search = True
    column_searchable_list = ("nombre", "apellido", "Numero_Factura")

    create_template = "admin/model/orden_entrega_create.html"
    edit_template = "admin/model/orden_entrega_edit.html"

    column_default_sort = ("ID_Orden_Entrega", True)

    column_list = (
        "Numero_Factura",
        "nombre",
        "apellido",
        "descripcion",
        "telefono",
        "estado",
        "Motivo_Cancelacion",
        "Fecha_Creacion",
    )

    column_details_list = (
        "ID_Orden_Entrega",
        "Numero_Factura",
        "nombre",
        "apellido",
        "descripcion",
        "telefono",
        "estado",
        "Motivo_Cancelacion",
        "Fecha_Creacion",
    )

    column_labels = {
        "ID_Orden_Entrega": "ID Orden",
        "Numero_Factura": "Número factura",
        "nombre": "Nombre cliente",
        "apellido": "Apellido cliente",
        "descripcion": "Descripción",
        "telefono": "Teléfono",
        "estado": "Estado",
        "Motivo_Cancelacion": "Motivo de cancelación",
        "Fecha_Creacion": "Fecha de creación",
    }

    form_columns = ("estado", "Motivo_Cancelacion")

    form_overrides = {
        "estado": SelectField,
        "Motivo_Cancelacion": TextAreaField,
    }

    form_widget_args = {
        "Motivo_Cancelacion": {"rows": 3},
    }
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#000000")
        return super().render(template, **kwargs)

    def _estado_map(self):
        return {
            0: "En preparación",
            1: "Listo para recoger",
            2: "Recogido",
            3: "Entregado",
            4: "Cancelado",
        }

    def _estado_label(self, model):
        try:
            valor = int(model.estado)
        except Exception:
            return str(model.estado)
        return self._estado_map().get(valor, str(valor))

    column_formatters = {
        "estado": lambda view, context, model, name: view._estado_label(model),
    }

    def _es_repartidor(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "tipo", None) == "empleado"
            and getattr(current_user, "id_puesto", None) == 4
        )

    def _empleado_id(self):
        if not current_user.is_authenticated:
            return None
        for attr in ("ID_Empleado", "id_empleado", "db_id", "id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass
        return None

    def _empleado_sucursal(self):
        if not current_user.is_authenticated:
            return None

        for attr in ("ID_sucursal", "id_sucursal", "sucursal_id"):
            v = getattr(current_user, attr, None)
            if v is not None:
                try:
                    return int(v)
                except Exception:
                    pass

        emp_id = self._empleado_id()
        if emp_id is None:
            return None

        emp = Empleado.query.get(emp_id)
        if not emp:
            return None

        v = getattr(emp, "ID_sucursal", None) or getattr(emp, "id_sucursal", None)
        try:
            return int(v)
        except Exception:
            return None

    def _cargar_choices_estado(self, form, obj=None):
        if not hasattr(form, "estado"):
            return

        mapa = self._estado_map()

        valor_actual = 0
        if obj is not None:
            try:
                valor_actual = int(obj.estado or 0)
            except Exception:
                valor_actual = 0

        es_repartidor = self._es_repartidor()

        choices = [(str(valor_actual), mapa.get(valor_actual, str(valor_actual)))]

        if valor_actual in (3, 4):
            form.estado.choices = choices
            return

        choices.append(("4", mapa.get(4, "Cancelado")))

        if not es_repartidor and valor_actual == 0:
            choices.append(("1", mapa.get(1, "Listo para recoger")))

        if es_repartidor and valor_actual in (1, 2):
            siguiente = valor_actual + 1
            choices.append((str(siguiente), mapa.get(siguiente, str(siguiente))))

        final = []
        seen = set()
        for v, lbl in choices:
            if v not in seen:
                final.append((v, lbl))
                seen.add(v)

        form.estado.choices = final

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._cargar_choices_estado(form, obj=obj)
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._cargar_choices_estado(form, obj=obj)

        if request.method == "GET" and obj is not None and hasattr(form, "estado"):
            try:
                form.estado.data = str(int(obj.estado or 0))
            except Exception:
                form.estado.data = "0"

        return form

    def _filtrar_por_sucursal_cliente(self, query):
        if not current_user.is_authenticated:
            return query.filter(False)

        tipo = getattr(current_user, "tipo", None)
        if tipo != "empleado":
            return query

        suc_emp = self._empleado_sucursal()
        if not suc_emp:
            return query.filter(False)

        return query.join(
            UsuarioCliente,
            UsuarioCliente.ID_Usuario_ClienteF == OrdenEntrega.ID_Usuario_ClienteF,
        ).filter(UsuarioCliente.ID_sucursal == int(suc_emp))

    def _filtrar_lista(self, query):
        query = self._filtrar_por_sucursal_cliente(query)
        estados_activos = [0, 1, 2]

        if getattr(current_user, "tipo", None) == "empleado" and self._es_repartidor():
            emp_id = self._empleado_id()
            if emp_id is None:
                return query.filter(False)
            return query.filter(
                OrdenEntrega.ID_Empleado_Repartidor == int(emp_id),
                OrdenEntrega.estado.in_(estados_activos),
            )

        return query.filter(OrdenEntrega.estado.in_(estados_activos))

    def get_query(self):
        return self._filtrar_lista(super().get_query())

    def get_count_query(self):
        return self._filtrar_lista(super().get_count_query())

    def get_one(self, id):
        try:
            oid = int(id)
        except Exception:
            return None
        return self.get_query().filter(OrdenEntrega.ID_Orden_Entrega == oid).first()

    def _obtener_estado_anterior(self, model, is_created):
        if is_created:
            return 0
        try:
            hist = sa_inspect(model).attrs.estado.history
            if hist.deleted:
                return int(hist.deleted[0])
            if hist.unchanged:
                return int(hist.unchanged[0])
            return int(model.estado or 0)
        except Exception:
            try:
                return int(model.estado or 0)
            except Exception:
                return 0

    def _guardar_historial_si_aplica(self, model, estado_anterior, estado_nuevo, motivo):
        if estado_nuevo not in (3, 4):
            return
        if estado_anterior in (3, 4):
            return

        orden_id = getattr(model, "ID_Orden_Entrega", None)
        repartidor_id = getattr(model, "ID_Empleado_Repartidor", None)

        if not orden_id:
            raise ValidationError("No se pudo determinar el ID de la orden para guardar en historial.")
        if not repartidor_id:
            raise ValidationError("No se pudo determinar el repartidor de la orden para guardar en historial.")

        existente = HistorialOrdenesRepartidor.query.filter_by(ID_Orden=int(orden_id)).first()
        if existente:
            existente.Estado_Final = int(estado_nuevo)
            existente.Fecha_Finalizacion = datetime.utcnow()
            existente.Observacion = motivo if estado_nuevo == 4 else None
            db.session.add(existente)
            return

        db.session.add(
            HistorialOrdenesRepartidor(
                ID_Orden=int(orden_id),
                ID_Repartidor=int(repartidor_id),
                Estado_Final=int(estado_nuevo),
                Fecha_Finalizacion=datetime.utcnow(),
                Observacion=motivo if estado_nuevo == 4 else None,
            )
        )

    def on_model_change(self, form, model, is_created):
        if not hasattr(form, "estado"):
            return

        try:
            nuevo_estado = int(form.estado.data)
        except Exception:
            raise ValidationError("Estado inválido.")

        anterior_estado = self._obtener_estado_anterior(model, is_created)

        motivo = ""
        if hasattr(form, "Motivo_Cancelacion"):
            motivo = (form.Motivo_Cancelacion.data or "").strip()

        es_repartidor = self._es_repartidor()

        if not is_created and anterior_estado in (3, 4) and nuevo_estado != anterior_estado:
            if anterior_estado == 3:
                raise ValidationError("La orden ya fue ENTREGADA y no se puede cambiar ni cancelar.")
            raise ValidationError("Esta orden ya no puede modificarse.")

        if nuevo_estado == 4:
            if anterior_estado == 3:
                raise ValidationError("No se puede cancelar una orden entregada.")
            if not motivo:
                raise ValidationError("Debes ingresar un motivo de cancelación.")
        else:
            if motivo:
                raise ValidationError("Primero marca la orden como cancelada para guardar un motivo.")

            if nuevo_estado != anterior_estado and nuevo_estado != (anterior_estado + 1):
                raise ValidationError("No puedes saltar estados. Debes avanzar de 1 en 1.")

            if not es_repartidor:
                if anterior_estado == 0 and nuevo_estado not in (0, 1):
                    raise ValidationError("Solo puedes pasar de 'En preparación' a 'Listo para recoger'.")
                if anterior_estado != 0 and nuevo_estado != anterior_estado:
                    raise ValidationError("Este rol no puede avanzar la orden en este punto.")
            else:
                if anterior_estado == 0 and nuevo_estado != 0:
                    raise ValidationError("Aún está en preparación. Espera a 'Listo para recoger'.")
                if anterior_estado == 1 and nuevo_estado not in (1, 2):
                    raise ValidationError("Debes pasar de 'Listo para recoger' a 'Recogido'.")
                if anterior_estado == 2 and nuevo_estado not in (2, 3):
                    raise ValidationError("Debes pasar de 'Recogido' a 'Entregado'.")

        model.estado = nuevo_estado
        model.Motivo_Cancelacion = motivo if nuevo_estado == 4 else None

        self._guardar_historial_si_aplica(model, anterior_estado, nuevo_estado, motivo)

    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        return True
def validar_cambio_estado_orden(estado_actual, estado_nuevo):
    try:
        actual = int(estado_actual)
    except Exception:
        return False

    try:
        nuevo = int(estado_nuevo)
    except Exception:
        return False

    if actual in (3, 4):
        return False

    if nuevo == 4:
        if actual == 3:
            return False
        return True

    if nuevo != actual and nuevo != (actual + 1):
        return False

    if actual == 0 and nuevo not in (0, 1):
        return False

    if actual == 1 and nuevo not in (1, 2):
        return False

    if actual == 2 and nuevo not in (2, 3):
        return False

    return True


def validar_cancelacion_orden_entregada(estado_actual, estado_nuevo):
    try:
        actual = int(estado_actual)
        nuevo = int(estado_nuevo)
    except Exception:
        return False

    if actual == 3 and nuevo == 4:
        return False

    return True