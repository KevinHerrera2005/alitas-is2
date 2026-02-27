import os
import sys
import importlib
import pytest
from unittest.mock import patch


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(scope="session")
def app():
    os.environ["SKIP_DB_INIT"] = "1"
    os.environ["SKIP_BOOTSTRAP"] = "1"

    if "Main" in importlib.sys.modules:
        del importlib.sys.modules["Main"]
    if "models.login_crear_usuario" in importlib.sys.modules:
        del importlib.sys.modules["models.login_crear_usuario"]

    main_module = importlib.import_module("Main")
    app = main_module.app
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test"

    importlib.import_module("models.login_crear_usuario")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def _post_registro(client, **overrides):
    data = {
        "username": "usuario_test",
        "password": "Password1!",
        "confirmar": "Password1!",
        "nombre": "Kevin",
        "apellido": "Perez",
        "telefono": "98765432",
        "direccion": "Col. Centro",
        "correo": "nuevo@correo.com",
    }
    data.update(overrides)
    return client.post("/registro", data=data, follow_redirects=False)


def test_registro_falla_si_no_se_pone_usuario(client):
    resp = _post_registro(client, username="")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_usuario_es_espacios(client):
    resp = _post_registro(client, username="   ")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_usuario_tiene_caracteres_invalidos(client):
    resp = _post_registro(client, username="user-invalido")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_usuario_muy_corto(client):
    resp = _post_registro(client, username="ab")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_usuario_muy_largo(client):
    resp = _post_registro(client, username="a" * 21)
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_no_se_pone_contrasena(client):
    resp = _post_registro(client, password="", confirmar="")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_contrasena_no_cumple_formato_muy_corta(client):
    resp = _post_registro(client, password="Aa1!", confirmar="Aa1!")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_contrasena_sin_mayuscula(client):
    resp = _post_registro(client, password="password1!", confirmar="password1!")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_contrasena_sin_minuscula(client):
    resp = _post_registro(client, password="PASSWORD1!", confirmar="PASSWORD1!")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_contrasena_sin_numero(client):
    resp = _post_registro(client, password="Password!!", confirmar="Password!!")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_contrasena_sin_simbolo_permitido(client):
    resp = _post_registro(client, password="Password12", confirmar="Password12")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_telefono_no_tiene_8_digitos(client):
    resp = _post_registro(client, telefono="9876543")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


def test_registro_falla_si_telefono_no_inicia_con_3_7_8_9(client):
    resp = _post_registro(client, telefono="12345678")
    assert resp.status_code == 302
    assert "/registro" in (resp.headers.get("Location") or "")


import pytest

@pytest.mark.parametrize(
    "telefono_invalido",
    [
        "77777777",
        "aaaaaaaa",
        "1234abcd",
        "193210321321908",
        "99999999",
        "00000000",
        "11111111",
    ],
    ids=[
        "todos_iguales_7",
        "solo_letras",
        "mixto_num_letras",
        "demasiado_largo",
        "todos_iguales_9",
        "todos_iguales_0",
        "todos_iguales_1",
    ],
)
def test_registro_falla_si_telefono_invalido_redirecciona_a_registro(client, telefono_invalido):
    resp = _post_registro(client, telefono=telefono_invalido)
    assert resp.status_code == 302#para ver si la pagina hizo alguna acción para ver si me redireccionó o nada
    assert "/registro" in (resp.headers.get("Location") or "")#al haber un error me redirecciona al /registro para que vuelva a meter las cosas pero bien, entonces ve si me redireccionó a registro ya que si me dejara introducir esos datos entonces me redireccionaría al menu y esto daria un failed


def test_registro_pasa_unitario_sin_bd_envia_codigo(client):
    with patch("models.login_crear_usuario._correo_ya_registrado", return_value=False), \
         patch("models.login_crear_usuario._usuario_ya_existe", return_value=False), \
         patch("models.login_crear_usuario._enviar_codigo_confirmacion", return_value=(True, None)), \
         patch("models.login_crear_usuario.validar_datos_registro", return_value=None), \
         patch("models.login_crear_usuario.db.session.get") as mock_get:

        mock_get.return_value = type("E", (), {"ID_sucursal": 1})()

        resp = _post_registro(client)
        assert resp.status_code == 302
        assert "/registro/confirmar_correo" in (resp.headers.get("Location") or "")

