from flask import Blueprint, render_template
from flask_login import current_user
from datetime import datetime
import traceback
from mensajes_logs import logger_

index_admin_bp = Blueprint("index_admin_bp", __name__)


@index_admin_bp.before_request
def _solo_staff():
    from models.permisos_mixin import verificar_tipo
    return verificar_tipo("gerente", "empleado")


@index_admin_bp.route("/index")
def index():
    from flask import redirect, url_for as _url_for
    from models.permisos_mixin import es_admin_panel, pantallas_del_empleado_actual

    # Gerentes y empleados admin van directamente al hub de administración
    if es_admin_panel():
        return redirect(_url_for("ver_permisos_empleado", modulo="permisos_puesto"))

    # Empleados normales: mostrar pantalla de bienvenida con imagen del puesto
    try:
        from flask import current_app, url_for as _url_for
        permisos = pantallas_del_empleado_actual() or set()
        nombre = (
            getattr(current_user, "nombre", None)
            or getattr(current_user, "Nombre", None)
            or "Usuario"
        )
        tipo = getattr(current_user, "tipo", None)

        # Obtener nombre del puesto
        id_puesto = getattr(current_user, "id_puesto", None) or getattr(current_user, "ID_Puesto", None)
        nombre_puesto = "Empleado"
        if id_puesto:
            from models.empleado_model import Puesto
            from Main import db
            puesto_obj = db.session.get(Puesto, int(id_puesto))
            if puesto_obj:
                nombre_puesto = puesto_obj.Nombre_Puesto

        _IMAGENES_PUESTO = {
            'jefe de cocina':                  'bienvenido_jef.png',
            'contador':                        'bienvenido_cont.png',
            'encargado':                       'bienvenido_enc.png',
            'encargado de compra':             'bienvenido_enc.png',
            'encargado de compras':            'bienvenido_enc.png',
            'encargado de compra de insumos':  'bienvenido_enc.png',
            'encargado de compras insumos':    'bienvenido_enc.png',
            'encargado compras insumos':       'bienvenido_enc.png',
            'repartidor':                      'bienvenido_repartidor.png',
            'consultor':                       'bienvenida_consultor.png',
            'gerente':                         'bienvenida_gerente.png',
            'admin roles':                     'bienvenido_administrador.png',
        }
        imagen_puesto = _IMAGENES_PUESTO.get(nombre_puesto.lower().strip(), 'logo_bienvenido.png')

        # Construir lista de pantallas para el navbar
        _EXCLUIR_NAV = {
            'acciones_admin.index_view',
            'impuesto_tasa_historica_admin.index_view',
            'carrito.index_view',
            'usuarios_cliente_admin.index_view',
            'empleado_documento_admin.index_view',
            'pantallas_admin.index_view',
        }
        _NOMBRES_CUSTOM = {
            'panel_encargado.encargar_insumos': 'Encargar Insumos',
            'crud_recetas': 'Recetas',
            'ver_pantallas_acciones': 'Pantallas & Acciones',
        }
        pantallas_nav = []
        _urls_agregadas = set()
        try:
            _admin_obj = current_app.extensions.get('admin')
            _admin_inst = (_admin_obj[0] if isinstance(_admin_obj, list) else _admin_obj)
            for _v in _admin_inst._views:
                if not _v.endpoint or _v.endpoint == 'admin':
                    continue
                ep = _v.endpoint + '.index_view'
                if ep in permisos and ep not in _EXCLUIR_NAV:
                    href = _url_for(ep)
                    pantallas_nav.append({'nombre': _v.name, 'url': href})
                    _urls_agregadas.add(ep)
        except Exception:
            pass
        # Agregar rutas personalizadas que estén en permisos y no sean Flask-Admin
        for ep in sorted(permisos):
            if ep in _EXCLUIR_NAV or ep in _urls_agregadas:
                continue
            try:
                href = _url_for(ep)
                nombre_ep = _NOMBRES_CUSTOM.get(ep, ep.replace('_', ' ').replace('.', ' ').title())
                pantallas_nav.append({'nombre': nombre_ep, 'url': href})
            except Exception:
                pass

        return render_template(
            "index_admin.html",
            nombre_usuario=nombre,
            tipo_usuario=tipo,
            nombre_puesto=nombre_puesto,
            imagen_puesto=imagen_puesto,
            pantallas_nav=pantallas_nav,
        )
    except Exception as error:
        fecha = datetime.now().strftime("%Y%m%d-%H%M%S")
        logger_.Logger.add_to_log("error", str(error), "index_admin", fecha)
        logger_.Logger.add_to_log("error", traceback.format_exc(), "index_admin", fecha)
        return "Error al abrir el panel.", 500
