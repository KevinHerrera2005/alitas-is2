import pytest
from sqlalchemy import text

from Main import app as flask_app
from models import db
from models.receta_model import Receta
from models.in_re_model import IN_RE
from models.admin_recetas_view import (
    validar_nombre_receta,
    validar_pasos_receta,
    validar_estado_receta,
    categoria_receta_existe_db,
)


def _require_db():
    with flask_app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            pytest.fail(f"SQL Server no accesible para tests: {type(e).__name__}: {e}")


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        "12",
        "aa",
        "pizaaa",
        "@Pizza",
        "Pizza#1",
        "Este nombre es demasiado largo para receta",
    ],
)
def test_validar_nombre_receta_invalido(raw):
    _require_db()
    assert validar_nombre_receta(raw) is None


@pytest.mark.parametrize(
    "raw,esperado",
    [
        ("  Pizza Suprema  ", "Pizza Suprema"),
        ("Alitas+BBQ", "Alitas+BBQ"),
        ("Postre=Flan", "Postre=Flan"),
    ],
)
def test_validar_nombre_receta_valido(raw, esperado):
    _require_db()
    assert validar_nombre_receta(raw) == esperado


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "   ",
        " Pasos",
        "Paso\n\nPaso 2",
        "aa",
        "Paso @",
    ],
)
def test_validar_pasos_receta_invalido(raw):
    _require_db()
    assert validar_pasos_receta(raw) is None


def test_validar_pasos_receta_valido_multilinea():
    _require_db()
    raw = "1) Preparar salsa\n2) Cocinar alitas\n3) Mezclar y servir"
    out = validar_pasos_receta(raw)
    assert out == raw


@pytest.mark.parametrize(
    "raw,esperado",
    [
        (None, 1),
        ("", 1),
        ("1", 1),
        (1, 1),
        (0, 0),
        ("0", 0),
        (2, 0),
        (-1, 0),
    ],
)
def test_validar_estado_receta(raw, esperado):
    _require_db()
    assert validar_estado_receta(raw) == esperado


def test_categoria_receta_debe_existir_en_bd():
    _require_db()
    with flask_app.app_context():
        rid = db.session.execute(text("SELECT TOP 1 id_categoria_receta FROM categoria_recetas ORDER BY id_categoria_receta"))
        row = rid.fetchone()
        if not row:
            pytest.fail("No hay categorías de recetas en la BD para validar selección de categoría.")
        assert categoria_receta_existe_db(int(row[0])) is True


def test_recetas_deben_existir_en_bd():
    _require_db()
    with flask_app.app_context():
        total = Receta.query.count()
        assert total > 0


def test_editar_receta_persiste_nombre_y_estado():
    _require_db()
    with flask_app.app_context():
        receta = Receta.query.order_by(Receta.ID_Receta).first()
        if not receta:
            pytest.fail("No hay recetas en la BD para probar edición.")

        nombre_original = receta.Nombre_receta
        estado_original = receta.Estado

        nuevo_nombre = validar_nombre_receta("Receta Test")
        assert nuevo_nombre is not None

        receta.Nombre_receta = nuevo_nombre
        receta.Estado = 0 if int(estado_original) == 1 else 1
        db.session.commit()
        db.session.refresh(receta)

        assert receta.Nombre_receta == "Receta Test"
        assert receta.Estado in (0, 1)
        assert receta.Estado != estado_original

        receta.Nombre_receta = nombre_original
        receta.Estado = estado_original
        db.session.commit()


def test_guardar_insumo_editado_persiste_cambio():
    _require_db()
    with flask_app.app_context():
        row = db.session.execute(
            text("SELECT TOP 1 ID_IN_RE, cantidad_usada FROM IN_RE ORDER BY ID_IN_RE")
        ).mappings().first()

        if not row:
            pytest.fail("No hay insumos asociados a recetas (IN_RE) para probar edición.")

        in_re_id = row["ID_IN_RE"]
        original = row["cantidad_usada"]
        if original is None:
            original = 0

        nuevo = float(original) + 1

        db.session.execute(
            text("UPDATE IN_RE SET cantidad_usada = :nuevo WHERE ID_IN_RE = :id"),
            {"nuevo": nuevo, "id": in_re_id},
        )
        db.session.commit()

        ver = db.session.execute(
            text("SELECT cantidad_usada FROM IN_RE WHERE ID_IN_RE = :id"),
            {"id": in_re_id},
        ).scalar()

        assert float(ver) == pytest.approx(nuevo)

        db.session.execute(
            text("UPDATE IN_RE SET cantidad_usada = :orig WHERE ID_IN_RE = :id"),
            {"orig": original, "id": in_re_id},
        )
        db.session.commit()


