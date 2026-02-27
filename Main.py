import os
import re
import sys
sys.modules["Main"] = sys.modules[__name__]
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import quote_plus

from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, UserMixin
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import validators as fa_validators
from flask_babel import Babel
from models import db

fa_validators.Unique.field_flags = {"unique": True}

_BOOTSTRAPPED = False


def _base_dir():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def _resource_path(filename):
    return os.path.join(_base_dir(), filename)


def _split_sql_batches(sql_text):
    lines = sql_text.splitlines()
    batches = []
    buf = []
    for line in lines:
        if re.match(r"^\s*GO\s*$", line, flags=re.IGNORECASE):
            chunk = "\n".join(buf).strip()
            if chunk:
                batches.append(chunk)
            buf = []
        else:
            buf.append(line)
    chunk = "\n".join(buf).strip()
    if chunk:
        batches.append(chunk)
    return batches


def _set_database_in_conn_str(conn_str, db_name):
    parts = conn_str.split(";")
    new_parts = []
    replaced = False
    for p in parts:
        p = (p or "").strip()
        if not p:
            continue
        if p.upper().startswith("DATABASE="):
            new_parts.append(f"DATABASE={db_name}")
            replaced = True
        else:
            new_parts.append(p)
    if not replaced:
        new_parts.append(f"DATABASE={db_name}")
    return ";".join(new_parts) + ";"


def _db_exists(master_conn_str, db_name):
    import pyodbc
    conn = pyodbc.connect(master_conn_str, autocommit=True)
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM sys.databases WHERE name = ?", (db_name,))
        row = cur.fetchone()
        cur.close()
        return row is not None
    finally:
        conn.close()


def ejecutar_init_sql_si_aplica(odbc_conn_str, init_sql_path, db_name):
    import pyodbc

    if not os.path.exists(init_sql_path):
        raise FileNotFoundError(f"No existe init.sql en: {init_sql_path}")

    master_conn_str = _set_database_in_conn_str(odbc_conn_str, "master")

    if _db_exists(master_conn_str, db_name):
        print(f"[INIT] La base '{db_name}' ya existe. No se ejecuta init.sql.")
        return

    print(f"[INIT] La base '{db_name}' no existe. Ejecutando init.sql...")

    with open(init_sql_path, "r", encoding="utf-8", errors="ignore") as f:
        sql_text = f.read()

    batches = _split_sql_batches(sql_text)

    conn = pyodbc.connect(master_conn_str, autocommit=True)
    try:
        cur = conn.cursor()
        for batch in batches:
            if batch.strip():
                cur.execute(batch)
        cur.close()
    finally:
        conn.close()

    print("[INIT] init.sql ejecutado.")

## poner sus credenciales aqui su sa  con la contrasseña y su nombre del sql o sea DB_SERVER = os.getenv("DB_SERVER", r"DESKTOP-5FSTOOH\SQLEXPRESS")
DB_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 17 for SQL Server")
DB_SERVER = os.getenv("DB_SERVER", r"DESKTOP-5FSTOOH\SQLEXPRESS")
DB_NAME = os.getenv("DB_NAME", "ALITAS EL COMELON SF")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "kevin190305")
DB_TRUST_CERT = os.getenv("DB_TRUST_CERT", "yes")

connection_string = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    f"TrustServerCertificate={DB_TRUST_CERT};"
)

init_sql_path = _resource_path("init.sql")
if os.getenv("SKIP_DB_INIT", "0").strip() != "1":
    ejecutar_init_sql_si_aplica(connection_string, init_sql_path, DB_NAME)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave_super_segura")
app.config["BABEL_DEFAULT_LOCALE"] = "es"
babel = Babel(app)
import pytz
app.config["COMPANY_NAME"] = os.getenv("COMPANY_NAME", "Alitas El Comelon")
app.config["COMPANY_LOGO_PATH"] = _resource_path(os.getenv("COMPANY_LOGO_RELATIVE", os.path.join("static", "img", "logo.png")))
app.config["REPORTS_TIMEZONE"] = pytz.timezone(os.getenv("REPORTS_TZ", "America/Tegucigalpa"))

app.config["GMAIL_USER"] = os.getenv("GMAIL_USER", "alitaselcomelon@gmail.com")
app.config["GMAIL_PASSWORD"] = os.getenv("GMAIL_PASSWORD", "hhbggiqfxnqzpmzo")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import load_models
load_models()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Primero debes iniciar sesión."
login_manager.login_message_category = "warning"


class AuthUser(UserMixin):
    def __init__(self, tipo, db_id, nombre=None, id_puesto=None, id_sucursal=None):
        self.tipo = tipo
        self.db_id = int(db_id)
        self.nombre = nombre
        self.id_puesto = id_puesto
        self.id_sucursal = id_sucursal
        self.ID_sucursal = id_sucursal

        if self.tipo == "cliente":
            self.ID_Usuario_ClienteF = self.db_id
        elif self.tipo == "empleado":
            self.ID_Empleado = self.db_id
            self.ID_Puesto = id_puesto
        elif self.tipo == "gerente":
            self.ID_gerente = self.db_id

    def get_id(self):
        if self.tipo == "cliente":
            prefijo = "C"
        elif self.tipo == "empleado":
            prefijo = "E"
        elif self.tipo == "gerente":
            prefijo = "G"
        else:
            prefijo = "U"
        return f"{prefijo}-{self.db_id}"


def _build_user_from_prefix(pref, real_id):
    from models.empleado_model import Empleado
    from models.gerente_model import Gerente
    from models.usuario_cliente_model import UsuarioCliente as ClienteModel

    if pref == "G":
        g = Gerente.query.get(real_id)
        if not g:
            return None
        return AuthUser(
            tipo="gerente",
            db_id=getattr(g, "ID_gerente", real_id),
            nombre=getattr(g, "Username", None),
            id_sucursal=getattr(g, "ID_sucursal", None) or getattr(g, "id_sucursal", None),
        )

    if pref == "E":
        e = Empleado.query.get(real_id)
        if not e:
            return None
        return AuthUser(
            tipo="empleado",
            db_id=getattr(e, "ID_Empleado", real_id),
            nombre=getattr(e, "Nombre", None),
            id_puesto=getattr(e, "ID_Puesto", None),
            id_sucursal=getattr(e, "ID_sucursal", None) or getattr(e, "id_sucursal", None),
        )

    if pref == "C":
        c = ClienteModel.query.get(real_id)
        if not c:
            return None
        return AuthUser(
            tipo="cliente",
            db_id=getattr(c, "ID_Usuario_ClienteF", real_id),
            nombre=getattr(c, "nombre", None) or getattr(c, "Username", None),
            id_sucursal=getattr(c, "ID_sucursal", None) or getattr(c, "id_sucursal", None),
        )

    return None


@login_manager.user_loader
def load_user(user_id):
    try:
        pref, real_id = user_id.split("-", 1)
        return _build_user_from_prefix(pref, int(real_id))
    except Exception:
        return None


@login_manager.request_loader
def load_user_from_request(req):
    user_id = session.get("_user_id")
    if user_id:
        u = load_user(user_id)
        if u:
            return u

    cid = session.get("cliente_id")
    if cid:
        try:
            return _build_user_from_prefix("C", int(cid))
        except Exception:
            return None

    gid = session.get("gerente_id")
    if gid:
        try:
            return _build_user_from_prefix("G", int(gid))
        except Exception:
            return None

    eid = session.get("empleado_id")
    if eid:
        try:
            return _build_user_from_prefix("E", int(eid))
        except Exception:
            return None

    return None

import time

_CONFIRM_CODES = {}

def registrar_codigo_confirmacion(destino, codigo, ttl_seconds=600):
    destino = (destino or "").strip().lower()
    codigo = (codigo or "").strip()
    if not destino or not codigo:
        return False
    _CONFIRM_CODES[destino] = {"codigo": codigo, "expira": time.time() + int(ttl_seconds)}
    return True

def validar_codigo_confirmacion(destino, codigo):
    destino = (destino or "").strip().lower()
    codigo = (codigo or "").strip()
    if not destino or not codigo:
        return False

    data = _CONFIRM_CODES.get(destino)
    if not data:
        return False

    if time.time() > float(data.get("expira", 0)):
        _CONFIRM_CODES.pop(destino, None)
        return False

    if data.get("codigo") != codigo:
        return False

    _CONFIRM_CODES.pop(destino, None)
    return True

def enviar_y_registrar_codigo_confirmacion(destino, codigo, ttl_seconds=600):
    ok, err = enviar_codigo_confirmacion(destino, codigo)
    if not ok:
        return False, err
    registrar_codigo_confirmacion(destino, codigo, ttl_seconds=ttl_seconds)
    return True, None
def enviar_codigo_confirmacion(destino, codigo):
    remitente = (app.config.get("GMAIL_USER") or "").strip()
    clave = (app.config.get("GMAIL_PASSWORD") or "").strip()

    if not remitente or not clave:
        return False, "Falta configurar GMAIL_USER o GMAIL_PASSWORD"
    if not destino:
        return False, "Correo inválido"

    asunto = "Codigo de confirmacion"
    cuerpo = f"Tu codigo de confirmacion es: {codigo}"

    mensaje = MIMEMultipart()
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destino
    mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

    try:
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto, timeout=20) as servidor:
            servidor.login(remitente, clave)
            servidor.sendmail(remitente, [destino], mensaje.as_string())
        return True, None
    except smtplib.SMTPAuthenticationError:
        return False, "Gmail rechazo la autenticacion (usa App Password)"
    except Exception:
        return False, "No se pudo enviar el correo"


class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False


def bootstrap_app(flask_app):
    from models.proveedores_model import ProveedorInsumo
    from models.impuestos_model import ImpuestoCategoria
    from models.direccion_cliente_model import DireccionDelCliente
    from models.pago_detalle_model import PagoDetalle
    from models.factura_model import Factura
    from models.factura_detalle_model import FacturaDetalle

    from models.insumo_model import Insumo
    from models.categoria_insumo_model import CategoriaInsumo
    from models.unidades_medida_model import Unidades_medida
    from models.empleado_model import Empleado, Puesto
    from models.categoria_recetas_model import Categoria_recetas
    from models.sucursal_model import Sucursal
    from models.insumo_precio_historico_model import InsumoPrecioHistorico
    from models.recetas_precio_historico_model import RecetaPrecioHistorico
    from models.receta_model import Receta
    from models.proveedores_model import Proveedor
    from models.impuestos_model import Impuesto
    from models.impuesto_tasa_historica_model import ImpuestoTasaHistorica
    from models.carrito_model import Carrito
    from models.usuario_cliente_model import UsuarioCliente
    from models.cai_model import CAI
    from models.cai_historico_model import CAIHistorico
    from models.tipo_documento_model import TipoDocumento
    from models.empleado_documento_model import EmpleadoDocumento
    from models.parametro_sar_model import ParametroSAR
    from models.orden_entrega_model import OrdenEntrega
    from models.ordenes_proveedores_model import OrdenesProveedores, OrdenesProveedoresDetalle
    from models.historial_ordenes_repartidor_model import HistorialOrdenesRepartidor

    from models.admin_unidades_medida_view import UnidadesMedidaAdmin
    from models.admin_insumo_view import InsumoAdmin
    from models.admin_categoria_view import CategoriaAdmin
    from models.admin_empleado_view import EmpleadoAdmin
    from models.admin_puesto_view import PuestoAdmin
    from models.admin_categoria_receta_view import CategoriaRecetaAdmin
    from models.admin_sucursal_view import SucursalAdmin
    from models.admin_insumo_precio_view import InsumoPrecioHistoricoAdmin
    from models.admin_receta_precio_view import RecetaPrecioHistoricoAdmin
    from models.admin_recetas_view import RecetaAdmin
    from models.admin_proveedores_view import ProveedorAdmin
    from models.admin_impuestos_view import ImpuestoAdmin
    from models.admin_impuesto_tasa_historica_view import ImpuestoTasaHistoricaAdmin
    from models.admin_carrito_view import CarritoAdmin
    from models.admin_usuario_cliente_admin import UsuarioClienteAdmin
    from models.admin_cai_view import CAIAdmin
    from models.admin_cai_historico_view import CAIHistoricoAdmin
    from models.admin_tipo_documento_view import TipoDocumentoAdmin
    from models.admin_empleado_documento_view import EmpleadoDocumentoAdmin
    from models.admin_parametro_sar_view import ParametroSARAdmin
    from models.admin_orden_entrega_view import OrdenEntregaAdmin
    from models.admin_ordenes_proveedores_view import OrdenesProveedoresAdmin, OrdenesProveedoresDetalleAdmin
    from models.historial_ordenes_repartidor_admin import HistorialOrdenesRepartidorAdmin
    from models.admin_historial_ordenes_proveedores_view import HistorialOrdenesProveedoresAdmin

    admin = Admin(
        flask_app,
        name="Panel Administrativo",
        index_view=MyAdminIndexView(),
        template_mode="bootstrap4",
    )

    admin.add_view(InsumoAdmin(Insumo, db.session, category="Inventario", name="Insumos"))
    admin.add_view(CategoriaAdmin(CategoriaInsumo, db.session, category="Inventario", name="Categorías"))
    admin.add_view(UnidadesMedidaAdmin(Unidades_medida, db.session, category="Inventario", name="Unidades de Medida", endpoint="unidades_medida_admin"))
    admin.add_view(EmpleadoAdmin(Empleado, db.session, category="Personal", name="Empleados", endpoint="empleados_admin"))
    admin.add_view(PuestoAdmin(Puesto, db.session, category="Personal", name="Puestos", endpoint="puestos_admin"))
    admin.add_view(CategoriaRecetaAdmin(Categoria_recetas, db.session, category="Recetas", name="Categoría de las Recetas", endpoint="categoria_recetas_admin"))
    admin.add_view(SucursalAdmin(Sucursal, db.session, category="Gerencia", name="Sucursales", endpoint="sucursales_admin"))
    admin.add_view(InsumoPrecioHistoricoAdmin(InsumoPrecioHistorico, db.session, category="Auditoría de Precios", name="Histórico de Insumos", endpoint="insumo_precio_historico_admin"))
    admin.add_view(RecetaPrecioHistoricoAdmin(RecetaPrecioHistorico, db.session, category="Auditoría de Precios", name="Histórico de Recetas", endpoint="receta_precio_historico_admin"))
    admin.add_view(RecetaAdmin(Receta, db.session, category="Recetas", name="Recetas", endpoint="recetas_admin"))
    admin.add_view(ProveedorAdmin(Proveedor, db.session, category="Gerencia", name="Proveedores", endpoint="proveedores_admin"))
    admin.add_view(ImpuestoAdmin(Impuesto, db.session, category="Contabilidad", name="Impuestos", endpoint="impuestos_admin"))
    admin.add_view(ImpuestoTasaHistoricaAdmin(ImpuestoTasaHistorica, db.session, category="Contabilidad", name="Histórico tasas", endpoint="impuesto_tasa_historica_admin"))
    admin.add_view(CarritoAdmin(Carrito, db.session, category="Contabilidad", name="Carrito"))
    admin.add_view(UsuarioClienteAdmin(UsuarioCliente, db.session))
    admin.add_view(CAIAdmin(CAI, db.session, name="CAI", category="Contabilidad"))
    admin.add_view(CAIHistoricoAdmin(CAIHistorico, db.session, name="CAI histórico", category="Contabilidad", endpoint="cai_historico_admin"))
    admin.add_view(TipoDocumentoAdmin(TipoDocumento, db.session, category="Personal", name="Tipos de documentos", endpoint="tipos_documento_admin"))
    admin.add_view(EmpleadoDocumentoAdmin(EmpleadoDocumento, db.session, category="Personal", name="Documentos de empleados", endpoint="empleado_documento_admin"))
    admin.add_view(ParametroSARAdmin(ParametroSAR, db.session, name="Parámetros SAR", endpoint="parametros_sar_admin"))
    admin.add_view(OrdenEntregaAdmin(OrdenEntrega, db.session, category="Reparto", name="Órdenes de entrega", endpoint="orden_entrega_admin"))
    admin.add_view(OrdenesProveedoresAdmin(OrdenesProveedores, db.session, category="Órdenes", name="Órdenes a proveedores", endpoint="ordenes_proveedores_admin"))
    admin.add_view(OrdenesProveedoresDetalleAdmin(OrdenesProveedoresDetalle, db.session, category="Órdenes", name="Detalle órdenes proveedores", endpoint="ordenes_proveedores_detalle_admin"))
    admin.add_view(HistorialOrdenesRepartidorAdmin(HistorialOrdenesRepartidor, db.session, name="Historial de órdenes", endpoint="historial_ordenes_repartidor_admin", category=None))
    admin.add_view(HistorialOrdenesProveedoresAdmin(OrdenesProveedores, db.session, name="Historial órdenes proveedores", endpoint="historial_ordenes_proveedores_admin"))

    from models.panel_repartidor import panel_repartidor
    from models.panel_encargado import panel_encargado
    from models.usuario_cliente_routes import usuario_cliente_bp
    from models.mis_pedidos import mis_pedidos_bp
    from models.cancelar import cancelar_bp
    from models.password_reset_routes import password_reset_bp
    from models.pagina_principal import pagina_principal_bp
    from models.insumos import bp_insumos
    from models.crear_insumos import bp_crear_insumo
    from models.categoria_insumo import bp_categoria_insumo
    from models.crear_categoria_insumo import bp_crear_categoria_insumo
    from models.login_jefe_de_cocina import bp_login_jefe
    from models.panel_gerente import panel_gerente
    from models.panel_contador import panel_contador

    flask_app.register_blueprint(mis_pedidos_bp)
    flask_app.register_blueprint(cancelar_bp)
    flask_app.register_blueprint(panel_gerente)
    flask_app.register_blueprint(bp_login_jefe)
    flask_app.register_blueprint(bp_crear_categoria_insumo)
    flask_app.register_blueprint(bp_categoria_insumo)
    flask_app.register_blueprint(pagina_principal_bp)
    flask_app.register_blueprint(bp_insumos)
    flask_app.register_blueprint(bp_crear_insumo)
    flask_app.register_blueprint(panel_contador)
    flask_app.register_blueprint(usuario_cliente_bp)
    flask_app.register_blueprint(panel_repartidor)
    flask_app.register_blueprint(panel_encargado)
    flask_app.register_blueprint(password_reset_bp)

    from reports.routes import reports_bp

    flask_app.register_blueprint(reports_bp)

    from models.factura_routes import factura_routes
    from models.crear_recetas import crear_receta_routes, editar_receta_routes
    from models.gestion_recetas import gestion_receta_routes
    from models.crear_categoria_receta import crear_categoria_receta_routes
    from models.carrito_routes import carrito_routes
    from models.tusdirecciones import tus_direcciones_routes
    from models.crear_direcciones import crear_direcciones_routes
    from models.metodos_pago_routes import metodos_pago_routes

    factura_routes(flask_app)
    crear_receta_routes(flask_app)
    editar_receta_routes(flask_app)
    gestion_receta_routes(flask_app)
    crear_categoria_receta_routes(flask_app)
    carrito_routes(flask_app)
    tus_direcciones_routes(flask_app)
    crear_direcciones_routes(flask_app)
    metodos_pago_routes(flask_app)

    import models.login_crear_usuario

    return admin


@app.route("/")
def index():
    return redirect(url_for("pagina_principal_bp.menu"))


def _ensure_bootstrap():
    global _BOOTSTRAPPED
    if _BOOTSTRAPPED:
        return
    bootstrap_app(app)
    _BOOTSTRAPPED = True


if os.getenv("SKIP_BOOTSTRAP", "0").strip() != "1":
    _ensure_bootstrap()


if __name__ == "__main__":
    import pyodbc

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        print(cursor.fetchone())
        conn.close()
        print("Conexión ODBC directa correcta")
    except Exception as e:
        print("Error al conectar directamente con SQL Server:", e)

    debug = os.getenv("FLASK_DEBUG", "1").strip() == "1"
    app.run(debug=debug, use_reloader=False)
