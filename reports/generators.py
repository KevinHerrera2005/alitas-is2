from datetime import datetime
from io import BytesIO
from typing import Any, List, Optional, Sequence, Tuple

from flask import current_app
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table as XLTable
from openpyxl.worksheet.table import TableStyleInfo


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFont("Helvetica", 8)
            ancho = self._pagesize[0]
            self.drawCentredString(ancho / 2, 0.48 * inch, f"Página {self._pageNumber}/{total_pages}")
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


def _nombre_empresa() -> str:
    return current_app.config.get("COMPANY_NAME", "Alitas El Comelon")


def _ruta_logo() -> Optional[str]:
    return current_app.config.get("COMPANY_LOGO_PATH")


def _ahora_str() -> str:
    tz = current_app.config.get("REPORTS_TIMEZONE")
    now = datetime.now(tz) if tz else datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def _texto(val: Any) -> str:
    if val is None:
        return ""
    try:
        if isinstance(val, (list, tuple, set)):
            parts = [_texto(v) for v in list(val)]
            parts = [p for p in parts if p]
            return ", ".join(parts)
        return str(val)
    except Exception:
        return ""


def _escape_para(s: str) -> str:
    s = str(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _separar_camel(s: str) -> str:
    if not s:
        return ""
    out = []
    prev = ""
    for ch in s:
        if prev and ch.isupper() and (prev.islower() or (prev.isupper() and len(out) > 0 and out[-1][-1].islower())):
            out.append(" ")
        out.append(ch)
        prev = ch
    return "".join(out)


def _normalizar_etiqueta(s: Any) -> str:
    txt = _texto(s).strip()
    if not txt:
        return ""
    txt = txt.replace("_", " ").replace("-", " ")
    txt = " ".join(txt.split())
    txt = _separar_camel(txt)
    txt = " ".join(txt.split())
    return txt.upper()


def _necesita_landscape(cols: int) -> bool:
    try:
        max_cols_portrait = int(current_app.config.get("REPORTS_MAX_COLS_PORTRAIT", 7))
    except Exception:
        max_cols_portrait = 7
    return cols > max_cols_portrait


def _should_split(columns_count: int) -> bool:
    try:
        max_cols = int(current_app.config.get("REPORTS_MAX_COLS_PER_TABLE", 12))
    except Exception:
        max_cols = 12
    return columns_count > max_cols


def _particionar_columnas(columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> List[Tuple[List[str], List[List[Any]]]]:
    try:
        max_cols = int(current_app.config.get("REPORTS_MAX_COLS_PER_TABLE", 12))
    except Exception:
        max_cols = 12

    cols = list(columns)
    out = []
    i = 0
    while i < len(cols):
        chunk_cols = cols[i : i + max_cols]
        chunk_rows = []
        for r in rows:
            rr = list(r)
            chunk_rows.append(rr[i : i + max_cols])
        out.append((chunk_cols, chunk_rows))
        i += max_cols
    return out


def _font_sizes_for_cols(ncols: int) -> Tuple[float, float]:
    if ncols >= 16:
        return 7.0, 6.5
    if ncols >= 12:
        return 7.5, 7.0
    if ncols >= 9:
        return 8.0, 7.5
    return 9.0, 8.0


def _calc_col_widths(avail_width: float, columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> List[float]:
    n = len(columns)
    if n <= 0:
        return []

    sample = rows[:250] if rows else []
    maxlens = []
    for i, c in enumerate(columns):
        m = len(_texto(c))
        for r in sample:
            if i < len(r):
                m = max(m, len(_texto(r[i])))
        maxlens.append(m)

    weights = [max(5, min(42, x)) for x in maxlens]
    total = sum(weights) if weights else 1

    min_w = 0.55 * inch if n >= 10 else 0.65 * inch
    max_w = 1.7 * inch if n >= 10 else 2.4 * inch

    widths = []
    for w in weights:
        ww = avail_width * (w / total)
        ww = max(min_w, min(max_w, ww))
        widths.append(ww)

    s = sum(widths)
    if s > 0:
        scale = avail_width / s
        widths = [x * scale for x in widths]

    return widths


def _header_block(report_title: str, printed_by: str) -> Table:
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        spaceAfter=6,
    )
    meta_style = ParagraphStyle(
        "MetaCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.grey,
        leading=11,
    )

    title = _normalizar_etiqueta(report_title)
    text_block = [
        Paragraph(title, title_style),
        Paragraph(f"Empresa: {_nombre_empresa()}", meta_style),
        Paragraph(f"Impreso por: {printed_by}", meta_style),
        Paragraph(f"Fecha/Hora: {_ahora_str()}", meta_style),
    ]

    logo_path = _ruta_logo()
    if logo_path:
        try:
            img = RLImage(logo_path)
            target_w = 1.6 * inch
            iw, ih = img.imageWidth, img.imageHeight
            if iw and ih:
                scale = target_w / float(iw)
                img.drawWidth = target_w
                img.drawHeight = float(ih) * scale
            t = Table([[img, text_block]], colWidths=[1.8 * inch, None])
        except Exception:
            t = Table([[text_block]], colWidths=[None])
    else:
        t = Table([[text_block]], colWidths=[None])

    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def generar_pdf(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]], printed_by: str) -> bytes:
    buf = BytesIO()

    page_size = landscape(letter) if _necesita_landscape(len(columns)) else letter

    left_margin = 0.6 * inch
    right_margin = 0.6 * inch
    top_margin = 0.7 * inch
    bottom_margin = 0.8 * inch

    doc = SimpleDocTemplate(
        buf,
        pagesize=page_size,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
        title=_normalizar_etiqueta(report_title),
        author=_nombre_empresa(),
    )

    avail_width = page_size[0] - left_margin - right_margin

    story = []
    story.append(_header_block(report_title, printed_by))
    story.append(Spacer(1, 0.15 * inch))

    if _should_split(len(columns)):
        secciones = _particionar_columnas(columns, rows)
    else:
        secciones = [(list(columns), [list(r) for r in rows])]

    for idx, (cols_chunk, rows_chunk) in enumerate(secciones):
        ncols = len(cols_chunk)
        head_fs, body_fs = _font_sizes_for_cols(ncols)

        wrap_header = ParagraphStyle(
            name="WrapHeader",
            fontName="Helvetica-Bold",
            fontSize=head_fs,
            leading=head_fs + 2,
            alignment=1,
            wordWrap="CJK",
            splitLongWords=1,
        )

        wrap_cell = ParagraphStyle(
            name="WrapCell",
            fontName="Helvetica",
            fontSize=body_fs,
            leading=body_fs + 2,
            wordWrap="CJK",
            splitLongWords=1,
        )

        header_row = [Paragraph(_escape_para(_normalizar_etiqueta(c)), wrap_header) for c in cols_chunk]
        data = [header_row]

        for r in rows_chunk:
            fila = []
            for v in r:
                s = _escape_para(_texto(v)).replace("\n", "<br/>")
                fila.append(Paragraph(s, wrap_cell))
            data.append(fila)

        col_widths = _calc_col_widths(avail_width, cols_chunk, rows_chunk)

        table = Table(data, repeatRows=1, colWidths=col_widths, hAlign="LEFT")

        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),

            ("ALIGN", (0, 1), (-1, -1), "LEFT"),
            ("VALIGN", (0, 1), (-1, -1), "TOP"),

            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9CA3AF")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#F3F4F6")]),

            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]

        table.setStyle(TableStyle(style_cmds))
        story.append(table)

        if idx < len(secciones) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    return buf.getvalue()


def _auto_anchos(ws, columns: Sequence[str], rows: Sequence[Sequence[Any]]):
    widths = [len(_texto(c)) for c in columns]
    for r in rows[:800]:
        for i, v in enumerate(r):
            s = _texto(v)
            if i < len(widths):
                widths[i] = max(widths[i], len(s))
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = min(max(w + 2, 11), 48)


def generar_excel(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]], printed_by: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "REPORTE"

    ws.sheet_view.showGridLines = False

    fondo = PatternFill("solid", fgColor="FFFFFF")
    for row in range(1, 140):
        for col in range(1, 70):
            ws.cell(row=row, column=col).fill = fondo

    cols_fmt = [_normalizar_etiqueta(c) for c in columns]

    max_col = max(1, len(cols_fmt))
    last_col = get_column_letter(max(2, max_col))

    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 42

    logo_path = _ruta_logo()
    if logo_path:
        try:
            img = XLImage(logo_path)
            size = 90
            img.width = size
            img.height = size
            ws.add_image(img, "A1")
            ws.row_dimensions[1].height = size * 0.75
        except Exception:
            ws.row_dimensions[1].height = 65
    else:
        ws.row_dimensions[1].height = 65

    ws.row_dimensions[2].height = 28
    ws.row_dimensions[3].height = 20
    ws.row_dimensions[4].height = 20
    ws.row_dimensions[5].height = 20
    ws.row_dimensions[6].height = 10

    ws.merge_cells(f"A2:{last_col}2")
    ws["A2"] = _normalizar_etiqueta(report_title)
    ws["A2"].font = Font(bold=True, name="Calibri", size=16)
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center")

    ws["A3"] = "EMPRESA:"
    ws["B3"] = _nombre_empresa()
    ws["A4"] = "IMPRESO POR:"
    ws["B4"] = printed_by
    ws["A5"] = "FECHA/HORA:"
    ws["B5"] = _ahora_str()

    for r in range(3, 6):
        ws[f"A{r}"].font = Font(bold=True, name="Calibri", size=11)
        ws[f"A{r}"].alignment = Alignment(horizontal="left", vertical="center")
        ws[f"B{r}"].alignment = Alignment(horizontal="left", vertical="center")

    start_row = 8

    header_fill = PatternFill("solid", fgColor="111827")
    header_font = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
    body_font = Font(name="Calibri", size=10)

    thin = Side(style="thin", color="D1D5DB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for col_index, col_name in enumerate(cols_fmt, 1):
        cell = ws.cell(row=start_row, column=col_index, value=col_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border

    for row_index, row_data in enumerate(rows, start_row + 1):
        for col_index, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_index, column=col_index, value=_texto(value))
            cell.font = body_font
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            cell.border = border

    _auto_anchos(ws, cols_fmt, rows)

    max_row = start_row + len(rows)
    real_last_col = get_column_letter(max_col)

    try:
        ref = f"A{start_row}:{real_last_col}{max_row}"
        tab = XLTable(displayName="TABLAREPORTE", ref=ref)
        style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True, showColumnStripes=False)
        tab.tableStyleInfo = style
        ws.add_table(tab)
    except Exception:
        pass

    ws.freeze_panes = ws[f"A{start_row + 1}"]

    out = BytesIO()
    wb.save(out)
    return out.getvalue()


def render_pdf(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]], printed_by: str) -> bytes:
    return generar_pdf(report_title=report_title, columns=columns, rows=rows, printed_by=printed_by)


def render_excel(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]], printed_by: str) -> bytes:
    return generar_excel(report_title=report_title, columns=columns, rows=rows, printed_by=printed_by)