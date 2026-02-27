import re

from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_login import current_user
from flask import redirect, url_for, flash, request
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Regexp
from sqlalchemy import func

from models import db
from models.empleado_model import Empleado, Puesto
from models.tipo_documento_model import TipoDocumento
from models.empleado_documento_model import EmpleadoDocumento
from models.sucursal_model import Sucursal

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmpleadoAdmin(ModelView):
    TIPO_DOC_LABELS = {
        1: "DNI",
        2: "RTN",
        3: "Pasaporte",
        4: "Otro",
    }

    can_search = True
    column_searchable_list = ("Nombre", "Apellido", "Username", "Email")

    column_list = (
        "Nombre",
        "Apellido",
        "Username",
        "Telefono",
        "Email",
        "puesto",
        "sucursal_col",
        "tipo_documento_col",
        "numero_documento_col",
        "estado",
    )

    column_default_sort = ("ID_Empleado", True)
    page_size = 10

    create_template = "admin/model/empleado_create.html"
    edit_template = "admin/model/empleado_edit.html"

    column_formatters = {
        "puesto": lambda view, context, model, name: (
            model.puesto.Nombre_Puesto if model.puesto else ""
        ),
        "sucursal_col": lambda view, context, model, name: (
            model.sucursal.Descripcion if getattr(model, "sucursal", None) else ""
        ),
        "tipo_documento_col": lambda view, context, model, name: view._format_tipo_documento(model),
        "numero_documento_col": lambda view, context, model, name: view._format_numero_documento(model),
    }

    form_columns = (
        "Nombre",
        "Apellido",
        "Username",
        "Password",
        "Telefono",
        "Email",
        "ID_Puesto",
        "ID_sucursal",
        "tipo_documento_empleado",
        "descripcion_documento",
        "numero_identificador",
        "estado",
    )

    column_labels = {
        "Nombre": "Nombre",
        "Apellido": "Apellido",
        "Username": "Usuario",
        "Password": "Contraseña",
        "Telefono": "Teléfono",
        "Email": "Correo electrónico",
        "ID_Puesto": "Puesto",
        "puesto": "Puesto",
        "ID_sucursal": "Sucursal",
        "sucursal_col": "Sucursal",
        "estado": "Estado",
        "tipo_documento_col": "Tipo de documento",
        "numero_documento_col": "Número identificador",
        "tipo_documento_empleado": "Tipo de documento a registrar",
        "descripcion_documento": "Descripción del documento",
        "numero_identificador": "Número identificador del documento",
    }

    form_widget_args = {
        "Nombre": {"data-validacion": "nombre", "id": "emp_nombre"},
        "Apellido": {"data-validacion": "nombre", "id": "emp_apellido"},
        "Username": {"data-validacion": "username", "id": "emp_username"},
        "Password": {"data-validacion": "password", "id": "emp_password"},
        "Telefono": {"data-validacion": "telefono", "id": "emp_telefono"},
        "Email": {"data-validacion": "email", "id": "emp_email"},
        "estado": {"id": "emp_estado"},
        "descripcion_documento": {"data-validacion": "descripcion", "id": "emp_doc_descripcion"},
        "numero_identificador": {"id": "emp_doc_numero", "inputmode": "numeric", "pattern": "[0-9]*"},
        "tipo_documento_empleado": {"id": "emp_doc_tipo"},
        "ID_sucursal": {"id": "emp_sucursal"},
    }

    form_overrides = {
        "ID_Puesto": SelectField,
        "ID_sucursal": SelectField,
        "estado": SelectField,
    }

    form_extra_fields = {
        "tipo_documento_empleado": SelectField(
            "Tipo de documento a registrar",
            choices=[
                ("1", "DNI"),
                ("2", "RTN"),
                ("3", "Pasaporte"),
                ("4", "Otro"),
            ],
            validators=[DataRequired(message="El tipo de documento es obligatorio.")],
        ),
        "descripcion_documento": StringField(
            "Descripción del documento",
            validators=[DataRequired(message="La descripción es obligatoria.")],
        ),
        "numero_identificador": StringField(
            "Número identificador del documento",
            validators=[
                DataRequired(message="El número de documento es obligatorio."),
                Regexp("^[0-9]+$", message="Solo se permiten dígitos."),
            ],
            render_kw={"type": "text", "inputmode": "numeric", "pattern": "[0-9]*"},
        ),
    }

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        tipo = getattr(current_user, "tipo", None)
        if tipo == "gerente":
            return True

        if tipo == "empleado":
            puesto = getattr(current_user, "id_puesto", None)
            if puesto is None:
                puesto = getattr(current_user, "ID_Puesto", None)
            try:
                puesto = int(puesto)
            except Exception:
                puesto = None
            return puesto == 16

        return False

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("login"))

    def is_visible(self):
        return self.is_accessible()

    def _build_puesto_choices(self):
        puestos_activos = Puesto.query.filter_by(estado=1).order_by(Puesto.Nombre_Puesto).all()
        return [(str(p.ID_Puesto), p.Nombre_Puesto) for p in puestos_activos]

    def _build_sucursal_choices(self):
        sucursales_activas = Sucursal.query.filter_by(estado=1).order_by(Sucursal.Descripcion).all()
        return [(str(s.ID_sucursal), s.Descripcion) for s in sucursales_activas]

    def _get_tipo_doc_for_empleado(self, empleado):
        if not empleado or not getattr(empleado, "ID_Empleado", None):
            return None

        cache_attr = "_tipo_doc_cache"
        if hasattr(empleado, cache_attr):
            return getattr(empleado, cache_attr)

        tipo_doc_obj = (
            self.session.query(TipoDocumento)
            .join(EmpleadoDocumento, EmpleadoDocumento.tipo_doc == TipoDocumento.tipo_doc)
            .filter(EmpleadoDocumento.ID_Empleado == empleado.ID_Empleado)
            .first()
        )

        setattr(empleado, cache_attr, tipo_doc_obj)
        return tipo_doc_obj

    def _format_tipo_documento(self, empleado):
        tipo_doc_obj = self._get_tipo_doc_for_empleado(empleado)
        if not tipo_doc_obj:
            return ""
        return self.TIPO_DOC_LABELS.get(tipo_doc_obj.tipo, "—")

    def _format_numero_documento(self, empleado):
        tipo_doc_obj = self._get_tipo_doc_for_empleado(empleado)
        if not tipo_doc_obj:
            return ""
        return tipo_doc_obj.numero_documento or ""

    def create_form(self, obj=None):
        form = super().create_form(obj)

        if hasattr(form, "ID_Puesto"):
            form.ID_Puesto.choices = self._build_puesto_choices()

        if hasattr(form, "ID_sucursal"):
            form.ID_sucursal.choices = self._build_sucursal_choices()

        if "estado" in form._fields:
            form._fields.pop("estado")

        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)

        if hasattr(form, "ID_Puesto"):
            form.ID_Puesto.choices = self._build_puesto_choices()
            if request.method == "GET" and obj and obj.ID_Puesto is not None:
                form.ID_Puesto.data = str(obj.ID_Puesto)

        if hasattr(form, "ID_sucursal"):
            form.ID_sucursal.choices = self._build_sucursal_choices()
            if request.method == "GET" and obj and getattr(obj, "ID_sucursal", None) is not None:
                form.ID_sucursal.data = str(obj.ID_sucursal)

        if hasattr(form, "estado"):
            form.estado.choices = [("1", "Activo"), ("0", "Inactivo")]
            if request.method == "GET" and obj is not None:
                form.estado.data = "1" if obj.estado == 1 else "0"

        if obj is not None:
            tipo_doc_obj = self._get_tipo_doc_for_empleado(obj)
            if tipo_doc_obj:
                if hasattr(form, "tipo_documento_empleado"):
                    form.tipo_documento_empleado.data = str(tipo_doc_obj.tipo)
                if hasattr(form, "descripcion_documento"):
                    form.descripcion_documento.data = tipo_doc_obj.descripcion or ""
                if hasattr(form, "numero_identificador"):
                    form.numero_identificador.data = tipo_doc_obj.numero_documento or ""

        return form

    def on_model_change(self, form, model, is_created):
        nombre = (form.Nombre.data or "").strip()
        apellido = (form.Apellido.data or "").strip()
        username = (form.Username.data or "").strip()
        telefono = (form.Telefono.data or "").strip()
        correo = (form.Email.data or "").strip()
        raw_password = (form.Password.data or "").strip()

        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        if not apellido:
            raise ValueError("El apellido es obligatorio.")
        if not username:
            raise ValueError("El usuario es obligatorio.")
        if not telefono:
            raise ValueError("El teléfono es obligatorio.")
        if not correo:
            raise ValueError("El correo electrónico es obligatorio.")

        if not EMAIL_REGEX.match(correo):
            raise ValueError("El correo electrónico no es válido.")

        with self.session.no_autoflush:
            q_user = self.session.query(Empleado).filter(func.lower(Empleado.Username) == func.lower(username))
            if not is_created and getattr(model, "ID_Empleado", None) is not None:
                q_user = q_user.filter(Empleado.ID_Empleado != model.ID_Empleado)
            if q_user.first():
                raise ValueError("Ya existe un empleado con ese usuario.")

            q_tel = self.session.query(Empleado).filter(Empleado.Telefono == telefono)
            if not is_created and getattr(model, "ID_Empleado", None) is not None:
                q_tel = q_tel.filter(Empleado.ID_Empleado != model.ID_Empleado)
            if q_tel.first():
                raise ValueError("Ya existe un empleado con ese teléfono.")

            q_mail = self.session.query(Empleado).filter(func.lower(Empleado.Email) == func.lower(correo))
            if not is_created and getattr(model, "ID_Empleado", None) is not None:
                q_mail = q_mail.filter(Empleado.ID_Empleado != model.ID_Empleado)
            if q_mail.first():
                raise ValueError("Ya existe un empleado con ese correo.")

        model.Nombre = nombre
        model.Apellido = apellido
        model.Username = username
        model.Telefono = telefono
        model.Email = correo

        if is_created:
            if not raw_password:
                raise ValueError("La contraseña es obligatoria.")
            model.Password = raw_password
        else:
            if raw_password:
                model.Password = raw_password

        if hasattr(form, "ID_Puesto"):
            try:
                model.ID_Puesto = int(form.ID_Puesto.data)
            except (TypeError, ValueError):
                raise ValueError("Debes seleccionar un puesto válido.")

        if hasattr(form, "ID_sucursal"):
            try:
                model.ID_sucursal = int(form.ID_sucursal.data)
            except (TypeError, ValueError):
                raise ValueError("Debes seleccionar una sucursal válida.")

        if is_created:
            model.estado = 1
        else:
            if hasattr(form, "estado"):
                model.estado = 1 if str(form.estado.data).strip() == "1" else 0

        tipo_doc_data = getattr(form, "tipo_documento_empleado", None)
        desc_doc_data = getattr(form, "descripcion_documento", None)
        num_doc_data = getattr(form, "numero_identificador", None)

        tipo_val = (tipo_doc_data.data or "").strip() if tipo_doc_data else ""
        desc_val = (desc_doc_data.data or "").strip() if desc_doc_data else ""
        num_val = (num_doc_data.data or "").strip() if num_doc_data else ""

        if not tipo_val or not desc_val or not num_val:
            raise ValueError("Debes completar la información del documento de identidad.")

        if is_created:
            nuevo_tipo_doc = TipoDocumento(descripcion=desc_val, tipo=int(tipo_val), numero_documento=num_val)
            self.session.add(nuevo_tipo_doc)
            self.session.flush()

            enlace = EmpleadoDocumento(tipo_doc=nuevo_tipo_doc.tipo_doc, empleado=model)
            self.session.add(enlace)
        else:
            tipo_doc_obj = self._get_tipo_doc_for_empleado(model)

            if tipo_doc_obj is None:
                nuevo_tipo_doc = TipoDocumento(descripcion=desc_val, tipo=int(tipo_val), numero_documento=num_val)
                self.session.add(nuevo_tipo_doc)
                self.session.flush()

                enlace = EmpleadoDocumento(tipo_doc=nuevo_tipo_doc.tipo_doc, ID_Empleado=model.ID_Empleado)
                self.session.add(enlace)
            else:
                tipo_doc_obj.descripcion = desc_val
                tipo_doc_obj.tipo = int(tipo_val)
                tipo_doc_obj.numero_documento = num_val

    def delete_model(self, model):
        try:
            model.estado = 0
            self.session.add(model)
            self.session.commit()
            flash("Empleado inactivado.", "success")
            return True
        except Exception:
            self.session.rollback()
            flash("No se pudo inactivar el empleado.", "danger")
            return False

    def delete_models(self, models):
        ok = True
        for m in models:
            if not self.delete_model(m):
                ok = False
        return ok

    @action("activar", "Activar seleccionados", "¿Activar los empleados seleccionados?")
    def action_activar(self, ids):
        try:
            self.session.query(Empleado).filter(Empleado.ID_Empleado.in_(ids)).update(
                {"estado": 1}, synchronize_session=False
            )
            self.session.commit()
            flash("Empleados activados.", "success")
        except Exception:
            self.session.rollback()
            flash("No se pudo activar.", "danger")

    @action("inactivar", "Inactivar seleccionados", "¿Inactivar los empleados seleccionados?")
    def action_inactivar(self, ids):
        try:
            self.session.query(Empleado).filter(Empleado.ID_Empleado.in_(ids)).update(
                {"estado": 0}, synchronize_session=False
            )
            self.session.commit()
            flash("Empleados inactivados.", "success")
        except Exception:
            self.session.rollback()
            flash("No se pudo inactivar.", "danger")
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)
