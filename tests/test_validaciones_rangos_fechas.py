from datetime import date

import pytest


@pytest.mark.parametrize(
    "emision,final,esperado",
    [
        (None, date(2026, 1, 1), "Debes ingresar"),
        (date(2026, 1, 1), None, "Debes ingresar"),
        (date(2026, 1, 2), date(2026, 1, 1), "no puede ser anterior"),
        (date(2026, 1, 1), date(2026, 1, 1), None),
        (date(2026, 1, 1), date(2026, 1, 2), None),
    ],
)
def test_validar_fechafinal(emision, final, esperado):
    from models.validaciones import validarFechafinal

    out = validarFechafinal(emision, final)
    if esperado is None:
        assert out is None
    else:
        assert isinstance(out, str)
        assert esperado in out


@pytest.mark.parametrize(
    "ri,rf,esperado",
    [
        ("1", "2", None),
        (1, 2, None),
        ("2", "2", "menor"),
        ("3", "2", "menor"),
        (None, "2", "números enteros"),
        ("a", "2", "números enteros"),
    ],
)
def test_validar_rangos(ri, rf, esperado):
    from models.validaciones import validarRangos

    out = validarRangos(ri, rf)
    if esperado is None:
        assert out is None
    else:
        assert isinstance(out, str)
        assert esperado in out
