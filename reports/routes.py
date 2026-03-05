from datetime import datetime
from typing import Any, Dict, List, Tuple

from flask import Blueprint, abort, make_response, request
from flask_login import current_user, login_required
from sqlalchemy import inspect

from models import db, load_models
from reports.generators import generar_excel, generar_pdf

reports_bp = Blueprint("reports", __name__, url_prefix="/reportes")


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


def _formatear_valor(val: Any) -> Any:
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    return val


def _to_str(v: Any) -> str:
    if v is None:
        return ""
    try:
        return str(v).strip()
    except Exception:
        return ""


def _get_attr(obj: Any, name: str) -> Any:
    try:
        return getattr(obj, name, None)
    except Exception:
        return None


def _is_sqla_instance(obj: Any) -> bool:
    if obj is None:
        return False
    try:
        inspect(obj.__class__)
        return True
    except Exception:
        return False


def _first_non_empty(values: List[Any]) -> str:
    for v in values:
        s = _to_str(v)
        if s:
            return s
    return ""


def _display_sqla(obj: Any) -> str:
    if obj is None:
        return ""

    prefer = [
        "numero_factura", "Numero_factura", "NUMERO_FACTURA",
        "num_cai", "Num_cai", "NUM_CAI", "cai",
        "factura", "Factura", "no_factura", "No_factura", "NoFactura",
        "codigo", "Codigo",
        "descripcion", "Descripcion", "detalle", "Detalle",
        "nombre", "Nombre", "name", "Name", "titulo", "Titulo",
        "direccion", "Direccion", "direccion1", "Direccion1", "direccion2", "Direccion2",
        "telefono", "Telefono",
    ]

    out = _first_non_empty([_get_attr(obj, k) for k in prefer])
    if out:
        return out

    try:
        mapper = inspect(obj.__class__)
        col_keys = [c.key for c in getattr(mapper, "columns", [])]
    except Exception:
        col_keys = []

    if col_keys:
        out = _first_non_empty([_get_attr(obj, k) for k in prefer if k in col_keys])
        if out:
            return out

        candidates = []
        for k in col_keys:
            kl = (k or "").lower()
            if kl == "id" or kl.startswith("id_") or kl.endswith("_id"):
                continue
            candidates.append(k)

        out = _first_non_empty([_get_attr(obj, k) for k in candidates])
        if out:
            return out

        out = _first_non_empty([_get_attr(obj, k) for k in col_keys])
        if out:
            return out

    return ""


def _texto_o_vacio(obj: Any) -> str:
    if obj is None:
        return ""

    if isinstance(obj, (str, int, float, bool)):
        return _to_str(obj)

    if isinstance(obj, datetime):
        return _formatear_valor(obj)

    if _is_sqla_instance(obj):
        s = _display_sqla(obj)
        if s:
            return s

    s = _to_str(obj)
    if s.startswith("<") and s.endswith(">"):
        return ""
    return s


def _valor_celda(val: Any) -> Any:
    val = _formatear_valor(val)
    if val is None:
        return ""
    if isinstance(val, (str, int, float, bool)):
        return val
    return _texto_o_vacio(val)


def _separar_camel(s: str) -> str:
    if not s:
        return ""
    out = []
    prev = ""
    for ch in s:
        if prev and ch.isupper() and (prev.islower() or (prev.isupper() and len(out) > 0 and out[-1][-1].islower())):
            out.append(" ")
        out.append(ch)
        prev = ch
    return "".join(out)


def _normalizar_frase(s: Any) -> str:
    txt = str(s or "").strip()
    if not txt:
        return ""
    txt = txt.replace("_", " ").replace("-", " ")
    txt = " ".join(txt.split())
    txt = _separar_camel(txt)
    txt = " ".join(txt.split())
    return txt


def _title_case_es(frase: str) -> str:
    if not frase:
        return ""
    minusculas = {"de", "del", "la", "las", "el", "los", "y", "o", "en", "por", "para", "a", "al"}
    palabras = [p for p in frase.split(" ") if p]
    out = []
    for i, p in enumerate(palabras):
        pl = p.lower()
        if i != 0 and pl in minusculas:
            out.append(pl)
        else:
            out.append(pl[:1].upper() + pl[1:])
    return " ".join(out)


def _titulo_humano(s: Any) -> str:
    base = _normalizar_frase(s).strip()
    return _title_case_es(base)


def _models_registry() -> Dict[str, Any]:
    load_models()

    for attr in ("_sa_registry", "registry"):
        reg = getattr(db.Model, attr, None)
        if reg is not None:
            cr = getattr(reg, "_class_registry", None)
            if isinstance(cr, dict) and cr:
                out = {}
                for k, v in cr.items():
                    if isinstance(k, str) and isinstance(v, type) and not k.startswith("_"):
                        out[k] = v
                if out:
                    return out

    cr = getattr(db.Model, "_decl_class_registry", None)
    if isinstance(cr, dict) and cr:
        out = {}
        for k, v in cr.items():
            if isinstance(k, str) and isinstance(v, type) and not k.startswith("_"):
                out[k] = v
        if out:
            return out

    out = {}
    for cls in db.Model.__subclasses__():
        try:
            out[cls.__name__] = cls
        except Exception:
            pass
    return out


def _key_norm(col: str) -> str:
    s = (col or "").strip().lower()
    s = s.replace("_", " ").replace("-", " ")
    s = " ".join(s.split())
    return s


def _filtrar_columnas_global(columnas: List[str], filas: List[List[Any]]) -> Tuple[List[str], List[List[Any]]]:
    if not columnas:
        return columnas, filas

    remove_idx = set()

    norm_to_idx = {}
    for i, c in enumerate(columnas):
        norm_to_idx.setdefault(_key_norm(c), i)

    for i, c in enumerate(columnas):
        n = _key_norm(c)

        if n in ("us co", "usco", "us co.", "us co id", "us_co", "us"):
            remove_idx.add(i)

    has_direccion = False
    for c in columnas:
        if _key_norm(c) == "direccion":
            has_direccion = True
            break

    if has_direccion:
        for i, c in enumerate(columnas):
            n = _key_norm(c)
            if n in ("id direccion", "direccion id", "id direccion cliente", "direccion cliente id"):
                remove_idx.add(i)

    if not remove_idx:
        return columnas, filas

    keep = [i for i in range(len(columnas)) if i not in remove_idx]
    new_cols = [columnas[i] for i in keep]
    new_rows = []
    for r in filas:
        rr = list(r)
        new_rows.append([rr[i] if i < len(rr) else "" for i in keep])

    return new_cols, new_rows


def _columnas_y_filas(model_cls, limit: int = 10000) -> Tuple[List[str], List[List[Any]]]:
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
        getters.append(lambda obj, k=col.key: _valor_celda(getattr(obj, k, None)))

        rel_key = fk_to_rel.get(col.key)
        if rel_key:
            columnas.append(rel_key)
            getters.append(lambda obj, rk=rel_key: _texto_o_vacio(getattr(obj, rk, None)))

    records = model_cls.query.limit(limit).all()
    filas = [[g(r) for g in getters] for r in records]

    columnas, filas = _filtrar_columnas_global(columnas, filas)
    return columnas, filas


def _reportes_personalizados() -> Dict[str, Tuple[str, Any]]:
    return {
        "ordenes_estado": ("Órdenes por estado", _reporte_ordenes_estado),
    }


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


def _reporte_ordenes_estado() -> Tuple[List[str], List[List[Any]]]:
    models = _models_registry()
    Orden = models.get("OrdenEntrega") or models.get("Orden_Entrega") or models.get("OrdenEntregaModel")

    if not Orden:
        return ["estado", "cantidad"], []

    q = db.session.query(Orden.estado, db.func.count(1)).group_by(Orden.estado).all()

    cols = ["estado", "cantidad"]
    rows: List[List[Any]] = []
    for estado, cantidad in q:
        rows.append([_estado_orden_humano(estado), int(cantidad) if cantidad is not None else 0])

    cols, rows = _filtrar_columnas_global(cols, rows)
    return cols, rows


@reports_bp.get("/<string:reporte>", endpoint="exportar")
@login_required
def exportar(reporte: str):
    formato = (request.args.get("formato") or "pdf").lower().strip()
    modelo = (request.args.get("modelo") or "").strip()

    reportes_custom = _reportes_personalizados()
    key = (reporte or "").lower().strip()

    if key in reportes_custom:
        titulo, fn = reportes_custom[key]
        cols, rows = fn()
        titulo_final = f"REPORTE: {_titulo_humano(titulo)}"
    else:
        models = _models_registry()
        if not models:
            abort(500, "No se pudieron cargar los modelos desde el registry de SQLAlchemy.")

        if not modelo:
            modelo = key

        model_cls = None
        for _, v in models.items():
            try:
                if _modelo_key(v) == modelo.lower():
                    model_cls = v
                    break
            except Exception:
                continue

        if not model_cls:
            abort(404, f"Modelo no encontrado: {modelo}")

        titulo_final = f"REPORTE: {_titulo_humano(model_cls.__name__)}"
        cols, rows = _columnas_y_filas(model_cls)

    usuario = _usuario_impresion()

    if formato in ("excel", "xlsx"):
        content = generar_excel(titulo_final, cols, rows, usuario)
        resp = make_response(content)
        resp.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        resp.headers["Content-Disposition"] = f'attachment; filename="{key}.xlsx"'
        return resp

    content = generar_pdf(titulo_final, cols, rows, usuario)
    resp = make_response(content)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f'attachment; filename="{key}.pdf"'
    return resp