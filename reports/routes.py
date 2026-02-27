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

    records = model_cls.query.limit(limit).all()
    filas = [[g(r) for g in getters] for r in records]
    return columnas, filas


def _reportes_personalizados() -> Dict[str, Tuple[str, List[str], Any]]:
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
    from models.cai_model import CAI
    from models.cai_historico_model import CAIHistorico
    from models.impuestos_model import Impuesto
    from models.impuesto_tasa_historica_model import ImpuestoTasaHistorica
    from models.parametro_sar_model import ParametroSAR

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
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], r[3], r[4], r[5] or "", r[6] or "", r[7] or "", r[8] or ""])
        return out

    def proveedor_rows():
        q = (
            db.session.query(
                Proveedor.ID_Proveedor,
                Proveedor.Nombre_proveedor,
                Proveedor.telefono,
                Proveedor.email,
                Proveedor.estado,
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
                OrdenEntrega.ID_OrdenEntrega,
                OrdenEntrega.factura,
                OrdenEntrega.estado,
                OrdenEntrega.Fecha_Creacion,
                Sucursal.Descripcion.label("Sucursal"),
            )
            .outerjoin(Sucursal, OrdenEntrega.ID_sucursal == Sucursal.ID_sucursal)
            .order_by(OrdenEntrega.ID_OrdenEntrega)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], _estado_orden_humano(r[2]), _formatear_dt(r[3]), r[4] or ""])
        return out

    def usuario_cliente_rows():
        q = (
            db.session.query(
                UsuarioCliente.ID_Usuario,
                UsuarioCliente.Nombre_usuario,
                UsuarioCliente.email,
                UsuarioCliente.estado,
            )
            .order_by(UsuarioCliente.ID_Usuario)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], _estado_humano(r[3])])
        return out

    def direccion_cliente_rows():
        q = (
            db.session.query(
                DireccionDelCliente.ID_DireccionCliente,
                DireccionDelCliente.ID_Usuario,
                Direccion.Descripcion.label("Direccion"),
            )
            .outerjoin(Direccion, DireccionDelCliente.ID_Direccion == Direccion.ID_Direccion)
            .order_by(DireccionDelCliente.ID_DireccionCliente)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2] or ""])
        return out

    def empleado_rows():
        q = (
            db.session.query(
                Empleado.ID_Empleado,
                Empleado.Nombre_empleado,
                Empleado.apellido,
                Empleado.telefono,
                Empleado.email,
                Empleado.estado,
            )
            .order_by(Empleado.ID_Empleado)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], r[3], r[4], _estado_humano(r[5])])
        return out

    def cai_rows():
        q = (
            db.session.query(
                CAI.ID_CAI,
                CAI.num_cai,
                CAI.fecha_inicio,
                CAI.fecha_fin,
                CAI.rango_desde,
                CAI.rango_hasta,
                CAI.estado,
            )
            .order_by(CAI.ID_CAI)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], _formatear_dt(r[2]), _formatear_dt(r[3]), r[4], r[5], _estado_humano(r[6])])
        return out

    def cai_historico_rows():
        q = (
            db.session.query(
                CAIHistorico.ID_CAIHistorico,
                CAIHistorico.num_cai,
                CAIHistorico.fecha_inicio,
                CAIHistorico.fecha_fin,
                CAIHistorico.rango_desde,
                CAIHistorico.rango_hasta,
                CAIHistorico.estado,
            )
            .order_by(CAIHistorico.ID_CAIHistorico)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], _formatear_dt(r[2]), _formatear_dt(r[3]), r[4], r[5], _estado_humano(r[6])])
        return out

    def impuesto_rows():
        q = (
            db.session.query(
                Impuesto.ID_Impuesto,
                Impuesto.Nombre_Impuesto,
                Impuesto.porcentaje,
                Impuesto.estado,
            )
            .order_by(Impuesto.ID_Impuesto)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], _estado_humano(r[3])])
        return out

    def impuesto_tasa_hist_rows():
        q = (
            db.session.query(
                ImpuestoTasaHistorica.ID_ImpuestoTasaHistorica,
                ImpuestoTasaHistorica.ID_Impuesto,
                ImpuestoTasaHistorica.tasa,
                ImpuestoTasaHistorica.fecha_inicio,
                ImpuestoTasaHistorica.fecha_fin,
            )
            .order_by(ImpuestoTasaHistorica.ID_ImpuestoTasaHistorica)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], _formatear_dt(r[3]), _formatear_dt(r[4])])
        return out

    def parametro_sar_rows():
        q = (
            db.session.query(
                ParametroSAR.ID_Parametro,
                ParametroSAR.nombre,
                ParametroSAR.valor,
                ParametroSAR.descripcion,
            )
            .order_by(ParametroSAR.ID_Parametro)
        )
        out = []
        for r in q.all():
            out.append([r[0], r[1], r[2], r[3]])
        return out

    return {
        "insumo": ("Reporte de Insumos", ["ID", "Nombre", "Stock", "Precio", "Sucursal", "Unidad", "Abreviatura", "Categoria", "Categoria_Descripcion"], insumo_rows),
        "proveedor": ("Reporte de Proveedores", ["ID", "Nombre", "Telefono", "Email", "Estado"], proveedor_rows),
        "receta": ("Reporte de Recetas", ["ID", "Nombre", "Estado", "Descripcion", "Categoria", "Categoria_Descripcion", "Sucursal"], receta_rows),
        "ordentrega": ("Reporte de Ordenes Entrega", ["ID", "Factura", "Estado", "Fecha_Creacion", "Sucursal"], ordentrega_rows),
        "usuario": ("Reporte de Usuarios", ["ID", "Usuario", "Email", "Estado"], usuario_cliente_rows),
        "direccioncliente": ("Reporte de Direcciones Cliente", ["ID", "ID_Usuario", "Direccion"], direccion_cliente_rows),
        "empleado": ("Reporte de Empleados", ["ID", "Nombre", "Apellido", "Telefono", "Email", "Estado"], empleado_rows),
        "cai": ("Reporte de CAI", ["ID", "CAI", "Inicio", "Fin", "Desde", "Hasta", "Estado"], cai_rows),
        "caihistorico": ("Reporte de CAI Historico", ["ID", "CAI", "Inicio", "Fin", "Desde", "Hasta", "Estado"], cai_historico_rows),
        "impuesto": ("Reporte de Impuestos", ["ID", "Nombre", "Porcentaje", "Estado"], impuesto_rows),
        "impuestotasahistorica": ("Reporte de Impuesto Tasa Historica", ["ID", "ID_Impuesto", "Tasa", "Inicio", "Fin"], impuesto_tasa_hist_rows),
        "parametrosar": ("Reporte de Parametros SAR", ["ID", "Nombre", "Valor", "Descripcion"], parametro_sar_rows),
    }


def _obtener_datos_reporte(key: str) -> Tuple[str, List[str], List[List[Any]]]:
    load_models()
    personalizados = _reportes_personalizados()
    if key in personalizados:
        title, cols, loader = personalizados[key]
        rows = loader()
        return title, list(cols), [[_formatear_dt(c) for c in r] for r in rows]

    model_cls = None
    for mapper in db.Model.registry.mappers:
        cls = mapper.class_
        if _modelo_key(cls) == key:
            model_cls = cls
            break

    if not model_cls:
        abort(404)

    title = f"Reporte de {model_cls.__name__}"
    cols, rows = _columnas_y_filas_amigables(model_cls)
    return title, cols, rows


@reportes_bp.get("/<string:reporte>", endpoint="exportar")
@login_required
def exportar(reporte: str):
    formato = (request.args.get("formato") or "pdf").lower().strip()
    title, cols, rows = _obtener_datos_reporte(reporte.lower())

    usuario = _usuario_impresion()
    filename = f"{reporte}.{ 'xlsx' if formato in ('excel', 'xlsx') else 'pdf' }"

    if formato in ("excel", "xlsx"):
        content = generar_excel(title, cols, rows, usuario)
        resp = make_response(content)
        resp.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        resp.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp

    content = generar_pdf(title, cols, rows, usuario)
    resp = make_response(content)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp