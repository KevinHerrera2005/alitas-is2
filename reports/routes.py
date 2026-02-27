from datetime import datetime
from typing import Any, Dict, List, Tuple

from flask import Blueprint, abort, make_response, request
from flask_login import current_user, login_required
from sqlalchemy import inspect

from models import db, load_models
from reports.generators import generar_excel, generar_pdf

reportes_bp = Blueprint("reports", __name__, url_prefix="/reportes")
reports_bp = reportes_bp


def _usuario_impresion() -> str:
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


def _modelo_key(model_cls) -> str:
    return model_cls.__name__.lower()


def _formatear_dt(val: Any) -> Any:
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    return val


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


def _texto_o_vacio(obj: Any) -> str:
    if obj is None:
        return ""
    for attr in (
        "Nombre", "nombre",
        "Descripcion", "descripcion",
        "Nombre_usuario", "username", "usuario", "email",
        "Nombre_Impuesto", "Nombre_insumo", "Nombre_receta",
        "Nombre_categoria", "Nombre_categoria_receta",
        "Nombre_proveedor", "Nombre_empleado",
        "num_cai",
    ):
        try:
            v = getattr(obj, attr, None)
            if v:
                return str(v)
        except Exception:
            pass
    try:
        return str(obj)
    except Exception:
        return ""


def _columnas_y_filas_amigables(model_cls, limit: int = 10000) -> Tuple[List[str], List[List[Any]]]:
    mapper = inspect(model_cls)
    fk_to_rel: Dict[str, str] = {}

    for rel in mapper.relationships:
        try:
            if getattr(rel, "uselist", False):
                continue
        except Exception:
            pass
        for col in rel.local_columns:
            fk_to_rel[col.key] = rel.key

    columnas: List[str] = []
    getters = []

    for col in mapper.columns:
        columnas.append(col.key)
        getters.append(lambda obj, k=col.key: _formatear_dt(getattr(obj, k, None)))

        rel_key = fk_to_rel.get(col.key)
        if rel_key:
            columnas.append(rel_key)
            getters.append(lambda obj, rk=rel_key: _texto_o_vacio(getattr(obj, rk, None)))

    query = model_cls.query.limit(limit)
    records = query.all()
    filas = [[g(r) for g in getters] for r in records]
    return columnas, filas


def _reportes_personalizados() -> Dict[str, Tuple[str, List[str], Any]]:
    return {
        "ordenes_estado": (
            "Órdenes por Estado",
            ["estado", "cantidad"],
            lambda: _reporte_ordenes_estado(),
        ),
    }


def _reporte_ordenes_estado() -> Tuple[List[str], List[List[Any]]]:
    try:
        Orden = load_models().get("OrdenEntrega")
    except Exception:
        return ["estado", "cantidad"], []

    if not Orden:
        return ["estado", "cantidad"], []

    q = db.session.query(Orden.estado, db.func.count(Orden.id)).group_by(Orden.estado).all()

    cols = ["estado", "cantidad"]
    rows: List[List[Any]] = []
    for estado, cantidad in q:
        rows.append([_estado_orden_humano(estado), int(cantidad) if cantidad is not None else 0])

    return cols, rows


@reportes_bp.get("/<string:reporte>", endpoint="exportar")
@login_required
def exportar(reporte: str):
    formato = (request.args.get("formato") or "pdf").lower().strip()
    modelo = (request.args.get("modelo") or "").strip()

    if not modelo:
        modelo = reporte

    reportes_custom = _reportes_personalizados()
    if reporte in reportes_custom:
        titulo, _, fn = reportes_custom[reporte]
        cols, rows = fn()
    else:
        models = load_models()
        model_cls = None
        for _, v in models.items():
            if _modelo_key(v) == modelo.lower():
                model_cls = v
                break

        if not model_cls:
            abort(404, "Modelo no encontrado")

        titulo = f"Reporte: {model_cls.__name__}"
        cols, rows = _columnas_y_filas_amigables(model_cls)

    usuario = _usuario_impresion()

    if formato in ("excel", "xlsx"):
        content = generar_excel(titulo, cols, rows, usuario)
        resp = make_response(content)
        resp.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        resp.headers["Content-Disposition"] = f'attachment; filename="{reporte}.xlsx"'
        return resp

    content = generar_pdf(titulo, cols, rows, usuario)
    resp = make_response(content)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f'attachment; filename="{reporte}.pdf"'
    return resp