import re
from models.admin_cai_view import CAIAdmin
import pytest
from sqlalchemy import text
import os
from Main import app as flask_app
from models import db

os.environ.setdefault("SKIP_DB_INIT", "1")
os.environ.setdefault("SKIP_BOOTSTRAP", "1")



def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


def _instancia_sin_init():
    return CAIAdmin.__new__(CAIAdmin)


def _assert_cai_normalizado(out):
    _require_db()
    assert out is not None
    assert out == out.upper()
    assert re.fullmatch(r"[A-Z0-9-]+", out) is not None
    compacto = out.replace("-", "")
    assert len(compacto) == 32
    assert compacto.isalnum() is True


def test_normalizar_cai_acepta_guiones_y_minusculas():
    _require_db()
    admin = _instancia_sin_init()
    raw = "abcd-1234-efgh-5678-ijkl-9012-mnop-3456"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)


def test_normalizar_cai_quita_simbolos():
    _require_db()
    admin = _instancia_sin_init()
    raw = "ABCD!1234@EFGH#5678$IJKL%9012^MNOP&3456"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)


def test_normalizar_cai_invalido_si_longitud_incorrecta():
    _require_db()
    admin = _instancia_sin_init()
    out = admin._normalizar_cai("ABCD1234")
    assert out is None


def test_normalizar_cai_none_devuelve_none():
    _require_db()
    admin = _instancia_sin_init()
    assert admin._normalizar_cai(None) is None


def test_normalizar_cai_vacio_devuelve_none():
    _require_db()
    admin = _instancia_sin_init()
    assert admin._normalizar_cai("") is None


def test_normalizar_cai_solo_espacios_devuelve_none():
    _require_db()
    admin = _instancia_sin_init()
    assert admin._normalizar_cai("   ") is None


def test_normalizar_cai_ya_normalizado_se_mantiene_en_formato():
    _require_db()
    admin = _instancia_sin_init()
    raw = "ABCD12-34EFGH-5678IJ-KL9012-MNOP34-56"
    out = admin._normalizar_cai(raw)
    assert out == raw


def test_normalizar_cai_acepta_muchos_separadores():
    _require_db()
    admin = _instancia_sin_init()
    raw = "ABCD-1234--EFGH---5678----IJKL-----9012------MNOP-------3456"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)


def test_normalizar_cai_acepta_tabs_y_saltos_de_linea():
    _require_db()
    admin = _instancia_sin_init()
    raw = "ABCD\t1234\nEFGH 5678\r\nIJKL 9012 MNOP 3456"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)


def test_normalizar_cai_invalido_si_tiene_caracteres_no_alfa_numericos():
    _require_db()
    admin = _instancia_sin_init()
    out = admin._normalizar_cai("ABCD1234EFGH5678IJKL9012MNOP345?")
    assert out is None


def test_normalizar_cai_invalido_si_le_faltan_caracteres_por_grupo():
    _require_db()
    admin = _instancia_sin_init()
    out = admin._normalizar_cai("ABC-1234-EFGH-5678-IJKL-9012-MNOP-3456")
    assert out is None


def test_normalizar_cai_recorta_si_le_sobran_caracteres():
    _require_db()
    admin = _instancia_sin_init()
    raw = "ABCD1234EFGH5678IJKL9012MNOP3456XXXX"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)


def test_normalizar_cai_guiones_raros_se_normaliza():
    _require_db()
    admin = _instancia_sin_init()
    raw = "-ABCD1234EFGH5678IJKL9012MNOP3456"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)


def test_normalizar_cai_invalido_si_no_alcanza_32_alfa_numericos():
    _require_db()
    admin = _instancia_sin_init()
    out = admin._normalizar_cai("ABCD1234EFGH5678IJKL9012MNOP345")
    assert out is None


def test_normalizar_cai_valido_sin_guiones_si_tiene_32_alfa_numericos():
    _require_db()
    admin = _instancia_sin_init()
    raw = "abcd1234efgh5678ijkl9012mnop3456"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)


def test_normalizar_cai_valido_con_mayus_y_minus_mix():
    _require_db()
    admin = _instancia_sin_init()
    raw = "AbCd-1234-eFgH-5678-IjKl-9012-mNoP-3456"
    out = admin._normalizar_cai(raw)
    _assert_cai_normalizado(out)