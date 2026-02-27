import os
import sys
import importlib
import pytest
from unittest.mock import patch
from email import message_from_string


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _extract_text_plain_from_raw_email(raw_msg):
    msg = message_from_string(raw_msg)
    parts_text = []

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True) or b""
                charset = part.get_content_charset() or "utf-8"
                parts_text.append(payload.decode(charset, errors="ignore"))
    else:
        payload = msg.get_payload(decode=True) or b""
        charset = msg.get_content_charset() or "utf-8"
        parts_text.append(payload.decode(charset, errors="ignore"))

    return "\n".join(parts_text)


@pytest.fixture
def main_module():
    os.environ["SKIP_DB_INIT"] = "1"
    os.environ["SKIP_BOOTSTRAP"] = "1"

    if "Main" in importlib.sys.modules:
        del importlib.sys.modules["Main"]

    return importlib.import_module("Main")


def test_enviar_codigo_confirmacion_envia_y_contiene_codigo(main_module):
    app = main_module.app

    with app.app_context():
        app.config["GMAIL_USER"] = "test@gmail.com"
        app.config["GMAIL_PASSWORD"] = "app_password"

        destino = "destino@correo.com"
        codigo = "123456"

        with patch("Main.smtplib.SMTP_SSL") as mock_smtp:
            ok, err = main_module.enviar_codigo_confirmacion(destino, codigo)

            assert ok is True
            assert err is None

            servidor = mock_smtp.return_value.__enter__.return_value
            servidor.sendmail.assert_called_once()

            raw_msg = servidor.sendmail.call_args[0][2]
            body = _extract_text_plain_from_raw_email(raw_msg)
            assert codigo in body


def test_enviar_codigo_confirmacion_falla_si_falta_config(main_module):
    app = main_module.app
    with app.app_context():
        app.config["GMAIL_USER"] = ""
        app.config["GMAIL_PASSWORD"] = ""

        ok, err = main_module.enviar_codigo_confirmacion("destino@correo.com", "123456")
        assert ok is False
        assert err is not None


def test_registrar_y_validar_codigo(main_module):
    destino = "destino@correo.com"
    codigo = "999999"

    ok_reg = main_module.registrar_codigo_confirmacion(destino, codigo, ttl_seconds=60)
    assert ok_reg is True

    ok_bad = main_module.validar_codigo_confirmacion(destino, "000000")
    assert ok_bad is False

    ok_good = main_module.validar_codigo_confirmacion(destino, codigo)
    assert ok_good is True

    ok_reuse = main_module.validar_codigo_confirmacion(destino, codigo)
    assert ok_reuse is False


def test_registrar_codigo_falla_si_codigo_none_o_espacios(main_module):
    assert main_module.registrar_codigo_confirmacion("destino@correo.com", None, ttl_seconds=60) is False
    assert main_module.registrar_codigo_confirmacion("destino@correo.com", "   ", ttl_seconds=60) is False


def test_validar_codigo_falla_si_codigo_none_o_espacios(main_module):
    assert main_module.validar_codigo_confirmacion("destino@correo.com", None) is False
    assert main_module.validar_codigo_confirmacion("destino@correo.com", "   ") is False


def test_enviar_y_registrar_codigo(main_module):
    app = main_module.app
    with app.app_context():
        app.config["GMAIL_USER"] = "test@gmail.com"
        app.config["GMAIL_PASSWORD"] = "app_password"

        destino = "destino@correo.com"
        codigo = "222222"

        with patch("Main.smtplib.SMTP_SSL") as mock_smtp:
            servidor = mock_smtp.return_value.__enter__.return_value
            servidor.login.return_value = None
            servidor.sendmail.return_value = None

            ok, err = main_module.enviar_y_registrar_codigo_confirmacion(destino, codigo, ttl_seconds=60)
            assert ok is True
            assert err is None

        assert main_module.validar_codigo_confirmacion(destino, codigo) is True

import pyodbc

def test_db_conectada_select_1_real(main_module):
    conn_str = main_module.connection_string
    try:
        conn = pyodbc.connect(conn_str, timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        row = cur.fetchone()
        conn.close()
    except Exception as e:
        pytest.fail(f"la base de datos está apagada o sin acceso: {e}")

    assert row is not None
    assert row[0] == 1