from collections import defaultdict

from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_login import current_user
from flask import redirect, url_for, flash, request
from wtforms import SelectField, SelectMultipleField
from wtforms.validators import ValidationError
from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError
import re
from models.proveedores_model import Proveedor, ProveedorInsumo
from models.insumo_model import Insumo


class ProveedorAdmin(ModelView):
    create_template = "admin/model/proveedor_create.html"
    edit_template = "admin/model/proveedor_edit.html"

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

    column_list = ("Nombre_Proveedor", "Telefono", "email", "activo")
    column_default_sort = ("ID_Proveedor", True)
    page_size = 10
    column_searchable_list = ("Nombre_Proveedor", "email")

    column_labels = {
        "Nombre_Proveedor": "Nombre del proveedor",
        "Telefono": "Teléfono",
        "email": "Email",
        "activo": "Estado",
    }

    column_formatters = {
        "activo": lambda v, c, m, n: "Activo" if m.activo == 1 else "Inactivo"
    }

    form_columns = (
        "Nombre_Proveedor",
        "Telefono",
        "email",
        "insumos_ids",
        "activo",
    )

    form_overrides = {
        "activo": SelectField,
    }

    form_widget_args = {
        "Nombre_Proveedor": {"data-validacion": "nombre", "id": "prov_nombre"},
        "Telefono": {"data-validacion": "telefono", "id": "prov_telefono"},
        "email": {"data-validacion": "email", "id": "prov_email"},
        "insumos_ids": {"id": "prov_insumos"},
        "activo": {"id": "prov_activo"},
    }

    form_extra_fields = {
        "insumos_ids": SelectMultipleField(
            "Este proveedor provee los siguientes insumos",
            coerce=int,
        )
    }

    @staticmethod
    def _norm(txt):
        return " ".join((txt or "").strip().lower().split())

    @staticmethod
    def _parse_int(v):
        try:
            return int(str(v).strip())
        except Exception:
            return None

    def _current_sucursal_id(self):
        sid = getattr(current_user, "id_sucursal", None)
        if sid is None:
            sid = getattr(current_user, "ID_sucursal", None)
        if sid is None:
            sid = getattr(current_user, "ID_Sucursal", None)
        return self._parse_int(sid)

    def _insumo_catalogo(self, sucursal_id):
        if sucursal_id is None:
            return [], {}, {}, defaultdict(list)

        q = (
            self.session.query(Insumo.ID_Insumo, Insumo.Nombre_insumo)
            .filter(Insumo.Nombre_insumo.isnot(None))
        )

        if hasattr(Insumo, "ID_sucursal"):
            q = q.filter(Insumo.ID_sucursal == sucursal_id)

        rows = q.all()

        ids_por_norm = defaultdict(list)
        norm_por_id = {}
        rep_por_norm = {}

        for insumo_id, nombre in rows:
            nombre_txt = (nombre or "").strip()
            norm = self._norm(nombre_txt)
            if not norm:
                continue

            insumo_id = int(insumo_id)
            norm_por_id[insumo_id] = norm
            ids_por_norm[norm].append(insumo_id)

            rep = rep_por_norm.get(norm)
            if rep is None or insumo_id < rep["id"]:
                rep_por_norm[norm] = {"id": insumo_id, "nombre": nombre_txt}

        choices = [(v["id"], v["nombre"]) for v in rep_por_norm.values()]
        choices.sort(key=lambda x: self._norm(x[1]))

        rep_id_por_norm = {k: v["id"] for k, v in rep_por_norm.items()}

        return choices, rep_id_por_norm, norm_por_id, ids_por_norm

    def _ids_representantes_desde_relaciones(self, relaciones_ids, rep_id_por_norm, norm_por_id):
        reps = set()
        for iid in relaciones_ids:
            norm = norm_por_id.get(int(iid))
            if not norm:
                continue
            rep = rep_id_por_norm.get(norm)
            if rep:
                reps.add(int(rep))
        return sorted(reps)

    def create_form(self, obj=None):
        form = super().create_form(obj)

        if hasattr(form, "activo"):
            form._fields.pop("activo")

        sucursal_id = self._current_sucursal_id()

        if hasattr(form, "insumos_ids"):
            choices, _, _, _ = self._insumo_catalogo(sucursal_id)
            form.insumos_ids.choices = choices

        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)

        if hasattr(form, "activo"):
            form.activo.choices = [("1", "Activo"), ("0", "Inactivo")]
            if request.method == "GET" and obj is not None:
                form.activo.data = "1" if obj.activo == 1 else "0"

        sucursal_id = self._current_sucursal_id()

        if hasattr(form, "insumos_ids"):
            choices, rep_id_por_norm, norm_por_id, _ = self._insumo_catalogo(sucursal_id)
            form.insumos_ids.choices = choices

            if obj is not None and request.method == "GET" and sucursal_id is not None:
                q = (
                    self.session.query(ProveedorInsumo.ID_Insumo)
                    .join(Insumo, ProveedorInsumo.ID_Insumo == Insumo.ID_Insumo)
                    .filter(ProveedorInsumo.ID_Proveedor == obj.ID_Proveedor)
                    .filter(ProveedorInsumo.Activo == 1)
                )
                if hasattr(Insumo, "ID_sucursal"):
                    q = q.filter(Insumo.ID_sucursal == sucursal_id)

                activos_ids = [int(r[0]) for r in q.all()]
                form.insumos_ids.data = self._ids_representantes_desde_relaciones(
                    activos_ids,
                    rep_id_por_norm,
                    norm_por_id,
                )

        return form

    def _buscar_existente(self, nombre_norm, email_norm, excluir_id=None):
        q = self.session.query(Proveedor)

        if excluir_id is not None:
            q = q.filter(Proveedor.ID_Proveedor != excluir_id)

        p_nombre = q.filter(func.lower(func.trim(Proveedor.Nombre_Proveedor)) == nombre_norm).first()
        if p_nombre:
            return p_nombre, "nombre"

        p_email = q.filter(func.lower(func.trim(Proveedor.email)) == email_norm).first()
        if p_email:
            return p_email, "email"

        return None, None

    def _validar_campos(self, form, model, is_created):
        nombre = (form.Nombre_Proveedor.data or "").strip()
        telefono_str = str(form.Telefono.data or "").strip()
        email = (form.email.data or "").strip()

        if not nombre or not telefono_str or not email:
            raise ValidationError("Todos los campos son obligatorios.")

        if not telefono_str.isdigit() or len(telefono_str) != 8:
            raise ValidationError("El teléfono debe tener 8 dígitos numéricos.")

        if len(email) < 6 or len(email) > 30:
            raise ValidationError("El correo debe tener entre 6 y 30 caracteres.")

        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError("Debes ingresar un correo electrónico válido.")

        sucursal_id = self._current_sucursal_id()
        if sucursal_id is None:
            raise ValidationError("No se pudo determinar tu sucursal para filtrar insumos.")

        seleccionados = form.insumos_ids.data or []
        if not seleccionados:
            raise ValidationError("Debes seleccionar al menos un insumo.")

        choices, _, _, _ = self._insumo_catalogo(sucursal_id)
        permitidos = {int(cid) for cid, _ in choices}

        seleccionados_ok = []
        for x in seleccionados:
            try:
                seleccionados_ok.append(int(x))
            except Exception:
                continue

        if any(i not in permitidos for i in seleccionados_ok):
            raise ValidationError("Seleccionaste insumos que no pertenecen a tu sucursal.")

        model.Nombre_Proveedor = nombre
        model.Telefono = int(telefono_str)
        model.email = email

        if is_created:
            model.activo = 1
        else:
            if hasattr(form, "activo"):
                model.activo = 1 if str(form.activo.data).strip() == "1" else 0

    def _sincronizar_insumos(self, form, model):
        sucursal_id = self._current_sucursal_id()
        if sucursal_id is None:
            return

        self.session.flush()

        _, rep_id_por_norm, norm_por_id, ids_por_norm = self._insumo_catalogo(sucursal_id)

        seleccion_rep_ids = []
        for x in (form.insumos_ids.data or []):
            try:
                seleccion_rep_ids.append(int(x))
            except Exception:
                continue

        seleccion_norms = set()
        for rid in seleccion_rep_ids:
            norm = norm_por_id.get(int(rid))
            if norm:
                seleccion_norms.add(norm)

        seleccionados_ids = set()
        for norm in seleccion_norms:
            for iid in ids_por_norm.get(norm, []):
                seleccionados_ids.add(int(iid))

        q_rel = (
            self.session.query(ProveedorInsumo)
            .join(Insumo, ProveedorInsumo.ID_Insumo == Insumo.ID_Insumo)
            .filter(ProveedorInsumo.ID_Proveedor == model.ID_Proveedor)
        )
        if hasattr(Insumo, "ID_sucursal"):
            q_rel = q_rel.filter(Insumo.ID_sucursal == sucursal_id)

        relaciones = q_rel.all()

        por_insumo = defaultdict(list)
        for r in relaciones:
            por_insumo[int(r.ID_Insumo)].append(r)

        existentes = {}
        for insumo_id, lista in por_insumo.items():
            lista_orden = sorted(lista, key=lambda x: getattr(x, "ID_Proveedor_Insumo", 0) or 0)
            existentes[insumo_id] = lista_orden[0]
            for extra in lista_orden[1:]:
                extra.Activo = 0

        for insumo_id in seleccionados_ids:
            rel = existentes.get(insumo_id)
            if rel:
                rel.Activo = 1
            else:
                self.session.add(
                    ProveedorInsumo(
                        ID_Proveedor=model.ID_Proveedor,
                        ID_Insumo=insumo_id,
                        Activo=1,
                    )
                )

        for insumo_id, rel in existentes.items():
            if insumo_id not in seleccionados_ids:
                rel.Activo = 0

        self.session.flush()

    def create_model(self, form):
        model = self.model()
        self._validar_campos(form, model, True)

        nombre_norm = self._norm(model.Nombre_Proveedor)
        email_norm = self._norm(model.email)

        with self.session.no_autoflush:
            existente, motivo = self._buscar_existente(nombre_norm, email_norm, excluir_id=None)

            if existente is not None and int(getattr(existente, "activo", 0) or 0) == 1:
                if motivo == "nombre":
                    raise ValidationError("Ya existe un proveedor con ese nombre.")
                raise ValidationError("Ya existe un proveedor con ese email.")

            if existente is not None and int(getattr(existente, "activo", 0) or 0) == 0:
                existente.Nombre_Proveedor = model.Nombre_Proveedor
                existente.Telefono = model.Telefono
                existente.email = model.email
                existente.activo = 1

                self._sincronizar_insumos(form, existente)
                self.session.commit()
                return existente

        self.session.add(model)
        self._sincronizar_insumos(form, model)
        self.session.commit()
        return model

    def on_model_change(self, form, model, is_created):
        if not is_created:
            self._validar_campos(form, model, False)
            self._sincronizar_insumos(form, model)

    def _tiene_historial_ordenes(self, proveedor_id):
        q = text("SELECT TOP 1 1 FROM Ordenes_Proveedores WHERE ID_Proveedor = :pid")
        row = self.session.execute(q, {"pid": int(proveedor_id)}).first()
        return row is not None

    def delete_model(self, model):
        try:
            if self._tiene_historial_ordenes(model.ID_Proveedor):
                flash("Este proveedor no se puede borrar porque ya tiene un historial de órdenes.", "danger")
                return False

            model.activo = 0
            self.session.query(ProveedorInsumo).filter(
                ProveedorInsumo.ID_Proveedor == model.ID_Proveedor
            ).update({"Activo": 0}, synchronize_session=False)

            self.session.commit()
            flash("Proveedor inactivado.", "success")
            return True
        except IntegrityError:
            self.session.rollback()
            flash("Este proveedor no se puede borrar porque ya tiene un historial de órdenes.", "danger")
            return False
        except Exception as e:
            self.session.rollback()
            flash(f"Error al eliminar el proveedor: {str(e)}", "danger")
            return False

    def delete_models(self, models):
        ok = True
        for m in models:
            if not self.delete_model(m):
                ok = False
        return ok

    @action("activar", "Activar seleccionados", "¿Activar los proveedores seleccionados?")
    def action_activar(self, ids):
        try:
            self.session.query(Proveedor).filter(Proveedor.ID_Proveedor.in_(ids)).update(
                {"activo": 1}, synchronize_session=False
            )
            self.session.commit()
            flash("Proveedores activados.", "success")
        except Exception:
            self.session.rollback()
            flash("No se pudo activar.", "danger")

    @action("inactivar", "Inactivar seleccionados", "¿Inactivar los proveedores seleccionados?")
    def action_inactivar(self, ids):
        try:
            self.session.query(Proveedor).filter(Proveedor.ID_Proveedor.in_(ids)).update(
                {"activo": 0}, synchronize_session=False
            )
            self.session.commit()
            flash("Proveedores inactivados.", "success")
        except Exception:
            self.session.rollback()
            flash("No se pudo inactivar.", "danger")
    def render(self, template, **kwargs):
        kwargs.setdefault("panel_color", "#c40000")
        return super().render(template, **kwargs)



def _normalizar_texto(raw):
    if raw is None:
        return None
    out = " ".join(str(raw).strip().split())
    return out or None


def validar_estado_proveedor(raw):
    if raw is None:
        return None
    s = str(raw).strip()
    if s == "":
        return None
    if s not in ("0", "1"):
        return None
    return 1 if s == "1" else 0


def validar_email_proveedor(raw, min_len=6, max_len=60):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if len(out) < int(min_len) or len(out) > int(max_len):
        return None
    if "@" not in out:
        return None
    local, _, domain = out.partition("@")
    if not local or not domain or "." not in domain:
        return None
    return out


def validar_telefono_proveedor(raw):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if not out.isdigit():
        return None
    if len(out) != 8:
        return None
    if out[0] not in ("3", "7", "8", "9"):
        return None
    return out


def validar_nombre_proveedor(raw, min_len=3, max_len=40):
    out = _normalizar_texto(raw)
    if out is None:
        return None
    if len(out) < int(min_len) or len(out) > int(max_len):
        return None
    if re.search(r"(.)\1\1", out.lower()):
        return None
    return out


def validar_insumos_ids_seleccionados(raw_ids, ids_permitidos):
    if raw_ids is None:
        return None
    try:
        permitidos = {int(x) for x in (ids_permitidos or [])}
    except Exception:
        permitidos = set()

    seleccionados = []
    for x in (raw_ids or []):
        try:
            seleccionados.append(int(x))
        except Exception:
            return None

    if not seleccionados:
        return None

    if any(i not in permitidos for i in seleccionados):
        return None

    return seleccionados