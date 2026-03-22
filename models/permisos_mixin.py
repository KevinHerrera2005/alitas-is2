from flask import g, redirect, url_for, flash
from flask_admin import expose
from flask_login import current_user
from models import db
from models.permisos_puesto_model import PermisosPuesto
from models.pantallas_acciones_model import PantallasAcciones
from models.Acciones_model import Acciones


def pantallas_del_empleado_actual():
    """
    Devuelve el set de endpoints (Pantallas.url) permitidos para el empleado actual.

    La lógica es puramente basada en el puesto:
      - Una pantalla está habilitada si el puesto tiene AL MENOS UN PermisosPuesto
        con estado == 1 para alguna acción de esa pantalla.
      - Si el puesto no tiene ningún permiso activo (todo estado=0), el set es vacío
        y el empleado no puede acceder a ninguna pantalla.

    Retorna None si el usuario NO es empleado → acceso total (gerente, etc.).
    Cacheado en g por request.
    """
    if not hasattr(g, "_pantallas_empleado_cache"):
        if not current_user.is_authenticated:
            g._pantallas_empleado_cache = set()
        else:
            id_puesto = getattr(current_user, "id_puesto", None) or getattr(current_user, "ID_Puesto", None)
            if not id_puesto:
                g._pantallas_empleado_cache = set()
            else:
                try:
                    from models.Pantallas_model import Pantallas

                    filas = (
                        db.session.query(Pantallas.url)
                        .join(PantallasAcciones, PantallasAcciones.ID_Pantalla == Pantallas.ID_Pantalla)
                        .join(PermisosPuesto, PermisosPuesto.ID_Pantalla_Accion == PantallasAcciones.ID_Pantalla_Accion)
                        .filter(
                            PermisosPuesto.ID_Puesto == int(id_puesto),
                            PermisosPuesto.estado == 1,
                            Pantallas.estado == 1,
                            PantallasAcciones.estado == 1,
                        )
                        .distinct()
                        .all()
                    )
                    g._pantallas_empleado_cache = {r[0] for r in filas}
                except Exception:
                    g._pantallas_empleado_cache = set()

    return g._pantallas_empleado_cache


def endpoint_accesible(endpoint: str) -> bool:
    """
    Verifica si el endpoint/url de pantalla está permitido para el usuario actual.
    Todos los usuarios (incluido gerente) pasan por PermisosPuesto.
    """
    if not current_user.is_authenticated:
        return False
    pantallas = pantallas_del_empleado_actual()
    return endpoint in pantallas


def _cargar_acciones_para_pantalla(id_puesto: int, pantalla_url: str) -> set:
    """
    Devuelve las acciones activas del PUESTO para una pantalla específica.
    Usa PermisosPuesto.estado directamente (no PermisosEmpleado).
    """
    from models.Pantallas_model import Pantallas

    resultados = (
        db.session.query(Acciones.Nombre)
        .join(PantallasAcciones, PantallasAcciones.ID_Accion == Acciones.ID_Accion)
        .join(PermisosPuesto, PermisosPuesto.ID_Pantalla_Accion == PantallasAcciones.ID_Pantalla_Accion)
        .join(Pantallas, Pantallas.ID_Pantalla == PantallasAcciones.ID_Pantalla)
        .filter(
            PermisosPuesto.ID_Puesto == id_puesto,
            PermisosPuesto.estado == 1,
            Pantallas.url == pantalla_url,
            Pantallas.estado == 1,
            PantallasAcciones.estado == 1,
        )
        .all()
    )
    return {r[0] for r in resultados}


def tiene_accion_en_pantalla(pantalla_url: str, nombre_accion: str) -> bool:
    """
    Comprueba si el puesto del empleado actual tiene una acción activa
    en una pantalla específica. Cacheado por request.
    Los gerentes y otros tipos que no sean empleados tienen acceso total.
    """
    if not current_user.is_authenticated:
        return False
    id_puesto = getattr(current_user, "id_puesto", None) or getattr(current_user, "ID_Puesto", None)
    if not id_puesto:
        return False
    try:
        cache_key = "_pac_" + pantalla_url.replace(".", "_").replace("/", "_")
        if not hasattr(g, cache_key):
            setattr(g, cache_key, _cargar_acciones_para_pantalla(int(id_puesto), pantalla_url))
        return nombre_accion in getattr(g, cache_key)
    except Exception:
        return False


def tiene_accion_empleado(nombre_accion: str) -> bool:
    """
    Compatibilidad con código existente.
    Verifica si el puesto del empleado tiene la acción activa en CUALQUIER pantalla.
    Los gerentes y otros tipos que no sean empleados tienen acceso total.
    """
    if not current_user.is_authenticated:
        return False
    id_puesto = getattr(current_user, "id_puesto", None) or getattr(current_user, "ID_Puesto", None)
    if not id_puesto:
        return False
    try:
        if not hasattr(g, "_permisos_global_cache"):
            resultados = (
                db.session.query(Acciones.Nombre)
                .join(PantallasAcciones, PantallasAcciones.ID_Accion == Acciones.ID_Accion)
                .join(PermisosPuesto, PermisosPuesto.ID_Pantalla_Accion == PantallasAcciones.ID_Pantalla_Accion)
                .filter(
                    PermisosPuesto.ID_Puesto == int(id_puesto),
                    PermisosPuesto.estado == 1,
                    PantallasAcciones.estado == 1,
                )
                .all()
            )
            g._permisos_global_cache = {r[0] for r in resultados}
        return nombre_accion in g._permisos_global_cache
    except Exception:
        return False


class PermisosAdminMixin:
    """
    Mixin para vistas Flask-Admin que controla la visibilidad de botones
    según los permisos activos del PUESTO en PermisosPuesto.

    Uso en la subclase:
        accion_buscar         = "buscar"
        accion_crear          = "crear"
        accion_editar         = "editar"
        accion_eliminar       = "eliminar"
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
        """Si la acción no está configurada, se permite por defecto. Verifica por pantalla.
        Todos los usuarios pasan por PermisosPuesto según su id_puesto."""
        if not accion:
            return True
        if not current_user.is_authenticated:
            return False
        pantalla_url = getattr(self, "endpoint", "") + ".index_view"
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

    @expose("/")
    def index_view(self):
        """Actualiza _search_supported por pantalla antes de que Flask-Admin lo use."""
        if self.accion_buscar is not None:
            self._search_supported = self._tiene_permiso(self.accion_buscar) and bool(
                getattr(self, "column_searchable_list", None)
            )
        return super().index_view()

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        tipo = getattr(current_user, "tipo", None)
        if tipo not in ("empleado", "gerente"):
            return False
        pantalla_url = getattr(self, "endpoint", "") + ".index_view"
        return endpoint_accesible(pantalla_url)

    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes acceso a esta pantalla.", "danger")
        return redirect(url_for("login"))

    def is_visible(self):
        return self.is_accessible()


def verificar_tipo(*tipos_permitidos):
    """
    Verifica que el usuario autenticado sea de uno de los tipos indicados.
    Retorna un redirect con mensaje si no tiene acceso, o None si sí tiene.
    Usar en before_request de blueprints.
    """
    if not current_user.is_authenticated:
        flash("Debes iniciar sesión para continuar.", "warning")
        return redirect(url_for("login"))
    if getattr(current_user, "tipo", None) not in tipos_permitidos:
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for("login"))
    return None
