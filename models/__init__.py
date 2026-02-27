from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

_models_loaded = False


def load_models():
    global _models_loaded
    if _models_loaded:
        return
    _models_loaded = True

    from .categoria_insumo_model import CategoriaInsumo
    from .tipo_documento_model import TipoDocumento
    from .impuestos_model import Impuesto, ImpuestoCategoria
    from .insumo_model import Insumo
    from .unidades_medida_model import Unidades_medida
    from .empleado_model import Empleado, Puesto
    from .empleado_documento_model import EmpleadoDocumento
    from .usuario_cliente_model import UsuarioCliente
    from .direccion_model import Direccion
    from .direccion_cliente_model import DireccionDelCliente
    from .metodo_pago_model import MetodoPago
    from .gerente_model import Gerente

    from .categoria_recetas_model import Categoria_recetas
    from .sucursal_model import Sucursal

    from .in_re_model import IN_RE
    from .insumo_precio_historico_model import InsumoPrecioHistorico
    from .recetas_precio_historico_model import RecetaPrecioHistorico
    from .receta_model import Receta

    from .proveedores_model import Proveedor, ProveedorInsumo

    from .metodos_money_model import MetodosMoney
    from .pagos_cliente_model import PagosCliente
    from .pago_detalle_model import PagoDetalle

    from .factura_model import Factura
    from .factura_detalle_model import FacturaDetalle

    from .parametro_sar_model import ParametroSAR
    from .cai_model import CAI
    from .cai_historico_model import CAIHistorico

    from .impuesto_tasa_historica_model import ImpuestoTasaHistorica

    from .carrito_model import Carrito

    from .orden_entrega_model import OrdenEntrega
    from .orden_proveedor_model import OrdenProveedor
    from .ordenes_proveedores_model import OrdenesProveedores, OrdenesProveedoresDetalle

    from .historial_ordenes_repartidor_model import HistorialOrdenesRepartidor
