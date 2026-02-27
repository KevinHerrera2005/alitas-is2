import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secrets import randbelow
import re

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from sqlalchemy import func

from models import db
from models.usuario_cliente_model import UsuarioCliente


password_reset_bp = Blueprint("password_reset", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _col_email_usuario_cliente():
    for name in ("correo", "Correo", "email", "Email"):
        col = getattr(UsuarioCliente, name, None)
        if col is not None:
            return col
    return None


def _buscar_cliente_por_email(email: str):
    col = _col_email_usuario_cliente()
    if col is None:
        return None
    return UsuarioCliente.query.filter(func.lower(col) == func.lower(email)).first()


def _generar_codigo_6():
    return f"{randbelow(1000000):06d}"


def _enviar_codigo_por_correo(destino: str, codigo: str):
    remitente = (current_app.config.get("GMAIL_USER") or "").strip()
    clave = (current_app.config.get("GMAIL_PASSWORD") or "").strip()

    if not remitente or not clave:
        raise RuntimeError("Falta configurar GMAIL_USER o GMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["Subject"] = "Código de verificación - Recuperar contraseña"
    msg["From"] = remitente
    msg["To"] = destino
    msg.attach(MIMEText(f"Tu código de verificación es: {codigo}", "plain", "utf-8"))

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto, timeout=20) as servidor:
        servidor.login(remitente, clave)
        servidor.sendmail(remitente, [destino], msg.as_string())


@password_reset_bp.route("/recuperar-contrasena", methods=["GET", "POST"])
def solicitar_reset():
    if request.method == "GET":
        return render_template("ingresar_correo.html")

    email = (request.form.get("email") or "").strip()
    if not email or not EMAIL_RE.match(email):
        flash("Ingresa un correo válido.", "danger")
        return render_template("ingresar_correo.html")

    cliente = _buscar_cliente_por_email(email)
    if not cliente:
        flash("lo siento no podemos encontrar tu gmail", "danger")
        return render_template("ingresar_correo.html")

    codigo = _generar_codigo_6()
    session["reset_password_email"] = email
    session["reset_password_code"] = codigo
    session["reset_password_verified"] = False

    try:
        _enviar_codigo_por_correo(email, codigo)
    except Exception:
        flash("No se pudo enviar el código. Intenta de nuevo.", "danger")
        return render_template("ingresar_correo.html")

    return redirect(url_for("password_reset.confirmar_codigo"))


@password_reset_bp.route("/recuperar-contrasena/confirmar", methods=["GET", "POST"])
def confirmar_codigo():
    email = (session.get("reset_password_email") or "").strip()
    codigo_guardado = (session.get("reset_password_code") or "").strip()

    if not email or not codigo_guardado:
        flash("Primero ingresa tu correo para enviarte el código.", "danger")
        return redirect(url_for("password_reset.solicitar_reset"))

    if request.method == "GET":
        return render_template("confirmar_codigo_reset.html")

    codigo = (request.form.get("codigo") or "").strip()
    if codigo != codigo_guardado:
        flash("El código introducido no es el correcto.", "danger")
        return render_template("confirmar_codigo_reset.html")

    session["reset_password_verified"] = True
    return redirect(url_for("password_reset.nueva_contrasena"))


@password_reset_bp.route("/recuperar-contrasena/nueva", methods=["GET", "POST"])
def nueva_contrasena():
    email = (session.get("reset_password_email") or "").strip()
    ok = bool(session.get("reset_password_verified"))

    if not email or not ok:
        flash("Primero confirma el código enviado a tu correo.", "danger")
        return redirect(url_for("password_reset.solicitar_reset"))

    if request.method == "GET":
        return render_template("nueva_contrasena.html")

    password = (request.form.get("password") or "").strip()
    confirmar = (request.form.get("confirmar") or "").strip()

    if not password or len(password) < 6:
        flash("La contraseña debe tener al menos 6 caracteres.", "danger")
        return render_template("nueva_contrasena.html")

    if password != confirmar:
        flash("Las contraseñas no coinciden.", "danger")
        return render_template("nueva_contrasena.html")

    cliente = _buscar_cliente_por_email(email)
    if not cliente:
        flash("lo siento no podemos encontrar tu gmail", "danger")
        return redirect(url_for("password_reset.solicitar_reset"))

    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt(current_app)
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")

    if hasattr(cliente, "password"):
        cliente.password = hashed
    elif hasattr(cliente, "Password"):
        setattr(cliente, "Password", hashed)
    else:
        flash("No se encontró el campo de contraseña en el modelo.", "danger")
        return render_template("nueva_contrasena.html")

    db.session.add(cliente)
    db.session.commit()

    session.pop("reset_password_email", None)
    session.pop("reset_password_code", None)
    session.pop("reset_password_verified", None)

    flash("Contraseña actualizada. Ahora inicia sesión.", "success")
    return redirect(url_for("login"))
