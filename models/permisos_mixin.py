from flask import g, redirect, url_for, flash
from flask_admin import expose
from flask_login import current_user
from models import db
from models.permisos_empleado_model import PermisosEmpleado
from models.permisos_puesto_model import PermisosPuesto
from models.pantallas_acciones_model import PantallasAcciones
from models.Acciones_model import Acciones


def pantallas_del_empleado_actual():
    """
    Devuelve el set de endpoints (Pantallas.url) permitidos para el empleado actual.
    Cacheado por request en g. Retorna None si el usuario no es empleado (acceso total).
    """
    if not hasattr(g, "_pantallas_empleado_cache"):
        if not current_user.is_authenticated:
            g._pantallas_empleado_cache = set()
        elif getattr(current_user, "tipo", None) != "empleado":
            g._pantallas_empleado_cache = None  # None = acceso total (gerente, etc.)
        else:
            try:
                from models.Pantallas_model import Pantallas
                from models.estado_pantalla_empleado_model import EstadoPantallaEmpleado

                id_empleado = int(
                    getattr(current_user, "db_id", None)
                    or getattr(current_user, "ID_Empleado", None)
                    or 0
                )
                id_puesto = current_user.id_puesto

                ids_puesto = {
                    r[0]
                    for r in db.session.query(Pantallas.ID_Pantalla)
                    .join(PantallasAcciones, PantallasAcciones.ID_Pantalla == Pantallas.ID_Pantalla)
                    .join(PermisosPuesto, PermisosPuesto.ID_Pantalla_Accion == PantallasAcciones.ID_Pantalla_Accion)
                    .filter(PermisosPuesto.ID_Puesto == id_puesto)
                    .distinct()
                    .all()
                }

                if not ids_puesto:
                    g._pantallas_empleado_cache = set()
                else:
                    activadas = {
                        r[0]
                        for r in db.session.query(Pantallas.url)
                        .join(EstadoPantallaEmpleado, EstadoPantallaEmpleado.ID_Pantalla == Pantallas.ID_Pantalla)
                        .filter(
                            EstadoPantallaEmpleado.ID_Empleado == id_empleado,
                            EstadoPantallaEmpleado.activa == 1,
                            Pantallas.ID_Pantalla.in_(ids_puesto),
                        )
                        .all()
                    }
                    ids_con_registro = {
                        r[0]
                        for r in db.session.query(EstadoPantallaEmpleado.ID_Pantalla)
                        .filter(
                            EstadoPantallaEmpleado.ID_Empleado == id_empleado,
                            EstadoPantallaEmpleado.ID_Pantalla.in_(ids_puesto),
                        )
                        .all()
                    }
                    sin_registro = {
                        r[0]
                        for r in db.session.query(Pantallas.url)
                        .filter(Pantallas.ID_Pantalla.in_(ids_puesto - ids_con_registro))
                        .all()
                    }
                    g._pantallas_empleado_cache = activadas | sin_registro
            except Exception:
                g._pantallas_empleado_cache = set()

    return g._pantallas_empleado_cache


def endpoint_accesible(endpoint: str) -> bool:
    """
    Verifica si el endpoint/url de pantalla está permitido para el usuario actual.
    Los gerentes siempre tienen acceso. Los empleados solo si la pantalla está activa.
    """
    if not current_user.is_authenticated:
        return False
    pantallas = pantallas_del_empleado_actual()
    if pantallas is None:
        return True  # gerente u otro tipo → acceso total
    return endpoint in pantallas


def _cargar_acciones_para_pantalla(id_empleado: int, pantalla_url: str) -> set:
    """Devuelve las acciones activas del empleado para UNA pantalla específica (por su url/endpoint)."""
    from models.Pantallas_model import Pantallas
    resultados = db.session.query(Acciones.Nombre).select_from(PermisosEmpleado).join(
        PermisosPuesto, PermisosPuesto.ID_Permiso_Puesto == PermisosEmpleado.ID_Permiso_Puesto
    ).join(
        PantallasAcciones, PantallasAcciones.ID_Pantalla_Accion == PermisosPuesto.ID_Pantalla_Accion
    ).join(
        Pantallas, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla
    ).join(
        Acciones, Acciones.ID_Accion == PantallasAcciones.ID_Accion
    ).filter(
        PermisosEmpleado.ID_Empleado == id_empleado,
        PermisosEmpleado.estado == 1,
        Pantallas.url == pantalla_url,
    ).all()
    return {r[0] for r in resultados}


def tiene_accion_en_pantalla(pantalla_url: str, nombre_accion: str) -> bool:
    """
    Comprueba si el empleado actual tiene una acción activa en una pantalla específica.
    Usa caché por request para no repetir la consulta.
    """
    id_empleado = getattr(current_user, "db_id", None) or getattr(current_user, "ID_Empleado", None)
    if not id_empleado:
        return False
    try:
        cache_key = "_pac_" + pantalla_url.replace(".", "_").replace("/", "_")
        if not hasattr(g, cache_key):
            setattr(g, cache_key, _cargar_acciones_para_pantalla(int(id_empleado), pantalla_url))
        return nombre_accion in getattr(g, cache_key)
    except Exception:
        return False


# Mantenido por compatibilidad con código existente
def tiene_accion_empleado(nombre_accion: str) -> bool:
    """Deprecated: usa tiene_accion_en_pantalla() para chequeos por pantalla."""
    id_empleado = getattr(current_user, "db_id", None) or getattr(current_user, "ID_Empleado", None)
    if not id_empleado:
        return False
    try:
        if not hasattr(g, "_permisos_global_cache"):
            from models.Pantallas_model import Pantallas
            resultados = db.session.query(Acciones.Nombre).select_from(PermisosEmpleado).join(
                PermisosPuesto, PermisosPuesto.ID_Permiso_Puesto == PermisosEmpleado.ID_Permiso_Puesto
            ).join(
                PantallasAcciones, PantallasAcciones.ID_Pantalla_Accion == PermisosPuesto.ID_Pantalla_Accion
            ).join(
                Acciones, Acciones.ID_Accion == PantallasAcciones.ID_Accion
            ).filter(
                PermisosEmpleado.ID_Empleado == int(id_empleado),
                PermisosEmpleado.estado == 1,
            ).all()
            g._permisos_global_cache = {r[0] for r in resultados}
        return nombre_accion in g._permisos_global_cache
    except Exception:
        return False


class PermisosAdminMixin:
    """
    Mixin para vistas Flask-Admin que controla la visibilidad de botones
    según los permisos activos del empleado en PermisosEmpleado.

    Uso en la subclase:
        accion_buscar       = "buscar"
        accion_crear        = "crear"
        accion_editar       = "editar"
        accion_eliminar     = "eliminar"
        accion_exportar_pdf   = "exportar pdf"
        accion_exportar_excel = "exportar excel"
    """

    accion_buscar = None
    accion_crear = None
    accion_editar = None
    accion_eliminar = None
    accion_exportar_pdf = None
    accion_exportar_excel = None

    def _tiene_permiso(self, accion):
        """Si la acción no está configurada, se permite por defecto. Verifica por pantalla."""
        if not accion:
            return True
        pantalla_url = getattr(self, 'endpoint', '') + '.index_view'
        return tiene_accion_en_pantalla(pantalla_url, accion)

    @property
    def can_create(self):
        return self._tiene_permiso(self.accion_crear)

    @property
    def can_edit(self):
        return self._tiene_permiso(self.accion_editar)

    @property
    def can_delete(self):
        return self._tiene_permiso(self.accion_eliminar)

    @property
    def puede_exportar_pdf(self):
        return self._tiene_permiso(self.accion_exportar_pdf)

    @property
    def puede_exportar_excel(self):
        return self._tiene_permiso(self.accion_exportar_excel)

    @expose('/')
    def index_view(self):
        """Actualiza _search_supported por pantalla antes de que Flask-Admin lo use."""
        if self.accion_buscar is not None:
            self._search_supported = (
                self._tiene_permiso(self.accion_buscar)
                and bool(getattr(self, 'column_searchable_list', None))
            )
        return super().index_view()

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        if getattr(current_user, "tipo", None) != "empleado":
            return False
        pantalla_url = getattr(self, 'endpoint', '') + '.index_view'
        return endpoint_accesible(pantalla_url)

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for('login'))
