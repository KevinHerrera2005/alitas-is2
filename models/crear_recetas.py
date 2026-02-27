from decimal import Decimal, ROUND_HALF_UP
import json
import traceback

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import text, func

from models import db
from models.empleado_model import Empleado
from models.in_re_model import IN_RE
from models.receta_model import Receta


def crear_receta_routes(app):
    @app.route("/crear_receta", methods=["GET", "POST"])
    @login_required
    def crear_receta():
        registrar_lookup_tipos_receta(app)
        insumos_query = db.session.execute(
            text(
                """
                SELECT ID_Insumo, Nombre_insumo, precio_lempiras, ID_Unidad, Tipo
                FROM (
                    SELECT
                        i.ID_Insumo,
                        i.Nombre_insumo,
                        i.precio_lempiras,
                        i.ID_Unidad,
                        uc.Tipo,
                        ROW_NUMBER() OVER (
                            PARTITION BY i.Nombre_insumo
                            ORDER BY i.ID_Insumo
                        ) AS rn
                    FROM Insumos i
                    JOIN (
                        SELECT ID_Unidad, MIN(Tipo) AS Tipo
                        FROM Unidades_Conversion
                        GROUP BY ID_Unidad
                    ) AS uc ON i.ID_Unidad = uc.ID_Unidad
                ) t
                WHERE rn = 1
                ORDER BY Nombre_insumo
                """
            )
        ).fetchall()
        insumos = [dict(row._mapping) for row in insumos_query]

        unidades_query = db.session.execute(
            text(
                """
                SELECT ID_Unidad, Nombre_Unidad, Equivalente, Tipo
                FROM Unidades_Conversion
                """
            )
        ).fetchall()
        unidades = [dict(row._mapping) for row in unidades_query]

        categorias_query = db.session.execute(
            text(
                """
                SELECT id_categoria_receta, Nombre_categoria_receta
                FROM categoria_recetas
                ORDER BY id_categoria_receta
                """
            )
        ).fetchall()
        categorias = {c.id_categoria_receta: c.Nombre_categoria_receta for c in categorias_query}

        if request.method == "POST":
            nombre = request.form.get("nombre") or ""
            descripcion = request.form.get("descripcion") or ""
            descripcion_cliente = request.form.get("descripcion_cliente") or ""
            categoria = request.form.get("categoria")
            insumos_json = request.form.get("insumos_json")

            nombre_limpio = nombre.strip()

            if (
                not nombre_limpio
                or not descripcion.strip()
                or not descripcion_cliente.strip()
                or not categoria
            ):
                flash("Por favor completa todos los campos obligatorios.", "warning")
                return redirect(url_for("crear_receta"))

            if getattr(current_user, "tipo", None) != "empleado":
                flash("No autorizado para crear recetas.", "danger")
                return redirect(url_for("login"))

            id_puesto = getattr(current_user, "ID_Puesto", None) or getattr(current_user, "id_puesto", None)
            if int(id_puesto or 0) != 1:
                flash("No autorizado para crear recetas.", "danger")
                return redirect(url_for("login"))

            id_sucursal_usuario = getattr(current_user, "ID_sucursal", None) or getattr(current_user, "id_sucursal", None)
            id_empleado_usuario = getattr(current_user, "ID_Empleado", None)

            if not id_sucursal_usuario or not id_empleado_usuario:
                flash(
                    "No se pudo determinar la sucursal o el empleado de la sesión. Vuelve a iniciar sesión.",
                    "danger",
                )
                return redirect(url_for("login"))

            try:
                empleado = Empleado.query.get(int(id_empleado_usuario))
                if not empleado:
                    flash("No se encontró el empleado de la sesión en la base de datos.", "danger")
                    return redirect(url_for("login"))

                id_jefe_de_cocina = db.session.execute(
                    text(
                        """
                        SELECT TOP 1 ID_Jefe_de_cocina
                        FROM dbo.Jefe_de_cocina
                        WHERE Username = :u AND ID_sucursal = :s AND activo = 1
                        """
                    ),
                    {"u": empleado.Username, "s": int(id_sucursal_usuario)},
                ).scalar()

                if not id_jefe_de_cocina:
                    id_jefe_de_cocina = db.session.execute(
                        text(
                            """
                            INSERT INTO dbo.Jefe_de_cocina (
                                Nombre, apellido, descripcion, activo, Username, Password, ID_sucursal
                            )
                            OUTPUT INSERTED.ID_Jefe_de_cocina
                            VALUES (
                                :nombre, :apellido, :descripcion, :activo, :username, :password, :id_sucursal
                            )
                            """
                        ),
                        {
                            "nombre": (empleado.Nombre or "").strip() or "Jefe",
                            "apellido": (empleado.Apellido or "").strip() or "Cocina",
                            "descripcion": "Jefe de cocina",
                            "activo": 1,
                            "username": (empleado.Username or "").strip(),
                            "password": (empleado.Password or "").strip(),
                            "id_sucursal": int(id_sucursal_usuario),
                        },
                    ).scalar()

                if not id_jefe_de_cocina:
                    flash(
                        "No se pudo vincular tu usuario con dbo.Jefe_de_cocina (no se creó ni se encontró registro).",
                        "danger",
                    )
                    db.session.rollback()
                    return redirect(url_for("crear_receta"))

                nombre_normalizado = "".join(nombre_limpio.split()).lower()

                receta_existente = (
                    Receta.query.filter(
                        func.lower(func.replace(Receta.Nombre_receta, " ", "")) == nombre_normalizado,
                        Receta.ID_sucursal == int(id_sucursal_usuario),
                    ).first()
                )

                if receta_existente:
                    flash(
                        f"Ya existe una receta con el nombre '{receta_existente.Nombre_receta}'.",
                        "danger",
                    )
                    return redirect(url_for("crear_receta"))

                insumos_lista = json.loads(insumos_json) if insumos_json else []
                print("INSUMOS LISTA PARSEADA:", insumos_lista)

                if not insumos_lista:
                    flash("Debes agregar al menos un insumo a la receta.", "warning")
                    return redirect(url_for("crear_receta"))

                insumo_por_clave = {}
                for insumo in insumos_lista:
                    try:
                        clave = (int(insumo["id_insumo"]), int(insumo["id_unidad"]))
                        insumo_por_clave[clave] = insumo
                    except Exception:
                        print("⚠ Insumo inválido en JSON:", insumo)

                insumos_normalizados = list(insumo_por_clave.values())
                print("INSUMOS NORMALIZADOS:", insumos_normalizados)

                if not insumos_normalizados:
                    flash("No se pudo procesar la lista de insumos.", "danger")
                    return redirect(url_for("crear_receta"))

                nueva_receta = Receta(
                    ID_Jefe_de_cocina=int(id_jefe_de_cocina),
                    Nombre_receta=nombre_limpio,
                    descripcion=descripcion,
                    descripcion_cliente=descripcion_cliente,
                    Estado=1,
                    categoria=int(categoria),
                    ID_sucursal=int(id_sucursal_usuario),
                )
                db.session.add(nueva_receta)
                db.session.commit()
                print(f"🆕 Receta creada con ID: {nueva_receta.ID_Receta}")

                values_sql = []
                params = {
                    "id_receta": nueva_receta.ID_Receta,
                    "id_sucursal": int(id_sucursal_usuario),
                }

                for idx, insumo in enumerate(insumos_normalizados, start=1):
                    print("➡ Procesando insumo (CREAR):", insumo)

                    id_insumo = int(insumo["id_insumo"])
                    cantidad_ingresada = float(insumo["cantidad"])
                    id_unidad_ingresada = int(insumo["id_unidad"])

                    unidad_insumo = db.session.execute(
                        text(
                            """
                            SELECT ID_Unidad
                            FROM Insumos
                            WHERE ID_Insumo = :id_insumo
                            """
                        ),
                        {"id_insumo": id_insumo},
                    ).scalar()

                    tipo_ingresado = db.session.execute(
                        text(
                            """
                            SELECT Tipo
                            FROM Unidades_Conversion
                            WHERE ID_Unidad = :id
                            """
                        ),
                        {"id": id_unidad_ingresada},
                    ).scalar()

                    tipo_insumo = db.session.execute(
                        text(
                            """
                            SELECT Tipo
                            FROM Unidades_Conversion
                            WHERE ID_Unidad = :id
                            """
                        ),
                        {"id": unidad_insumo},
                    ).scalar()

                    if tipo_ingresado != tipo_insumo:
                        flash(f"Unidad incompatible para el insumo ID {id_insumo}.", "danger")
                        db.session.rollback()
                        return redirect(url_for("crear_receta"))

                    if unidad_insumo != id_unidad_ingresada:
                        eq_ingresada = db.session.execute(
                            text(
                                """
                                SELECT Equivalente
                                FROM Unidades_Conversion
                                WHERE ID_Unidad = :id
                                """
                            ),
                            {"id": id_unidad_ingresada},
                        ).scalar()

                        eq_insumo = db.session.execute(
                            text(
                                """
                                SELECT Equivalente
                                FROM Unidades_Conversion
                                WHERE ID_Unidad = :id
                                """
                            ),
                            {"id": unidad_insumo},
                        ).scalar()

                        cantidad_convertida = float(cantidad_ingresada) * (float(eq_ingresada) / float(eq_insumo))
                    else:
                        cantidad_convertida = cantidad_ingresada

                    suf = str(idx)
                    values_sql.append(
                        f"(:id_sucursal, :id_receta, :id_insumo_{suf}, :cantidad_{suf}, :id_unidad_{suf}, 1)"
                    )
                    params[f"id_insumo_{suf}"] = id_insumo
                    params[f"cantidad_{suf}"] = cantidad_convertida
                    params[f"id_unidad_{suf}"] = unidad_insumo

                if values_sql:
                    sql_insert = """
                        INSERT INTO IN_RE (
                            ID_sucursal, ID_Receta, ID_Insumo, cantidad_usada, ID_Unidad, Activo
                        )
                        VALUES {values_clause}
                    """.format(values_clause=",\n                               ".join(values_sql))

                    db.session.execute(text(sql_insert), params)

                db.session.commit()
                flash(f"✅ Receta '{nombre_limpio}' creada correctamente con insumos.", "success")
                return redirect(url_for("crud_recetas"))

            except Exception as e:
                db.session.rollback()
                print("❌ ERROR AL CREAR RECETA:")
                traceback.print_exc()
                flash(f"Error al crear la receta: {e}", "danger")
                return redirect(url_for("crear_receta"))

        return render_template(
            "crear_receta.html",
            insumos=insumos,
            unidades=unidades,
            categorias=categorias,
        )


def editar_receta_routes(app):
    registrar_lookup_tipos_receta(app)
    @app.route("/editar_receta/<int:id_receta>", methods=["GET", "POST"])
    @login_required
    def editar_receta(id_receta):
        receta = Receta.query.get_or_404(id_receta)

        insumos_query = db.session.execute(
            text(
                """
                SELECT ID_Insumo, Nombre_insumo, precio_lempiras, ID_Unidad, Tipo
                FROM (
                    SELECT
                        i.ID_Insumo,
                        i.Nombre_insumo,
                        i.precio_lempiras,
                        i.ID_Unidad,
                        uc.Tipo,
                        ROW_NUMBER() OVER (
                            PARTITION BY i.Nombre_insumo
                            ORDER BY i.ID_Insumo
                        ) AS rn
                    FROM Insumos i
                    JOIN (
                        SELECT ID_Unidad, MIN(Tipo) AS Tipo
                        FROM Unidades_Conversion
                        GROUP BY ID_Unidad
                    ) AS uc ON i.ID_Unidad = uc.ID_Unidad
                ) t
                WHERE rn = 1
                ORDER BY Nombre_insumo
                """
            )
        ).fetchall()
        insumos = [dict(row._mapping) for row in insumos_query]

        unidades_query = db.session.execute(
            text(
                """
                SELECT ID_Unidad, Nombre_Unidad, Equivalente, Tipo
                FROM Unidades_Conversion
                """
            )
        ).fetchall()
        unidades = [dict(row._mapping) for row in unidades_query]

        categorias_query = db.session.execute(
            text(
                """
                SELECT id_categoria_receta, Nombre_categoria_receta
                FROM categoria_recetas
                ORDER BY id_categoria_receta
                """
            )
        ).fetchall()
        categorias = {c.id_categoria_receta: c.Nombre_categoria_receta for c in categorias_query}

        ingredientes_query = db.session.execute(
            text(
                """
                SELECT
                    ir.ID_IN_RE,
                    ir.ID_Insumo,
                    i.Nombre_insumo,
                    ir.cantidad_usada,
                    ir.ID_Unidad,
                    uc.Nombre_Unidad,
                    uc.Tipo
                FROM IN_RE ir
                JOIN Insumos i ON ir.ID_Insumo = i.ID_Insumo
                JOIN Unidades_Conversion uc ON ir.ID_Unidad = uc.ID_Unidad
                WHERE ir.ID_Receta = :id AND ir.Activo = 1
                ORDER BY i.Nombre_insumo
                """
            ),
            {"id": id_receta},
        ).fetchall()

        ingredientes = []
        for row in ingredientes_query:
            d = dict(row._mapping)
            ingredientes.append(
                {
                    "id_in_re": d["ID_IN_RE"],
                    "id_insumo": d["ID_Insumo"],
                    "nombre_insumo": d["Nombre_insumo"],
                    "cantidad": float(d["cantidad_usada"]),
                    "id_unidad": d["ID_Unidad"],
                    "nombre_unidad": d["Nombre_Unidad"],
                    "tipo": d["Tipo"],
                }
            )

        if request.method == "POST":
            nombre = request.form.get("nombre") or ""
            descripcion = request.form.get("descripcion") or ""
            descripcion_cliente = request.form.get("descripcion_cliente") or ""
            categoria = request.form.get("categoria")
            insumos_json = request.form.get("insumos_json")

            nombre_limpio = nombre.strip()
            nombre_normalizado = "".join(nombre_limpio.split()).lower()

            if (
                not nombre_limpio
                or not descripcion.strip()
                or not descripcion_cliente.strip()
                or not categoria
            ):
                flash("Por favor completa todos los campos obligatorios.", "warning")
                return redirect(url_for("editar_receta", id_receta=id_receta))

            try:
                existe = (
                    Receta.query.filter(
                        func.lower(func.replace(Receta.Nombre_receta, " ", "")) == nombre_normalizado,
                        Receta.ID_Receta != id_receta,
                        Receta.ID_sucursal == receta.ID_sucursal,
                    ).first()
                )
                if existe:
                    flash(
                        f"Ya existe otra receta con el nombre '{existe.Nombre_receta}'.",
                        "danger",
                    )
                    return redirect(url_for("editar_receta", id_receta=id_receta))

                insumos_lista = json.loads(insumos_json) if insumos_json else []
                print("INSUMOS LISTA PARSEADA (EDITAR):", insumos_lista)

                if not insumos_lista:
                    flash("Debes agregar al menos un insumo a la receta.", "warning")
                    return redirect(url_for("editar_receta", id_receta=id_receta))

                insumo_por_clave = {}
                for insumo in insumos_lista:
                    try:
                        id_in_re = insumo.get("id_in_re")
                        if id_in_re:
                            clave = ("existente", int(id_in_re))
                        else:
                            clave = (int(insumo["id_insumo"]), int(insumo["id_unidad"]))
                        insumo_por_clave[clave] = insumo
                    except Exception as e:
                        print("⚠ Insumo inválido en JSON (editar):", insumo, e)

                insumos_normalizados = list(insumo_por_clave.values())
                print("INSUMOS NORMALIZADOS (EDITAR):", insumos_normalizados)

                receta.Nombre_receta = nombre_limpio
                receta.descripcion = descripcion
                receta.descripcion_cliente = descripcion_cliente
                receta.categoria = int(categoria)
                db.session.add(receta)

                relaciones_actuales = {
                    rel.ID_IN_RE: rel
                    for rel in IN_RE.query.filter_by(ID_Receta=id_receta).all()
                }

                relaciones_por_insumo = {
                    (rel.ID_Insumo, rel.ID_Unidad): rel
                    for rel in relaciones_actuales.values()
                    if rel.Activo
                }

                ids_vigentes = set()

                for insumo in insumos_normalizados:
                    print("➡ Procesando insumo (EDITAR):", insumo)

                    id_in_re = insumo.get("id_in_re")
                    id_insumo = int(insumo["id_insumo"])
                    cantidad_ingresada = Decimal(str(insumo["cantidad"]))
                    id_unidad_ingresada = int(insumo["id_unidad"])

                    unidad_insumo = db.session.execute(
                        text(
                            """
                            SELECT ID_Unidad
                            FROM Insumos
                            WHERE ID_Insumo = :id_insumo
                            """
                        ),
                        {"id_insumo": id_insumo},
                    ).scalar()

                    tipo_ingresado = db.session.execute(
                        text(
                            """
                            SELECT Tipo
                            FROM Unidades_Conversion
                            WHERE ID_Unidad = :id
                            """
                        ),
                        {"id": id_unidad_ingresada},
                    ).scalar()

                    tipo_insumo = db.session.execute(
                        text(
                            """
                            SELECT Tipo
                            FROM Unidades_Conversion
                            WHERE ID_Unidad = :id
                            """
                        ),
                        {"id": unidad_insumo},
                    ).scalar()

                    if tipo_ingresado != tipo_insumo:
                        flash(f"Unidad incompatible para el insumo ID {id_insumo}.", "danger")
                        db.session.rollback()
                        return redirect(url_for("editar_receta", id_receta=id_receta))

                    if unidad_insumo != id_unidad_ingresada:
                        eq_ingresada = db.session.execute(
                            text(
                                """
                                SELECT Equivalente
                                FROM Unidades_Conversion
                                WHERE ID_Unidad = :id
                                """
                            ),
                            {"id": id_unidad_ingresada},
                        ).scalar()

                        eq_insumo = db.session.execute(
                            text(
                                """
                                SELECT Equivalente
                                FROM Unidades_Conversion
                                WHERE ID_Unidad = :id
                                """
                            ),
                            {"id": unidad_insumo},
                        ).scalar()

                        cantidad_convertida = cantidad_ingresada * (
                            Decimal(str(eq_ingresada)) / Decimal(str(eq_insumo))
                        )
                    else:
                        cantidad_convertida = cantidad_ingresada

                    cantidad_convertida = cantidad_convertida.quantize(
                        Decimal("0.001"), rounding=ROUND_HALF_UP
                    )

                    precio_insumo = db.session.execute(
                        text(
                            """
                            SELECT precio_lempiras, peso_individual
                            FROM Insumos
                            WHERE ID_Insumo = :id_insumo
                            """
                        ),
                        {"id_insumo": id_insumo},
                    ).fetchone()

                    costo = Decimal("0")
                    if precio_insumo and precio_insumo.peso_individual not in (0, None):
                        costo = (
                            Decimal(str(precio_insumo.precio_lempiras or 0))
                            / Decimal(str(precio_insumo.peso_individual))
                        ) * cantidad_convertida
                        costo = costo.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                    if id_in_re and int(id_in_re) in relaciones_actuales:
                        relacion = relaciones_actuales[int(id_in_re)]
                    elif (id_insumo, unidad_insumo) in relaciones_por_insumo:
                        relacion = relaciones_por_insumo[(id_insumo, unidad_insumo)]
                    else:
                        relacion = None

                    if relacion:
                        relacion.ID_Insumo = id_insumo
                        relacion.cantidad_usada = cantidad_convertida
                        relacion.ID_Unidad = unidad_insumo
                        relacion.precio_final = costo
                        relacion.Activo = 1
                        ids_vigentes.add(relacion.ID_IN_RE)
                    else:
                        nueva_relacion = IN_RE(
                            ID_Receta=id_receta,
                            ID_Insumo=id_insumo,
                            cantidad_usada=cantidad_convertida,
                            ID_Unidad=unidad_insumo,
                            Activo=1,
                            precio_final=costo,
                            ID_sucursal=receta.ID_sucursal,
                        )
                        db.session.add(nueva_relacion)
                        db.session.flush()
                        ids_vigentes.add(nueva_relacion.ID_IN_RE)

                for id_rel, relacion in relaciones_actuales.items():
                    if id_rel not in ids_vigentes:
                        relacion.Activo = 0

                db.session.commit()
                flash("Receta actualizada correctamente.", "success")
                return redirect(url_for("crud_recetas"))

            except Exception as e:
                db.session.rollback()
                print("❌ ERROR AL EDITAR RECETA:")
                traceback.print_exc()
                flash(f"Error al editar la receta: {e}", "danger")
                return redirect(url_for("editar_receta", id_receta=id_receta))

        return render_template(
            "receta_edit.html",
            receta=receta,
            insumos=insumos,
            unidades=unidades,
            categorias=categorias,
            ingredientes=ingredientes,
        )
def registrar_lookup_tipos_receta(app):
    if "receta_tipo_lookup" in app.view_functions:
        return

    @app.get("/recetas/tipo_lookup")
    @login_required
    def receta_tipo_lookup():
        id_insumo = request.args.get("id_insumo", type=int)
        if not id_insumo:
            return {"error": "Falta id_insumo"}, 400

        tipo_insumo = db.session.execute(
            text(
                """
                SELECT TOP 1 uc.Tipo
                FROM Insumos i
                JOIN Unidades_Conversion uc ON i.ID_Unidad = uc.ID_Unidad
                WHERE i.ID_Insumo = :id_insumo
                """
            ),
            {"id_insumo": id_insumo},
        ).scalar()

        if tipo_insumo is None:
            return {"error": "No se encontró el tipo del insumo"}, 404

        unidades = db.session.execute(
            text(
                """
                SELECT ID_Unidad, Nombre_Unidad
                FROM Unidades_Conversion
                WHERE Tipo = :tipo
                ORDER BY Nombre_Unidad
                """
            ),
            {"tipo": int(tipo_insumo)},
        ).fetchall()

        unidades_list = [{"id": int(u.ID_Unidad), "nombre": u.Nombre_Unidad} for u in unidades]

        return {"tipo_insumo": int(tipo_insumo), "unidades": unidades_list}

import os
import re

def _connection_string():
    driver = os.getenv("ODBC_DRIVER", "ODBC Driver 17 for SQL Server")
    server = os.getenv("DB_SERVER", r"DESKTOP-8S6NK4G\SQLEXPRESS")
    db_name = os.getenv("DB_NAME", "ALITAS EL COMELON SF")
    user = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD", "z41ss1l0")
    trust = os.getenv("DB_TRUST_CERT", "yes")

    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={db_name};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate={trust};"
    )

def db_esta_activa(app=None):
    try:
        if app is not None:
            with app.app_context():
                db.session.execute(text("SELECT 1")).scalar()
                return True
    except Exception:
        pass

    try:
        import pyodbc
        conn = pyodbc.connect(_connection_string(), timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        row = cur.fetchone()
        conn.close()
        return bool(row) and row[0] == 1
    except Exception:
        return False

def evitar_valores_nulos(raw):
    if raw is None:
        return None

    out = str(raw).strip()
    if out == "":
        return None

    if out.isdigit():
        return None

    if re.search(r"(.)\1\1", out.lower()):
        return None

    return out

def validar_cantidad_usada(raw):
    try:
        out = float(raw)
    except Exception:
        return None

    if out <= 0:
        return None

    if int(abs(out)) >= 100000:
        return None

    return int(out) if float(out).is_integer() else float(out)

def validar_insumo_existe(raw_id_insumo):
    try:
        rid = int(raw_id_insumo)
    except Exception:
        return False

    try:
        import pyodbc
        conn = pyodbc.connect(_connection_string(), timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT TOP 1 1 FROM Insumos WHERE ID_Insumo = ?", (rid,))
        row = cur.fetchone()
        conn.close()
        return row is not None
    except Exception:
        return False

def validar_categoria_existe(raw_id_categoria):
    try:
        rid = int(raw_id_categoria)
    except Exception:
        return False

    try:
        import pyodbc
        conn = pyodbc.connect(_connection_string(), timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT TOP 1 1 FROM categoria_recetas WHERE id_categoria_receta = ?", (rid,))
        row = cur.fetchone()
        conn.close()
        return row is not None
    except Exception:
        return False

def borrar_receta_si_existe(raw_id_receta):
    try:
        rid = int(raw_id_receta)
    except Exception:
        return False

    try:
        import pyodbc
        conn = pyodbc.connect(_connection_string(), timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT TOP 1 1 FROM Recetas WHERE ID_Receta = ?", (rid,))
        row = cur.fetchone()
        if row is None:
            conn.close()
            return False
        cur.execute("DELETE FROM IN_RE WHERE ID_Receta = ?", (rid,))
        cur.execute("DELETE FROM Recetas WHERE ID_Receta = ?", (rid,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        try:
            conn.rollback()
            conn.close()
        except Exception:
            pass
        return False
