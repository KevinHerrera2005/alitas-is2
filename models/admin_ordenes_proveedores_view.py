import json
from datetime import datetime, date, time as dtime

from flask import flash, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy import inspect, text
from wtforms import SelectField
from wtforms.fields import DateField
from wtforms.validators import ValidationError

from models import db
from models.insumo_model import Insumo
from models.unidades_medida_model import Unidades_medida


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "tipo", None) == "empleado"

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))


def _nombre_col_unidad():
    return getattr(Unidades_medida, "Nombre_Unidad", getattr(Unidades_medida, "Nombre", Unidades_medida.ID_Unidad))


def _equivalente_tipo(id_unidad: int):
    row = db.session.execute(
        text(
            """
            SELECT TOP 1 Equivalente, Tipo
            FROM Unidades_Conversion
            WHERE ID_Unidad = :id
            """
        ),
        {"id": id_unidad},
    ).mappings().first()

    if not row:
        raise ValidationError(f"No existe conversión para la unidad ID {id_unidad} (tabla Unidades_Conversion).")

    equiv = float(row["Equivalente"])
    tipo = int(row["Tipo"])

    if equiv <= 0:
        raise ValidationError(f"Equivalente inválido para unidad ID {id_unidad}.")

    return equiv, tipo


def _convertir_cantidad(cantidad: float, unidad_origen: int, unidad_destino: int) -> float:
    if unidad_origen == unidad_destino:
        return cantidad

    equiv_o, tipo_o = _equivalente_tipo(unidad_origen)
    equiv_d, tipo_d = _equivalente_tipo(unidad_destino)

    if tipo_o != tipo_d:
        raise ValidationError("No se puede convertir entre unidades de distinto tipo (peso vs volumen).")

    base = cantidad * equiv_o
    return base / equiv_d


class OrdenesProveedoresAdmin(SecureModelView):
    can_create = False
    can_edit = True
    can_delete = False

    edit_template = "admin/model/ordenes_proveedores_edit.html"

    column_list = (
        "ID_Orden_Proveedor",
        "Fecha_Inicio",
        "proveedor",
        "sucursal",
        "Estado",
        "Comentarios",
    )

    column_labels = {
        "ID_Orden_Proveedor": "ID",
        "Fecha_Inicio": "Fecha inicio",
        "Fecha_Estimada": "Fecha estimada",
        "Fecha_Entregado": "Fecha entregado",
        "Estado": "Estado",
        "Numero_Factura": "Número de factura",
        "Comentarios": "Comentarios",
        "proveedor": "Proveedor",
        "sucursal": "Sucursal",
    }

    form_columns = (
        "Fecha_Estimada",
        "Fecha_Entregado",
        "Estado",
        "Numero_Factura",
        "Comentarios",
    )

    form_overrides = {
        "Fecha_Estimada": DateField,
        "Fecha_Entregado": DateField,
        "Estado": SelectField,
    }

    form_args = {
        "Fecha_Estimada": {"format": "%Y-%m-%d"},
        "Fecha_Entregado": {"format": "%Y-%m-%d"},
    }

    def _estado_map(self):
        return {0: "Pendiente", 1: "Enviada", 2: "Entregada", 3: "Cancelada"}

    def _estado_label(self, model):
        try:
            v = int(model.Estado)
        except Exception:
            return str(model.Estado)
        return self._estado_map().get(v, str(v))

    column_formatters = {
        "proveedor": lambda v, c, m, p: (
            getattr(m.proveedor, "Nombre_Proveedor", None)
            or getattr(m.proveedor, "Nombre", None)
            or ""
        )
        if getattr(m, "proveedor", None) is not None
        else "",
        "sucursal": lambda v, c, m, p: (getattr(m.sucursal, "Descripcion", None) or "")
        if getattr(m, "sucursal", None) is not None
        else "",
        "Estado": lambda view, context, model, name: view._estado_label(model),
    }

    def get_query(self):
        return super().get_query().filter(self.model.Estado.in_([0, 1]))

    def get_count_query(self):
        return super().get_count_query().filter(self.model.Estado.in_([0, 1]))

    def render(self, template, **kwargs):
        col = _nombre_col_unidad()
        kwargs.setdefault("unidades", Unidades_medida.query.order_by(col.asc()).all())
        return super().render(template, **kwargs)

    def _cargar_choices_estado(self, form, obj=None):
        if not hasattr(form, "Estado"):
            return

        mapa = self._estado_map()

        actual = 0
        if obj is not None:
            try:
                actual = int(obj.Estado or 0)
            except Exception:
                actual = 0

        choices = [(str(actual), mapa.get(actual, str(actual)))]

        if actual in (2, 3):
            form.Estado.choices = choices
            return

        choices.append(("3", mapa.get(3, "Cancelada")))

        if actual == 0:
            choices.append(("1", mapa.get(1, "Enviada")))
        elif actual == 1:
            choices.append(("2", mapa.get(2, "Entregada")))

        final = []
        seen = set()
        for v, lbl in choices:
            if v not in seen:
                final.append((v, lbl))
                seen.add(v)

        form.Estado.choices = final

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._cargar_choices_estado(form, obj=obj)

        if request.method == "GET" and obj is not None and hasattr(form, "Estado"):
            try:
                form.Estado.data = str(int(obj.Estado or 0))
            except Exception:
                form.Estado.data = "0"

        return form

    def on_form_prefill(self, form, id):
        super().on_form_prefill(form, id)

        fe = getattr(form, "Fecha_Estimada", None)
        if fe is not None and isinstance(fe.data, datetime):
            fe.data = fe.data.date()

        fent = getattr(form, "Fecha_Entregado", None)
        if fent is not None and isinstance(fent.data, datetime):
            fent.data = fent.data.date()

        self._cargar_choices_estado(form, obj=self.get_one(id))

    def _obtener_estado_anterior(self, model, is_created):
        if is_created:
            return 0
        try:
            hist = inspect(model).attrs.Estado.history
            if hist.deleted:
                return int(hist.deleted[0])
            if hist.unchanged:
                return int(hist.unchanged[0])
            return int(model.Estado or 0)
        except Exception:
            try:
                return int(model.Estado or 0)
            except Exception:
                return 0

    def on_model_change(self, form, model, is_created):
        with db.session.no_autoflush:
            detalles = list(getattr(model, "detalles", []) or [])

        anterior_estado = self._obtener_estado_anterior(model, is_created)

        try:
            estado_nuevo = int(getattr(form, "Estado").data)
        except Exception:
            raise ValidationError("Estado inválido.")

        if not is_created and anterior_estado in (2, 3) and estado_nuevo != anterior_estado:
            if anterior_estado == 2:
                raise ValidationError("La orden ya fue ENTREGADA y no se puede cambiar ni cancelar.")
            raise ValidationError("Esta orden ya está CANCELADA y no se puede modificar.")

        if estado_nuevo == 3:
            if anterior_estado == 2:
                raise ValidationError("No se puede cancelar una orden entregada.")
            if anterior_estado not in (0, 1, 3):
                raise ValidationError("Transición de estado inválida.")
        else:
            if estado_nuevo != anterior_estado and estado_nuevo != (anterior_estado + 1):
                raise ValidationError("No puedes saltar estados. Debes avanzar de 1 en 1 o cancelar.")
            if anterior_estado == 0 and estado_nuevo not in (0, 1):
                raise ValidationError("Solo puedes pasar de 'Pendiente' a 'Enviada' o cancelar.")
            if anterior_estado == 1 and estado_nuevo not in (1, 2):
                raise ValidationError("Solo puedes pasar de 'Enviada' a 'Entregada' o cancelar.")
            if anterior_estado in (2, 3):
                raise ValidationError("Este estado ya es final y no puede cambiar.")

        inicio = getattr(model, "Fecha_Inicio", None)
        if isinstance(inicio, datetime):
            inicio_d = inicio.date()
        elif isinstance(inicio, date):
            inicio_d = inicio
        else:
            inicio_d = None

        for d in detalles:
            det_id = getattr(d, "ID_Detalle", None)
            if not det_id:
                continue

            csol_raw = (request.form.get(f"det_solicitada_{det_id}") or "").strip()
            usol_raw = (request.form.get(f"det_unidad_solicitada_{det_id}") or "").strip()

            if csol_raw:
                try:
                    csol = float(csol_raw.replace(",", "."))
                except Exception:
                    raise ValidationError("Cantidad solicitada inválida.")
                actual = float(getattr(d, "Cantidad_Solicitada", 0) or 0)
                if abs(csol - actual) > 1e-9:
                    raise ValidationError("No está permitido modificar la cantidad solicitada.")

            if usol_raw:
                try:
                    usol = int(usol_raw)
                except Exception:
                    raise ValidationError("Unidad solicitada inválida.")
                actual_u = int(getattr(d, "ID_Unidad", 0) or 0)
                if usol != actual_u:
                    raise ValidationError("No está permitido modificar la unidad solicitada.")

        nf_field = getattr(form, "Numero_Factura", None)
        nf_raw = (nf_field.data or "").strip() if nf_field is not None else ""
        nf = nf_raw if nf_raw else None

        if nf is not None:
            if (not nf.isdigit()) or len(nf) != 14:
                raise ValidationError("El número de factura debe tener exactamente 14 dígitos numéricos.")

        if estado_nuevo == 2 and not nf:
            raise ValidationError('Debes ingresar el número de factura para marcar la orden como "Entregada".')

        model.Numero_Factura = nf

        data_fe = getattr(form, "Fecha_Estimada", None).data if getattr(form, "Fecha_Estimada", None) else None
        data_fent = getattr(form, "Fecha_Entregado", None).data if getattr(form, "Fecha_Entregado", None) else None

        if estado_nuevo == 1:
            if not data_fe:
                raise ValidationError('Debes ingresar "Fecha estimada" cuando el estado es "Enviada".')
            fe_d = data_fe.date() if isinstance(data_fe, datetime) else data_fe
            if inicio_d and fe_d and fe_d < inicio_d:
                raise ValidationError("La fecha estimada no puede ser una fecha antes de la fecha de inicio.")
            if isinstance(data_fe, date) and not isinstance(data_fe, datetime):
                model.Fecha_Estimada = datetime.combine(data_fe, dtime.min)
            else:
                model.Fecha_Estimada = data_fe
        else:
            if not is_created:
                hist_fe = inspect(model).attrs.Fecha_Estimada.history
                if hist_fe.deleted:
                    model.Fecha_Estimada = hist_fe.deleted[0]

        if estado_nuevo == 2:
            fent_d = data_fent.date() if isinstance(data_fent, datetime) else data_fent
            if inicio_d and fent_d and fent_d < inicio_d:
                raise ValidationError("La fecha entregada no puede ser una fecha antes de la fecha de inicio.")

            if data_fent and isinstance(data_fent, date) and not isinstance(data_fent, datetime):
                model.Fecha_Entregado = datetime.combine(data_fent, dtime.min)
            elif data_fent:
                model.Fecha_Entregado = data_fent
            if not model.Fecha_Entregado:
                model.Fecha_Entregado = datetime.utcnow()

            if inicio_d and isinstance(model.Fecha_Entregado, datetime) and model.Fecha_Entregado.date() < inicio_d:
                raise ValidationError("La fecha entregada no puede ser una fecha antes de la fecha de inicio.")
        else:
            if not is_created:
                hist_fent = inspect(model).attrs.Fecha_Entregado.history
                if hist_fent.deleted:
                    model.Fecha_Entregado = hist_fent.deleted[0]

        if isinstance(getattr(model, "Fecha_Estimada", None), date) and not isinstance(getattr(model, "Fecha_Estimada", None), datetime):
            model.Fecha_Estimada = datetime.combine(model.Fecha_Estimada, dtime.min)

        if isinstance(getattr(model, "Fecha_Entregado", None), date) and not isinstance(getattr(model, "Fecha_Entregado", None), datetime):
            model.Fecha_Entregado = datetime.combine(model.Fecha_Entregado, dtime.min)

        transicion_a_entregada = (anterior_estado != 2 and estado_nuevo == 2)
        if not transicion_a_entregada:
            model.Estado = estado_nuevo
            return

        raw = (request.form.get("recepciones_json") or "").strip()
        if not raw:
            raise ValidationError("Debes ingresar cantidad recibida y unidad recibida en todos los insumos.")

        try:
            data = json.loads(raw)
        except Exception:
            raise ValidationError("El JSON de recepciones no es válido.")

        if not isinstance(data, list) or not data:
            raise ValidationError("Debes registrar al menos una recepción válida.")

        por_detalle = {}
        for item in data:
            try:
                detalle_id = int(item.get("detalle_id"))
                cantidad = float(str(item.get("cantidad")).replace(",", "."))
                unidad_id = int(item.get("unidad_id"))
            except Exception:
                continue

            if detalle_id <= 0 or cantidad <= 0 or unidad_id <= 0:
                continue

            por_detalle[detalle_id] = {"cantidad": cantidad, "unidad_id": unidad_id}

        if not por_detalle:
            raise ValidationError("No hay recepciones válidas para guardar.")

        detalles_map = {d.ID_Detalle: d for d in detalles if getattr(d, "ID_Detalle", None)}
        faltantes = [d.ID_Detalle for d in detalles_map.values() if d.ID_Detalle not in por_detalle]
        if faltantes:
            raise ValidationError("Debes ingresar cantidad y unidad recibida para TODOS los insumos de la orden.")

        for detalle_id, payload in por_detalle.items():
            d = detalles_map.get(detalle_id)
            if not d:
                raise ValidationError("Hay recepciones que no pertenecen a esta orden.")
            d.Cantidad_Recibida = payload["cantidad"]
            d.ID_Unidad_Recibida = payload["unidad_id"]

        for d in detalles_map.values():
            insumo = getattr(d, "insumo", None) or Insumo.query.get(getattr(d, "ID_Insumo", None))
            if not insumo:
                raise ValidationError("No se encontró el insumo asociado a un detalle.")

            if d.Cantidad_Recibida is None or float(d.Cantidad_Recibida) <= 0:
                raise ValidationError("Cantidad recibida inválida en un detalle.")

            unidad_origen = d.ID_Unidad_Recibida or d.ID_Unidad
            if not unidad_origen:
                raise ValidationError("Falta la unidad recibida en un detalle.")

            if not getattr(insumo, "ID_Unidad", None):
                nombre_ins = getattr(insumo, "Nombre_insumo", "N/D")
                raise ValidationError(f"El insumo '{nombre_ins}' no tiene unidad asignada (ID_Unidad).")

            cantidad_convertida = _convertir_cantidad(
                float(d.Cantidad_Recibida),
                int(unidad_origen),
                int(insumo.ID_Unidad),
            )

            actual = float(getattr(insumo, "stock_total", 0) or 0)
            insumo.stock_total = actual + cantidad_convertida

        model.Estado = estado_nuevo


class OrdenesProveedoresDetalleAdmin(SecureModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_list = (
        "ID_Detalle",
        "orden",
        "insumo",
        "Cantidad_Solicitada",
        "unidad",
        "Cantidad_Recibida",
        "unidad_recibida",
    )

    column_labels = {
        "ID_Detalle": "Detalle",
        "orden": "Orden",
        "insumo": "Insumo",
        "Cantidad_Solicitada": "Cantidad solicitada",
        "Cantidad_Recibida": "Cantidad recibida",
        "unidad": "Unidad solicitada",
        "unidad_recibida": "Unidad recibida",
    }

    def _unidad_nombre(self, u):
        if not u:
            return ""
        return getattr(u, "Nombre_Unidad", None) or getattr(u, "Nombre", None) or str(getattr(u, "ID_Unidad", ""))

    column_formatters = {
        "orden": lambda v, c, m, p: str(getattr(getattr(m, "orden", None), "ID_Orden_Proveedor", "") or ""),
        "insumo": lambda v, c, m, p: (
            getattr(getattr(m, "insumo", None), "Nombre_insumo", None)
            or getattr(getattr(m, "insumo", None), "Nombre", None)
            or str(getattr(m, "ID_Insumo", "") or "")
        ),
        "unidad": lambda view, context, model, name: view._unidad_nombre(getattr(model, "unidad", None)),
        "unidad_recibida": lambda view, context, model, name: view._unidad_nombre(getattr(model, "unidad_recibida", None)),
    }
