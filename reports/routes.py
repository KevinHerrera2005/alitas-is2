from datetime import datetime
from typing import Any, Dict, List, Sequence, Tuple

from flask import Blueprint, abort, current_app, make_response, request
from flask_login import current_user, login_required
from sqlalchemy import inspect
from models import db, load_models
from reports.generators import render_excel, render_pdf


reports_bp = Blueprint("reports", __name__, url_prefix="/reportes")


def _safe_username() -> str:
    try:
        if current_user and getattr(current_user, "is_authenticated", False):
            for attr in ("username", "usuario", "email", "Nombre_usuario", "Nombre", "nombre", "Username"):
                val = getattr(current_user, attr, None)
                if val:
                    return str(val)
            return str(getattr(current_user, "id", "Usuario"))
    except Exception:
        pass
    return "Usuario"


def _company_name() -> str:
    return current_app.config.get("COMPANY_NAME", "Alitas El Comelon")


def _model_key(model_cls) -> str:
    return model_cls.__name__.lower()


def _fmt_dt(val: Any) -> Any:
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    return val


def _estado_humano(val: Any) -> str:
    if val is None:
        return ""
    try:
        return "Activo" if int(val) == 1 else "Inactivo"
    except Exception:
        return str(val)


def _estado_orden_humano(val: Any) -> str:
    if val is None:
        return ""
    try:
        n = int(val)
    except Exception:
        return str(val)
    if n == 0:
        return "Pendiente"
    if n == 1:
        return "En camino"
    if n == 2:
        return "Entregada"
    if n == 3:
        return "Cancelada"
    return str(n)


def _str_or_empty(obj: Any) -> str:
    if obj is None:
        return ""
    try:
        return str(obj)
    except Exception:
        return ""


def _friendly_columns_and_rows(model_cls, limit: int = 10000) -> Tuple[List[str], List[List[Any]]]:
    mapper = inspect(model_cls)
    fk_to_rel: Dict[str, str] = {}

    for rel in mapper.relationships:
        for col in rel.local_columns:
            fk_to_rel[col.key] = rel.key

    columns: List[str] = []
    getters = []

    for col in mapper.columns:
        columns.append(col.key)
        getters.append(lambda obj, k=col.key: _fmt_dt(getattr(obj, k, None)))

        rel_key = fk_to_rel.get(col.key)
        if rel_key:
            columns.append(rel_key)
            getters.append(lambda obj, rk=rel_key: _str_or_empty(getattr(obj, rk, None)))

    query = model_cls.query.limit(limit)
    records = query.all()
    rows = [[g(r) for g in getters] for r in records]
    return columns, rows


def _custom_reports() -> Dict[str, Tuple[str, List[str], Any]]:
    from models.insumo_model import Insumo
    from models.proveedores_model import Proveedor
    from models.receta_model import Receta
    from models.orden_entrega_model import OrdenEntrega
    from models.usuario_cliente_model import UsuarioCliente
    from models.direccion_cliente_model import DireccionDelCliente
    from models.sucursal_model import Sucursal
    from models.unidades_medida_model import Unidades_medida
    from models.categoria_insumo_model import CategoriaInsumo
    from models.categoria_recetas_model import Categoria_recetas
    from models.empleado_model import Empleado
    from models.direccion_model import Direccion

    def insumo_rows():
        q = (
            db.session.query(
                Insumo.ID_Insumo,
                Insumo.Nombre_insumo,
                Insumo.stock_total,
                Insumo.precio_lempiras,
                Sucursal.Descripcion.label("Sucursal"),
                Unidades_medida.Nombre.label("Unidad"),
                Unidades_medida.abreviatura.label("Abreviatura"),
                CategoriaInsumo.Nombre_categoria.label("Categoria"),
                CategoriaInsumo.descripcion.label("Categoria_Descripcion"),
            )
            .join(Sucursal, Insumo.ID_sucursal == Sucursal.ID_sucursal)
            .outerjoin(Unidades_medida, Insumo.ID_Unidad == Unidades_medida.ID_Unidad)
            .outerjoin(CategoriaInsumo, Insumo.ID_Categoria == CategoriaInsumo.ID_Categoria)
            .order_by(Insumo.ID_Insumo)
        )
        return [list(r) for r in q.all()]

    def proveedor_rows():
        q = (
            db.session.query(
                Proveedor.ID_Proveedor,
                Proveedor.Nombre_Proveedor,
                Proveedor.Telefono,
                Proveedor.email,
                Proveedor.activo,
            )
            .order_by(Proveedor.ID_Proveedor)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], r[3], _estado_humano(r[4])])
        return out

    def receta_rows():
        q = (
            db.session.query(
                Receta.ID_Receta,
                Receta.Nombre_receta,
                Receta.Estado,
                Receta.descripcion,
                Categoria_recetas.Nombre_categoria_receta.label("Categoria"),
                Categoria_recetas.descripcion.label("Categoria_Descripcion"),
                Sucursal.Descripcion.label("Sucursal"),
            )
            .join(Sucursal, Receta.ID_sucursal == Sucursal.ID_sucursal)
            .outerjoin(Categoria_recetas, Receta.categoria == Categoria_recetas.id_categoria_receta)
            .order_by(Receta.ID_Receta)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], _estado_humano(r[2]), r[3], r[4] or "", r[5] or "", r[6]])
        return out

    def ordentrega_rows():
        q = (
            db.session.query(
                OrdenEntrega.ID_Orden_Entrega,
                OrdenEntrega.Numero_Factura,
                OrdenEntrega.estado,
                OrdenEntrega.Fecha_Creacion,
                Sucursal.Descripcion.label("Sucursal"),
                Empleado.Nombre.label("Repartidor_Nombre"),
                Empleado.Apellido.label("Repartidor_Apellido"),
                Empleado.Username.label("Repartidor_Usuario"),
                UsuarioCliente.Username.label("Cliente_Usuario"),
                UsuarioCliente.nombre.label("Cliente_Nombre"),
                UsuarioCliente.apellido.label("Cliente_Apellido"),
                Direccion.Descripcion.label("Direccion"),
            )
            .join(Sucursal, OrdenEntrega.ID_sucursal == Sucursal.ID_sucursal)
            .outerjoin(Empleado, OrdenEntrega.ID_Empleado_Repartidor == Empleado.ID_Empleado)
            .outerjoin(UsuarioCliente, OrdenEntrega.ID_Usuario_ClienteF == UsuarioCliente.ID_Usuario_ClienteF)
            .outerjoin(Direccion, OrdenEntrega.ID_Direccion == Direccion.ID_Direccion)
            .order_by(OrdenEntrega.ID_Orden_Entrega)
        )
        out = []
        for r in q.all():
            repartidor = " ".join([p for p in [r[5], r[6]] if p]) or (r[7] or "")
            cliente = " ".join([p for p in [r[9], r[10]] if p]) or (r[8] or "")
            out.append([r[0], r[1], _estado_orden_humano(r[2]), _fmt_dt(r[3]), r[4], repartidor, r[7] or "", r[8] or "", cliente, r[11] or ""])
        return out

    def usuariocliente_rows():
        q = (
            db.session.query(
                UsuarioCliente.ID_Usuario_ClienteF,
                UsuarioCliente.Username,
                UsuarioCliente.nombre,
                UsuarioCliente.apellido,
                UsuarioCliente.telefono,
                UsuarioCliente.correo,
                UsuarioCliente.estado,
                Sucursal.Descripcion.label("Sucursal"),
            )
            .join(Sucursal, UsuarioCliente.ID_sucursal == Sucursal.ID_sucursal)
            .order_by(UsuarioCliente.ID_Usuario_ClienteF)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], r[3], r[4], r[5] or "", _estado_humano(r[6]), r[7]])
        return out

    def direcciondelcliente_rows():
        q = (
            db.session.query(
                DireccionDelCliente.ID_US_CO,
                UsuarioCliente.Username.label("Cliente_Usuario"),
                UsuarioCliente.nombre.label("Cliente_Nombre"),
                UsuarioCliente.apellido.label("Cliente_Apellido"),
                Direccion.Descripcion.label("Direccion"),
            )
            .join(UsuarioCliente, DireccionDelCliente.ID_Usuario_ClienteF == UsuarioCliente.ID_Usuario_ClienteF)
            .join(Direccion, DireccionDelCliente.ID_Direccion == Direccion.ID_Direccion)
            .order_by(DireccionDelCliente.ID_US_CO)
        )
        out = []
        for r in q.all():
            cliente = " ".join([p for p in [r[2], r[3]] if p]) or (r[1] or "")
            out.append([r[0], r[1] or "", cliente, r[4] or ""])
        return out

    return {
        "insumo": (
            "Reporte de Insumos",
            ["ID", "Insumo", "Stock", "Precio (L)", "Sucursal", "Unidad", "Abreviatura", "Categoría", "Descripción categoría"],
            insumo_rows,
        ),
        "proveedor": (
            "Reporte de Proveedores",
            ["ID", "Proveedor", "Teléfono", "Email", "Estado"],
            proveedor_rows,
        ),
        "receta": (
            "Reporte de Recetas",
            ["ID", "Receta", "Estado", "Descripción", "Categoría", "Descripción categoría", "Sucursal"],
            receta_rows,
        ),
        "ordentrega": (
            "Reporte de Órdenes de Entrega",
            ["ID", "Factura", "Estado", "Fecha creación", "Sucursal", "Repartidor", "Repartidor usuario", "Cliente usuario", "Cliente", "Dirección"],
            ordentrega_rows,
        ),
        "usuariocliente": (
            "Reporte de Clientes",
            ["ID", "Usuario", "Nombre", "Apellido", "Teléfono", "Correo", "Estado", "Sucursal"],
            usuariocliente_rows,
        ),
        "direcciondelcliente": (
            "Reporte de Direcciones de Clientes",
            ["ID", "Cliente usuario", "Cliente", "Dirección"],
            direcciondelcliente_rows,
        ),
    }


def _get_report_data(key: str) -> Tuple[str, List[str], List[List[Any]]]:
    load_models()
    custom = _custom_reports()
    if key in custom:
        title, cols, loader = custom[key]
        rows = loader()
        return title, list(cols), [[_fmt_dt(c) for c in r] for r in rows]

    model_cls = None
    for mapper in db.Model.registry.mappers:
        cls = mapper.class_
        if _model_key(cls) == key:
            model_cls = cls
            break

    if not model_cls:
        abort(404)

    title = f"Reporte de {model_cls.__name__}"
    cols, rows = _friendly_columns_and_rows(model_cls)
    return title, cols, rows


@reports_bp.get("/<string:reporte>")
@login_required
def exportar(reporte: str):
    formato = (request.args.get("formato") or "pdf").lower().strip()
    if formato not in ("pdf", "excel", "xlsx"):
        abort(400)

    titulo, columnas, filas = _get_report_data(reporte)
    printed_by = _safe_username()

    if formato == "pdf":
        pdf_bytes = render_pdf(titulo, columnas, filas, printed_by=printed_by)
        filename = f"{reporte}.pdf"
        resp = make_response(pdf_bytes)
        resp.headers["Content-Type"] = "application/pdf"
        resp.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp

    xlsx_bytes = render_excel(titulo, columnas, filas)
    filename = f"{reporte}.xlsx"
    resp = make_response(xlsx_bytes)
    resp.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    resp.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp
