from datetime import datetime
from io import BytesIO
from typing import Any, Callable, List, Optional, Sequence, Tuple

from flask import current_app
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table as XLTable
from openpyxl.worksheet.table import TableStyleInfo


Cell = Any
ColumnSpec = Tuple[str, Callable[[Any], Any]]


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


def _necesita_landscape(cols: int) -> bool:
    try:
        max_cols_portrait = int(current_app.config.get("REPORTS_MAX_COLS_PORTRAIT", 7))
    except Exception:
        max_cols_portrait = 7
    return cols > max_cols_portrait


def _particionar_columnas(columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> List[Tuple[List[str], List[List[Any]]]]:
    try:
        max_cols = int(current_app.config.get("REPORTS_MAX_COLS_PER_TABLE", 10))
    except Exception:
        max_cols = 10

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


def generar_pdf(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]], printed_by: str) -> bytes:
    buf = BytesIO()
    page_size = landscape(letter) if _necesita_landscape(len(columns)) else letter

    doc = SimpleDocTemplate(
        buf,
        pagesize=page_size,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.8 * inch,
        title=report_title,
        author=_nombre_empresa(),
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        spaceAfter=10,
    )
    meta_style = ParagraphStyle(
        "MetaCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.grey,
        spaceAfter=8,
    )

    story = []

    logo_path = _ruta_logo()
    if logo_path:
        try:
            img = ImageReader(logo_path)
            iw, ih = img.getSize()
            max_w = 1.6 * inch
            scale = max_w / float(iw)
            story.append(Table([[img]], colWidths=[max_w], rowHeights=[ih * scale]))
            story.append(Spacer(1, 0.08 * inch))
        except Exception:
            pass

    story.append(Paragraph(report_title, title_style))
    story.append(Paragraph(f"Empresa: {_nombre_empresa()}", meta_style))
    story.append(Paragraph(f"Impreso por: {printed_by}", meta_style))
    story.append(Paragraph(f"Fecha/Hora: {_ahora_str()}", meta_style))
    story.append(Spacer(1, 0.15 * inch))

    secciones = _particionar_columnas(columns, rows)

    for idx, (cols_chunk, rows_chunk) in enumerate(secciones):
        data = [list(cols_chunk)]
        for r in rows_chunk:
            data.append([_texto(v) for v in r])

        table = Table(data, repeatRows=1)

        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
        table.setStyle(style)
        story.append(table)

        if idx < len(secciones) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    return buf.getvalue()


def _auto_anchos(ws, columns: Sequence[str], rows: Sequence[Sequence[Any]]):
    widths = [len(str(c)) if c is not None else 0 for c in columns]
    for r in rows:
        for i, v in enumerate(r):
            s = _texto(v)
            if i < len(widths):
                widths[i] = max(widths[i], len(s))
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = min(max(w + 2, 10), 45)


def _excel_partes(report_title: str, printed_by: str):
    header_fill = PatternFill("solid", fgColor="111827")
    header_font = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
    body_font = Font(name="Calibri", size=10)
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left = Alignment(horizontal="left", vertical="top", wrap_text=True)

    thin = Side(style="thin", color="D1D5DB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    return header_fill, header_font, body_font, center, left, border


def generar_excel(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]], printed_by: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    ws["A1"] = report_title
    ws["A2"] = f"Empresa: {_nombre_empresa()}"
    ws["A3"] = f"Impreso por: {printed_by}"
    ws["A4"] = f"Fecha/Hora: {_ahora_str()}"

    start_row = 6
    for i, col in enumerate(columns, start=1):
        ws.cell(row=start_row, column=i, value=col)

    for r_idx, r in enumerate(rows, start=start_row + 1):
        for c_idx, v in enumerate(r, start=1):
            ws.cell(row=r_idx, column=c_idx, value=_texto(v))

    header_fill, header_font, body_font, center, left, border = _excel_partes(report_title, printed_by)

    max_col = len(columns)
    max_row = start_row + len(rows)

    for c in range(1, max_col + 1):
        cell = ws.cell(row=start_row, column=c)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center
        cell.border = border

    for r in range(start_row + 1, max_row + 1):
        for c in range(1, max_col + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = body_font
            cell.alignment = left
            cell.border = border

    _auto_anchos(ws, columns, rows)

    try:
        ref = f"A{start_row}:{get_column_letter(max_col)}{max_row}"
        tab = XLTable(displayName="TablaReporte", ref=ref)
        style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True, showColumnStripes=False)
        tab.tableStyleInfo = style
        ws.add_table(tab)
    except Exception:
        pass

    logo_path = _ruta_logo()
    if logo_path:
        try:
            img = XLImage(logo_path)
            img.width = 160
            img.height = 55
            ws.add_image(img, "H1")
        except Exception:
            pass

    out = BytesIO()
    wb.save(out)
    return out.getvalue()