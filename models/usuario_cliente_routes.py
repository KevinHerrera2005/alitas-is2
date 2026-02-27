from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.usuario_cliente_model import UsuarioCliente
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

usuario_cliente_bp = Blueprint("usuario_cliente", __name__)


@usuario_cliente_bp.route("/perfil")
@login_required
def perfil():
    cliente_id = getattr(current_user, "ID_Usuario_ClienteF", None)
    if not cliente_id:
        flash("No se encontró el usuario cliente asociado a tu sesión.", "danger")
        return redirect(url_for("login"))

    usuario = UsuarioCliente.query.get(cliente_id)
    if not usuario:
        flash("No se encontró el usuario cliente en la base de datos.", "danger")
        return redirect(url_for("login"))

    return render_template("perfil.html", usuario=usuario)


@usuario_cliente_bp.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    cliente_id = getattr(current_user, "ID_Usuario_ClienteF", None)
    if not cliente_id:
        flash("No se encontró el usuario cliente asociado a tu sesión.", "danger")
        return redirect(url_for("login"))

    usuario = UsuarioCliente.query.get(cliente_id)
    if not usuario:
        flash("No se encontró el usuario cliente en la base de datos.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        telefono = request.form.get("telefono", "").strip()

        if not nombre or not apellido or not telefono:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for("usuario_cliente.editar_perfil"))

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.telefono = telefono

        db.session.commit()
        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for("usuario_cliente.perfil"))

    return render_template("perfil_editar.html", usuario=usuario)
import re
from wtforms.validators import ValidationError


def _tiene_tres_iguales_seguidos(texto):
    if texto is None:
        return False
    s = str(texto)
    for i in range(len(s) - 2):
        if s[i] == s[i + 1] == s[i + 2]:
            return True
    return False


def validar_nombre_persona(valor):
    if valor is None:
        raise ValidationError("El nombre es obligatorio.")
    valor = str(valor).strip()
    if len(valor) < 3 or len(valor) > 40:
        raise ValidationError("El nombre debe tener entre 3 y 40 caracteres.")
    if any(ch.isdigit() for ch in valor):
        raise ValidationError("El nombre no puede contener números.")
    if _tiene_tres_iguales_seguidos(valor):
        raise ValidationError("El nombre no puede tener 3 caracteres iguales seguidos.")
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValidationError("El nombre no puede contener caracteres especiales.")
    return valor


def validar_apellido_persona(valor):
    if valor is None:
        raise ValidationError("El apellido es obligatorio.")
    valor = str(valor).strip()
    if len(valor) < 3 or len(valor) > 40:
        raise ValidationError("El apellido debe tener entre 3 y 40 caracteres.")
    if any(ch.isdigit() for ch in valor):
        raise ValidationError("El apellido no puede contener números.")
    if _tiene_tres_iguales_seguidos(valor):
        raise ValidationError("El apellido no puede tener 3 caracteres iguales seguidos.")
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValidationError("El apellido no puede contener caracteres especiales.")
    return valor


def validar_telefono_hn(valor):
    if valor is None:
        raise ValidationError("El teléfono es obligatorio.")
    valor = str(valor).strip()
    if not valor:
        raise ValidationError("El teléfono es obligatorio.")
    if not valor.isdigit():
        raise ValidationError("El teléfono debe contener solo dígitos.")
    if len(valor) != 8:
        raise ValidationError("El teléfono debe tener 8 dígitos.")
    if valor[0] not in ("3", "7", "8", "9"):
        raise ValidationError("El teléfono debe iniciar con 3, 7, 8 o 9.")
    return valor