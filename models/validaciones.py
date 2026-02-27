
import re
from flask import flash, redirect, url_for
from models.usuario_cliente_model import UsuarioCliente as Usuario

def validar_datos_registro(username, password, nombre, apellido, telefono, direccion,
                           metodo_pago=None, numero_tarjeta=None):
    """Valida todos los campos del formulario de registro de usuario."""

    if not all([username, password, nombre, apellido, telefono, direccion]):
        flash("Completa todos los campos obligatorios.", "danger")
        return redirect(url_for("registro"))

    def validar_nombre_campo(campo, tipo):
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$", campo):
            flash(f"El {tipo} solo puede contener letras y espacios.", "danger")
            return False
        if len(campo) < 2 or len(campo) > 30:
            flash(f"El {tipo} debe tener entre 2 y 30 caracteres.", "danger")
            return False
        if re.search(r"(.)\1\1", campo):
            flash(f"El {tipo} no puede tener tres letras consecutivas iguales.", "danger")
            return False
        if re.search(r" {2,}", campo):
            flash(f"El {tipo} no puede contener múltiples espacios seguidos.", "danger")
            return False
        if not re.match(r"^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)( [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*$", campo):
            flash(f"Cada palabra del {tipo} debe iniciar con mayúscula.", "danger")
            return False
        return True

    if not validar_nombre_campo(nombre.strip(), "nombre"):
        return redirect(url_for("registro"))
    if not validar_nombre_campo(apellido.strip(), "apellido"):
        return redirect(url_for("registro"))

    nombre = " ".join([p.capitalize() for p in nombre.split()])
    apellido = " ".join([p.capitalize() for p in apellido.split()])

    if "  " in username:
        flash("El nombre de usuario no puede contener espacios múltiples.", "danger")
        return redirect(url_for("registro"))

    if not (3 <= len(username) <= 16):
        flash("El nombre de usuario debe tener entre 3 y 16 caracteres.", "danger")
        return redirect(url_for("registro"))

    if not re.match(r"^[A-Za-z0-9_]+$", username):
        flash("El usuario solo puede contener letras, números o guiones bajos.", "danger")
        return redirect(url_for("registro"))

    usuario_existente = Usuario.query.filter_by(Username=username).first()
    if usuario_existente:
        flash("Este usuario ya existe. Por favor elige otro.", "danger")
        return redirect(url_for("registro"))

    if not telefono.isdigit():
        flash("El número de teléfono solo puede contener números.", "danger")
        return redirect(url_for("registro"))

    if len(telefono) != 8:
        flash("El número de teléfono debe tener exactamente 8 dígitos.", "danger")
        return redirect(url_for("registro"))

    if telefono[0] not in ["3", "7", "8", "9"]:
        flash("El número de teléfono debe comenzar con 3, 7, 8 o 9.", "danger")
        return redirect(url_for("registro"))

    if len(direccion) < 5 or len(direccion) > 100:
        flash("La dirección debe tener entre 5 y 100 caracteres.", "danger")
        return redirect(url_for("registro"))

    if re.search(r"[!@#$%^&*()_=+{}\[\]<>?/|\\;:\"'`~]", direccion):
        flash("La dirección contiene caracteres especiales no permitidos.", "danger")
        return redirect(url_for("registro"))

    if len(password) < 10:
        flash("La contraseña debe tener al menos 10 caracteres.", "warning")
        return redirect(url_for("registro"))
    if not re.search(r"[A-Z]", password):
        flash("La contraseña debe contener al menos una letra mayúscula.", "warning")
        return redirect(url_for("registro"))
    if not re.search(r"[a-z]", password):
        flash("La contraseña debe contener al menos una letra minúscula.", "warning")
        return redirect(url_for("registro"))
    if not re.search(r"\d", password):
        flash("La contraseña debe contener al menos un número.", "warning")
        return redirect(url_for("registro"))
    if not re.search(r"[^A-Za-z0-9]", password):
        flash("La contraseña debe contener al menos un símbolo (ej: !@#$%).", "warning")
        return redirect(url_for("registro"))

    if metodo_pago in ["efectivo", "mixto"]:
        numero_tarjeta = None

    return None


class ValidadorTexto:
    """Valida nombres y descripciones generales (usado en admin, recetas, etc)."""

    @staticmethod
    def sin_doble_espacio(valor: str) -> str:
        """✔ Elimina espacios dobles consecutivos."""
        return re.sub(r"\s{2,}", " ", valor)

    @staticmethod
    def tiene_tres_letras_iguales(valor: str) -> bool:
        """❌ Detecta si hay tres letras consecutivas iguales (ej: aaa, sss)."""
        return bool(re.search(r"([a-záéíóúñ])\1\1", valor.lower()))

    @staticmethod
    def validar_nombre(valor: str, campo: str = "Nombre"):
        limpio = valor.strip()

        if limpio.startswith(" "):
            flash(f"El {campo} no puede iniciar con espacio.", "danger")
            return False
        if re.search(r" {2,}", limpio):
            flash(f"El {campo} no puede tener múltiples espacios seguidos.", "danger")
            return False

        if re.match(r"^[0-9]+$", limpio) or re.match(r"^[^A-Za-zÁÉÍÓÚáéíóúÑñ0-9]+$", limpio):
            flash(f"El {campo} no puede ser solo números o símbolos.", "danger")
            return False

        if not (3 <= len(re.sub(r'\s+', '', limpio)) <= 20):
            flash(f"El {campo} debe tener entre 3 y 20 caracteres válidos.", "danger")
            return False

        if ValidadorTexto.tiene_tres_letras_iguales(limpio):
            flash(f"El {campo} no puede tener tres letras iguales seguidas.", "danger")
            return False

        if not re.match(r"^[A-Za-z0-9 +=ÁÉÍÓÚáéíóúÑñ]+( [A-Za-z0-9 +=ÁÉÍÓÚáéíóúÑñ]+)*$", limpio):
            flash(f"El {campo} solo puede tener letras, números y los símbolos + =.", "danger")
            return False

        return True

    @staticmethod
    def validar_descripcion(valor: str, campo: str = "Descripción"):
        if re.match(r"^[ \n]", valor):
            flash(f"La {campo} no puede iniciar con espacio o salto de línea.", "danger")
            return False
        if re.search(r" {2,}", valor):
            flash(f"La {campo} no puede tener múltiples espacios seguidos.", "danger")
            return False

        lineas = valor.split("\n")
        for i, linea in enumerate(lineas, 1):
            texto = linea.strip()
            if texto == "":
                flash(f"No se permiten líneas vacías en la {campo} (línea {i}).", "danger")
                return False
            if len(re.sub(r"\s+", "", texto)) < 3:
                flash(f"Cada línea debe tener al menos 3 caracteres válidos (línea {i}).", "danger")
                return False
            if ValidadorTexto.tiene_tres_letras_iguales(texto):
                flash(f"No puede tener tres letras seguidas iguales (línea {i}).", "danger")
                return False
            if not re.match(r"^[A-Za-z0-9 +=:,().ÁÉÍÓÚáéíóúÑñ]+$", texto):
                flash(f"Caracteres no válidos en la línea {i} de la {campo}.", "danger")
                return False

        sin_espacios = valor.replace(" ", "")
        if not (3 <= len(sin_espacios) <= 200):
            flash(f"La {campo} debe tener entre 3 y 200 caracteres válidos.", "danger")
            return False

        return True
def validarFechafinal(fecha_emision, fecha_final):
    """
    Valida que la fecha final no sea anterior a la fecha de emisión.
    Devuelve un mensaje de error (str) o None si todo está bien.
    """
    if not fecha_emision or not fecha_final:
        return "Debes ingresar la fecha de emisión y la fecha final."

    if fecha_final < fecha_emision:
        return "La fecha final no puede ser anterior a la fecha de emisión."

    return None


def validarRangos(rango_inicial, rango_final):
    """
    Valida que el rango inicial sea menor que el rango final.
    Devuelve un mensaje de error (str) o None si todo está bien.
    """
    try:
        ri = int(rango_inicial)
        rf = int(rango_final)
    except (TypeError, ValueError):
        return "Los rangos deben ser números enteros."

    if ri >= rf:
        return "El rango inicial debe ser menor que el rango final."

    return None