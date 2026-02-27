from flask import render_template, request, redirect, url_for, flash, session
from Main import app, db, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, logout_user, login_required
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from models.validaciones import validar_datos_registro
from models.empleado_model import Empleado
from models.gerente_model import Gerente
from models.direccion_model import Direccion
from models.usuario_cliente_model import UsuarioCliente as ClienteModel
from models.direccion_cliente_model import DireccionDelCliente
from models.metodo_pago_model import MetodoPago

bcrypt = Bcrypt(app)


class UserLogin(UserMixin):
    def __init__(self, tipo, db_id, nombre, id_puesto=None, id_sucursal=None):
        self.tipo = tipo
        self.db_id = db_id
        self.nombre = nombre
        self.id_puesto = id_puesto
        self.id_sucursal = id_sucursal
        self.ID_sucursal = id_sucursal

        if self.tipo == "cliente":
            self.ID_Usuario_ClienteF = db_id
        elif self.tipo == "empleado":
            self.ID_Empleado = db_id
            self.ID_Puesto = id_puesto
        elif self.tipo == "gerente":
            self.ID_gerente = db_id

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


@login_manager.user_loader
def load_user(user_id):
    try:
        pref, real_id = user_id.split("-", 1)
        real_id = int(real_id)
    except Exception:
        return None

    if pref == "G":
        g = Gerente.query.get(real_id)
        if not g:
            return None
        return UserLogin(
            tipo="gerente",
            db_id=g.ID_gerente,
            nombre=g.Username,
            id_sucursal=getattr(g, "ID_sucursal", None) or getattr(g, "id_sucursal", None),
        )

    if pref == "E":
        empleado = Empleado.query.get(real_id)
        if not empleado:
            return None
        return UserLogin(
            tipo="empleado",
            db_id=empleado.ID_Empleado,
            nombre=empleado.Nombre,
            id_puesto=empleado.ID_Puesto,
            id_sucursal=getattr(empleado, "ID_sucursal", None) or getattr(empleado, "id_sucursal", None),
        )

    if pref == "C":
        usuario = ClienteModel.query.get(real_id)
        if not usuario:
            return None
        return UserLogin(
            tipo="cliente",
            db_id=usuario.ID_Usuario_ClienteF,
            nombre=usuario.nombre,
            id_sucursal=getattr(usuario, "ID_sucursal", None) or getattr(usuario, "id_sucursal", None),
        )

    return None


def _enviar_codigo_confirmacion(destino: str, codigo: str):
    remitente = (app.config.get("GMAIL_USER") or "").strip()
    clave = (app.config.get("GMAIL_PASSWORD") or "").strip()

    if not remitente or not clave:
        return False, "Falta configurar GMAIL_USER o GMAIL_PASSWORD"
    if not destino:
        return False, "Correo destino inválido"

    asunto = "Código de confirmación - Alitas El Comelón"
    cuerpo = f"Tu código de confirmación es: {codigo}"

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
        return False, "Gmail rechazó la autenticación (usa App Password)"
    except Exception:
        return False, "No se pudo enviar el correo"


def _correo_ya_registrado(correo: str) -> bool:
    if not correo:
        return False
    row = db.session.execute(
        text("SELECT 1 FROM Usuarios_cliente WHERE correo = :c"),
        {"c": correo},
    ).first()
    return bool(row)


def _usuario_ya_existe(username: str) -> bool:
    if not username:
        return False
    return bool(ClienteModel.query.filter_by(Username=username).first())


def _correo_valido(correo: str) -> bool:
    correo = (correo or "").strip()
    if not correo:
        return False
    if "@" not in correo:
        return False
    if "." not in correo.split("@")[-1]:
        return False
    return True


def _crear_direccion_safe(texto_direccion: str):
    texto_direccion = (texto_direccion or "").strip()
    if not texto_direccion:
        raise ValueError("Dirección vacía")

    posibles = ["descripcion", "Descripcion", "direccion", "Direccion", "detalle", "Detalle"]
    columnas = set(getattr(Direccion, "__table__").columns.keys())

    campo = None
    for c in posibles:
        if c in columnas:
            campo = c
            break

    if not campo:
        raise TypeError(
            f"El modelo Direccion no tiene un campo para texto de dirección. Columnas disponibles: {sorted(columnas)}"
        )

    obj = Direccion()
    setattr(obj, campo, texto_direccion)
    return obj


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        g = Gerente.query.filter_by(Username=username).first()
        if g and g.Password == password:
            user = UserLogin(
                tipo="gerente",
                db_id=g.ID_gerente,
                nombre=g.Username,
                id_sucursal=getattr(g, "ID_sucursal", None) or getattr(g, "id_sucursal", None),
            )
            login_user(user)
            session.pop("cliente_id", None)
            return redirect(url_for("panel_gerente.panel"))

        empleado = Empleado.query.filter_by(Username=username).first()
        if empleado and empleado.Password == password:
            user = UserLogin(
                tipo="empleado",
                db_id=empleado.ID_Empleado,
                nombre=empleado.Nombre,
                id_puesto=empleado.ID_Puesto,
                id_sucursal=getattr(empleado, "ID_sucursal", None) or getattr(empleado, "id_sucursal", None),
            )
            login_user(user)
            session.pop("cliente_id", None)

            if empleado.ID_Puesto == 1:
                return redirect(url_for("login_jefe.panel_jefe"))
            if empleado.ID_Puesto == 10:
                return redirect(url_for("panel_contador.panel"))
            if empleado.ID_Puesto == 4:
                return redirect(url_for("panel_repartidor.panel"))
            if empleado.ID_Puesto == 14:
                return redirect(url_for("panel_encargado.panel"))
            if empleado.ID_Puesto == 16:
                return redirect(url_for("panel_gerente.panel"))

            return redirect(url_for("pagina_principal_bp.menu"))

        usuario = ClienteModel.query.filter_by(Username=username).first()
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            user = UserLogin(
                tipo="cliente",
                db_id=usuario.ID_Usuario_ClienteF,
                nombre=usuario.nombre,
                id_sucursal=getattr(usuario, "ID_sucursal", None) or getattr(usuario, "id_sucursal", None),
            )
            login_user(user)
            session["cliente_id"] = usuario.ID_Usuario_ClienteF
            return redirect(url_for("pagina_principal_bp.menu"))

        flash("Usuario o contraseña equivocados", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("cliente_id", None)
    session.pop("registro_pendiente", None)
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()
        confirmar = (request.form.get("confirmar") or "").strip()
        nombre = (request.form.get("nombre") or "").strip()
        apellido = (request.form.get("apellido") or "").strip()
        telefono = (request.form.get("telefono") or "").strip()
        direccion = (request.form.get("direccion") or "").strip()
        correo = (request.form.get("correo") or "").strip()

        if not _correo_valido(correo):
            flash("Correo inválido.", "danger")
            return redirect(url_for("registro"))

        if _usuario_ya_existe(username):
            flash("Ese usuario ya existe.", "danger")
            return redirect(url_for("registro"))

        if _correo_ya_registrado(correo):
            flash("Ese gmail ya está creado.", "danger")
            return redirect(url_for("registro"))

        if password != confirmar:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for("registro"))

        error = validar_datos_registro(
            username,
            password,
            nombre,
            apellido,
            telefono,
            direccion,
            None,
            None,
        )
        if error:
            return error

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        empleado_web = db.session.get(Empleado, 20)
        if empleado_web and getattr(empleado_web, "ID_sucursal", None) is not None:
            id_sucursal_web = empleado_web.ID_sucursal
        else:
            id_sucursal_web = 1

        codigo = str(secrets.randbelow(9000) + 1000)

        ok, err = _enviar_codigo_confirmacion(correo, codigo)
        if not ok:
            flash(f"No se pudo enviar el correo: {err}", "danger")
            return redirect(url_for("registro"))

        session["registro_pendiente"] = {
            "Username": username,
            "password": hashed,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "direccion": direccion,
            "correo": correo,
            "ID_sucursal": int(id_sucursal_web),
            "codigo": codigo,
        }

        return redirect(url_for("confirmar_correo"))

    return render_template("registro.html")


@app.route("/registro/confirmar_correo", methods=["GET", "POST"])
def confirmar_correo():
    pendiente = session.get("registro_pendiente")
    if not pendiente:
        flash("No hay un registro pendiente. Vuelve a registrarte.", "danger")
        return redirect(url_for("registro"))

    if request.method == "POST":
        codigo = (request.form.get("codigo") or "").strip()

        if codigo != str(pendiente.get("codigo")):
            flash("El código introducido no es el correcto.", "danger")
            return render_template("confirmar_correo.html")

        if _correo_ya_registrado(pendiente.get("correo", "")):
            session.pop("registro_pendiente", None)
            flash("Ese gmail ya está creado.", "danger")
            return redirect(url_for("registro"))

        try:
            nuevo_usuario = ClienteModel(
                Username=pendiente["Username"],
                password=pendiente["password"],
                nombre=pendiente["nombre"],
                apellido=pendiente["apellido"],
                telefono=pendiente["telefono"],
                ID_sucursal=pendiente["ID_sucursal"],
                estado=1,
            )

            if hasattr(ClienteModel, "correo"):
                setattr(nuevo_usuario, "correo", pendiente["correo"])

            db.session.add(nuevo_usuario)
            db.session.flush()

            direccion_base = _crear_direccion_safe(pendiente["direccion"])
            db.session.add(direccion_base)
            db.session.flush()

            nueva_direccion = DireccionDelCliente(
                ID_Usuario_ClienteF=nuevo_usuario.ID_Usuario_ClienteF,
                ID_Direccion=direccion_base.ID_Direccion,
            )
            db.session.add(nueva_direccion)

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            session.pop("registro_pendiente", None)
            flash("Ese gmail o usuario ya está creado.", "danger")
            return redirect(url_for("registro"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear la cuenta: {e}", "danger")
            return redirect(url_for("registro"))

        user = UserLogin(
            tipo="cliente",
            db_id=nuevo_usuario.ID_Usuario_ClienteF,
            nombre=nuevo_usuario.nombre,
            id_sucursal=getattr(nuevo_usuario, "ID_sucursal", None) or getattr(nuevo_usuario, "id_sucursal", None),
        )
        login_user(user)
        session["cliente_id"] = nuevo_usuario.ID_Usuario_ClienteF
        session.pop("registro_pendiente", None)

        return redirect(url_for("pagina_principal_bp.menu"))

    return render_template("confirmar_correo.html")
