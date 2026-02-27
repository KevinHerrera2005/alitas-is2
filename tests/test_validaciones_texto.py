import pytest


def _capturador_flash(monkeypatch):
    import models.validaciones as v

    mensajes = []

    def fake_flash(msg, category="message"):
        mensajes.append((str(msg), str(category)))

    monkeypatch.setattr(v, "flash", fake_flash, raising=True)
    return v, mensajes


def test_sin_doble_espacio_colapsa_espacios():
    from models.validaciones import ValidadorTexto

    assert ValidadorTexto.sin_doble_espacio("hola   mundo") == "hola mundo"
    assert ValidadorTexto.sin_doble_espacio("  a    b   c  ") == " a b c "


@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("aaa", True),
        ("Holaaa", True),
        ("ssS", True),
        ("abca", False),
        ("aááá", True),
        ("Ñññ", True),
    ],
)
def test_tiene_tres_letras_iguales(texto, esperado):
    from models.validaciones import ValidadorTexto

    assert ValidadorTexto.tiene_tres_letras_iguales(texto) is esperado


def test_validar_nombre_acepta_nombre_simple(monkeypatch):
    v, mensajes = _capturador_flash(monkeypatch)

    assert v.ValidadorTexto.validar_nombre("Juan Perez", campo="Nombre") is True
    assert mensajes == []


def test_validar_nombre_rechaza_doble_espacio(monkeypatch):
    v, mensajes = _capturador_flash(monkeypatch)

    assert v.ValidadorTexto.validar_nombre("Juan  Perez", campo="Nombre") is False
    assert any("múltiples espacios" in m[0] for m in mensajes)


def test_validar_nombre_rechaza_tres_letras_iguales(monkeypatch):
    v, mensajes = _capturador_flash(monkeypatch)

    assert v.ValidadorTexto.validar_nombre("Juaaan", campo="Nombre") is False
    assert any("tres letras" in m[0] for m in mensajes)


def test_validar_nombre_rechaza_solo_numeros(monkeypatch):
    v, mensajes = _capturador_flash(monkeypatch)

    assert v.ValidadorTexto.validar_nombre("123456", campo="Nombre") is False
    assert any("solo números" in m[0] for m in mensajes)


def test_validar_descripcion_acepta_multilinea(monkeypatch):
    v, mensajes = _capturador_flash(monkeypatch)

    texto = "Linea uno\nLinea dos (ok)"
    assert v.ValidadorTexto.validar_descripcion(texto, campo="Descripción") is True
    assert mensajes == []


def test_validar_descripcion_rechaza_linea_vacia(monkeypatch):
    v, mensajes = _capturador_flash(monkeypatch)

    texto = "Linea uno\n\nLinea tres"
    assert v.ValidadorTexto.validar_descripcion(texto, campo="Descripción") is False
    assert any("líneas vacías" in m[0] for m in mensajes)
