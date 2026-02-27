from datetime import date
import re

from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask import flash, request, session
from wtforms import DateField, IntegerField, SelectField
from wtforms.validators import ValidationError

from models import db
from models.cai_model import CAI
from models.sucursal_model import Sucursal
from models.validaciones import validarFechafinal, validarRangos


class CAIAdmin(ModelView):
    create_template = "admin/model/cai_create.html"
    edit_template = "admin/model/cai_edit.html"

    can_search = True
    column_searchable_list = ("num_cai",)

    column_list = (
        "ID_Cai",
        "num_cai",
        "Fecha_Emision",
        "Fecha_Final",
        "Rango_Inicial",
        "Rango_Final",
        "Secuencia",
        "estado",
        "sucursal_col",
    )

    column_labels = {
        "num_cai": "Número CAI",
        "Fecha_Emision": "Fecha de emisión",
        "Fecha_Final": "Fecha final",
        "Rango_Inicial": "Rango inicial",
        "Rango_Final": "Rango final",
        "Secuencia": "Secuencia actual",
        "estado": "Estado",
        "sucursal_col": "Sucursal",
    }

    form_columns = (
        "num_cai",
        "Fecha_Emision",
        "Fecha_Final",
        "Rango_Inicial",
        "Rango_Final",
        "Secuencia",
        "estado",
        "ID_sucursal",
    )

    CAI_TOTAL_LEN = 37
    CAI_RAW_LEN = 32
    CAI_REGEX = re.compile(r"^[A-Z0-9]{6}(?:-[A-Z0-9]{6}){4}-[A-Z0-9]{2}$")

    def _quitar_flash_default_admin(self):
        flashes = session.get("_flashes", [])
        if not flashes:
            return
        filtrados = []
        for cat, msg in flashes:
            if isinstance(msg, str) and msg.strip().lower().startswith("record was successfully"):
                continue
            filtrados.append((cat, msg))
        session["_flashes"] = filtrados

    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        resp = super().create_view()
        if request.method == "POST":
            self._quitar_flash_default_admin()
        return resp

    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self):
        resp = super().edit_view()
        if request.method == "POST":
            self._quitar_flash_default_admin()
        return resp

    def _format_sucursal(self, model):
        suc = getattr(model, "sucursal", None)
        if suc:
            return suc.Descripcion
        suc = Sucursal.query.get(model.ID_sucursal) if model.ID_sucursal else None
        return suc.Descripcion if suc else ""

    column_formatters = {
        "estado": lambda v, c, m, p: "Activo" if m.estado == 1 else "Inactivo",
        "sucursal_col": lambda v, c, m, p: v._format_sucursal(m),
    }

    form_overrides = {
        "Rango_Inicial": IntegerField,
        "Rango_Final": IntegerField,
        "estado": SelectField,
        "ID_sucursal": SelectField,
    }

    form_extra_fields = {
        "Fecha_Emision": DateField(
            "Fecha de emisión",
            format="%Y-%m-%d",
            render_kw={"type": "date", "id": "fecha_emision"},
        ),
        "Fecha_Final": DateField(
            "Fecha final",
            format="%Y-%m-%d",
            render_kw={"type": "date", "id": "fecha_final"},
        ),
    }

    form_widget_args = {
        "Rango_Inicial": {"id": "rango_inicial"},
        "Rango_Final": {"id": "rango_final"},
        "Secuencia": {"id": "secuencia_actual"},
        "num_cai": {"id": "num_cai", "maxlength": str(CAI_TOTAL_LEN), "autocomplete": "off"},
    }

    def _cargar_choices(self, form):
        form.ID_sucursal.choices = [(str(s.ID_sucursal), s.Descripcion) for s in Sucursal.query.all()]
        form.estado.choices = [("1", "Activo"), ("0", "Inactivo")]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._cargar_choices(form)
        form.estado.data = "1"
        return form
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#0d47a1")
        return super().render(template, **kwargs)

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._cargar_choices(form)
        if obj is not None and request.method == "GET":
            form.estado.data = "1" if obj.estado == 1 else "0"
            if obj.ID_sucursal is not None:
                form.ID_sucursal.data = str(obj.ID_sucursal)
        return form

    def _actualizar_estados(self):
        hoy = date.today()
        hay_cambios = False
        for cai in CAI.query.all():
            nuevo_estado = cai.estado
            if cai.Fecha_Final and cai.Fecha_Final <= hoy:
                nuevo_estado = 0
            if cai.Secuencia is not None and cai.Rango_Final is not None and cai.Secuencia >= cai.Rango_Final:
                nuevo_estado = 0
            if nuevo_estado != cai.estado:
                cai.estado = nuevo_estado
                hay_cambios = True
                db.session.add(cai)
        if hay_cambios:
            db.session.commit()

    def get_query(self):
        self._actualizar_estados()
        return super().get_query()

    def get_count_query(self):
        self._actualizar_estados()
        return super().get_count_query()

    def _normalizar_cai(self, valor):
        raw = re.sub(r"[^A-Za-z0-9]", "", (valor or "")).upper()
        raw = raw[: self.CAI_RAW_LEN]
        if len(raw) != self.CAI_RAW_LEN:
            return None
        return f"{raw[0:6]}-{raw[6:12]}-{raw[12:18]}-{raw[18:24]}-{raw[24:30]}-{raw[30:32]}"

    def on_model_change(self, form, model, is_created):
        num_cai_in = (getattr(form, "num_cai").data or "").strip()
        num_cai = self._normalizar_cai(num_cai_in)
        if not num_cai or not self.CAI_REGEX.match(num_cai):
            msg = "Formato CAI inválido. Debe ser XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XX (37 caracteres)."
            getattr(form, "num_cai").errors.append(msg)
            raise ValidationError(msg)

        try:
            sucursal_id = int(form.ID_sucursal.data)
        except Exception:
            msg = "Sucursal inválida"
            form.ID_sucursal.errors.append(msg)
            raise ValidationError(msg)

        q = CAI.query.filter(CAI.ID_sucursal == sucursal_id)
        if getattr(model, "ID_Cai", None):
            q = q.filter(CAI.ID_Cai != model.ID_Cai)
        if q.first():
            msg = "Esta sucursal ya tiene un CAI asignado"
            form.ID_sucursal.errors.append(msg)
            raise ValidationError(msg)

        inicio = form.Fecha_Emision.data
        fin = form.Fecha_Final.data

        if inicio and fin and inicio == fin:
            msg = "La fecha de emisión y la fecha final no pueden ser las mismas"
            form.Fecha_Final.errors.append(msg)
            raise ValidationError(msg)

        error_fecha = validarFechafinal(inicio, fin)
        if error_fecha:
            form.Fecha_Final.errors.append(error_fecha)
            raise ValidationError(error_fecha)

        error_rango = validarRangos(form.Rango_Inicial.data, form.Rango_Final.data)
        if error_rango:
            form.Rango_Final.errors.append(error_rango)
            raise ValidationError(error_rango)

        rango_inicial = int(form.Rango_Inicial.data)
        rango_final = int(form.Rango_Final.data)

        if is_created:
            model.Secuencia = rango_inicial
        else:
            sec_field = getattr(form, "Secuencia", None)
            secuencia_nueva = model.Secuencia if sec_field is None or sec_field.data is None else int(sec_field.data)

            if secuencia_nueva < rango_inicial or secuencia_nueva > rango_final:
                msg = "Secuencia incorrecta"
                form.Secuencia.errors.append(msg)
                raise ValidationError(msg)

            model.Secuencia = secuencia_nueva

        hoy = date.today()
        auto_inactivo = False

        if fin and fin <= hoy:
            auto_inactivo = True

        if model.Secuencia is not None and rango_final is not None and model.Secuencia >= rango_final:
            auto_inactivo = True

        if not auto_inactivo and int(form.estado.data) == 0:
            msg = "No puedes poner este CAI en Inactivo manualmente. Solo queda Inactivo cuando llega la fecha final o cuando la secuencia alcanza el rango final."
            form.estado.errors.append(msg)
            raise ValidationError(msg)

        model.estado = 0 if auto_inactivo else int(form.estado.data)
        model.ID_sucursal = sucursal_id
        model.num_cai = num_cai

        if auto_inactivo:
            razones = []
            if fin and fin <= hoy:
                razones.append("llegó a su fecha final")
            if model.Secuencia is not None and rango_final is not None and model.Secuencia >= rango_final:
                razones.append("alcanzó su rango final")
            if razones:
                flash("Este CAI " + " y ".join(razones) + " y quedó inactivo.", "danger")
            else:
                flash("Este CAI quedó inactivo automáticamente.", "danger")
        else:
            flash("CAI guardado correctamente.", "success")
