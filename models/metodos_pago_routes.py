import re
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from wtforms.validators import ValidationError

from models import db
from models.metodos_money_model import MetodosMoney
from models.pagos_cliente_model import PagosCliente


def _obtener_id_cliente():
    if current_user.is_authenticated and hasattr(current_user, "ID_Usuario_ClienteF"):
        return current_user.ID_Usuario_ClienteF
    return None


def metodos_pago_routes(app):
    @app.route("/tus_metodos_pago", methods=["GET"])
    @login_required
    def tus_metodos_pago():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            flash("No se pudo identificar el cliente.", "danger")
            return redirect(url_for("index"))

        tarjetas = (
            PagosCliente.query.join(MetodosMoney, PagosCliente.ID_Metodo == MetodosMoney.ID_Metodo)
            .filter(
                PagosCliente.ID_Usuario_ClienteF == id_cliente,
                MetodosMoney.Tipo == 2,
            )
            .all()
        )

        return render_template("tus_metodos_pago.html", tarjetas=tarjetas)

    @app.route("/metodos_pago/nuevo", methods=["GET", "POST"])
    @login_required
    def nuevo_metodo_pago():
        id_cliente = _obtener_id_cliente()
        if not id_cliente:
            flash("No se pudo identificar el cliente.", "danger")
            return redirect(url_for("index"))

        if request.method == "POST":
            try:
                nombre = validar_nombre_tarjeta(request.form.get("a_nombre_de"))
                numero_tarjeta = validar_numero_tarjeta(request.form.get("numero_tarjeta"))
            except ValidationError as e:
                flash(str(e), "danger")
                return redirect(url_for("nuevo_metodo_pago"))

            ultimos4 = numero_tarjeta[-4:]

            metodo_tarjeta = MetodosMoney.query.filter_by(Tipo=2).first()
            if not metodo_tarjeta:
                flash("No está configurado el método de pago 'Tarjeta'.", "danger")
                return redirect(url_for("tus_metodos_pago"))

            pago = PagosCliente(
                ID_Usuario_ClienteF=id_cliente,
                ID_Metodo=metodo_tarjeta.ID_Metodo,
                Cantidad=None,
                Numero_tarjeta=ultimos4,
                a_nombre_de=nombre[:50],
            )

            db.session.add(pago)
            db.session.commit()

            flash("Tarjeta guardada correctamente", "success")
            return redirect(url_for("tus_metodos_pago"))

        return render_template("metodo_pago_nuevo.html")


def _tiene_tres_iguales_seguidos(texto):
    if texto is None:
        return False
    s = str(texto)
    for i in range(len(s) - 2):
        if s[i] == s[i + 1] == s[i + 2]:
            return True
    return False


def validar_nombre_tarjeta(valor, min_len=3, max_len=50):
    if valor is None:
        raise ValidationError("El nombre en la tarjeta es obligatorio.")
    valor = str(valor).strip()
    if valor == "":
        raise ValidationError("El nombre en la tarjeta no puede estar vacío.")
    if len(valor) < min_len or len(valor) > max_len:
        raise ValidationError(f"El nombre en la tarjeta debe tener entre {min_len} y {max_len} caracteres.")
    if _tiene_tres_iguales_seguidos(valor):
        raise ValidationError("El nombre en la tarjeta no puede tener 3 letras iguales seguidas.")
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValidationError("El nombre en la tarjeta solo puede contener letras y espacios (sin números ni caracteres especiales).")
    return valor


def validar_numero_tarjeta(valor, min_len=4, max_len=19):
    if valor is None:
        raise ValidationError("El número de tarjeta es obligatorio.")
    valor = str(valor).replace(" ", "").strip()
    if valor == "":
        raise ValidationError("El número de tarjeta no puede estar vacío.")
    if not valor.isdigit():
        raise ValidationError("El número de tarjeta solo puede contener dígitos (0-9).")
    if len(valor) < min_len:
        raise ValidationError(f"Número de tarjeta inválido (debe tener al menos {min_len} dígitos).")
    if len(valor) > max_len:
        raise ValidationError(f"Número de tarjeta inválido (no puede superar {max_len} dígitos).")
    return valor