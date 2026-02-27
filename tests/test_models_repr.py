from models.direccion_cliente_model import DireccionDelCliente
from models.orden_entrega_model import OrdenEntrega

from models.categoria_insumo_model import CategoriaInsumo
from models.unidades_medida_model import Unidades_medida
from models.direccion_model import Direccion
from models.metodos_money_model import MetodosMoney


def test_repr_categoria_insumo_devuelve_nombre():
    obj = CategoriaInsumo(Nombre_categoria="Bebidas", descripcion="x", estado=1, tipo=1)
    assert repr(obj) == "Bebidas"


def test_repr_unidades_medida_devuelve_nombre():
    obj = Unidades_medida(Nombre="Kilogramo", abreviatura="kg", Tipo=1)
    assert repr(obj) == "Kilogramo"


def test_repr_direccion_incluye_id_y_descripcion():
    obj = Direccion(ID_Direccion=10, Descripcion="Barrio Centro")
    out = repr(obj)
    assert "10" in out
    assert "Barrio Centro" in out


def test_repr_metodos_money_incluye_id_nombre_y_tipo():
    obj = MetodosMoney(ID_Metodo=3, Nombre="Tarjeta", Tipo=2, Descripcion="x")
    out = repr(obj)
    assert "3" in out
    assert "Tarjeta" in out
    assert "Tipo=2" in out