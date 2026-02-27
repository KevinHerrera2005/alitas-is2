from datetime import datetime
from io import BytesIO
from typing import Any, Callable, Iterable, List, Optional, Sequence, Tuple

from flask import current_app
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph
from reportlab.lib.utils import ImageReader

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font
from openpyxl.drawing.image import Image as XLImage


Cell = Any
ColumnSpec = Tuple[str, Callable[[Any], Any]]


def _company_name() -> str:
    return current_app.config.get("COMPANY_NAME", "Mi Empresa")


def _logo_path() -> Optional[str]:
    return current_app.config.get("COMPANY_LOGO_PATH")


def _now_str() -> str:
    tz = current_app.config.get("REPORTS_TIMEZONE")
    now = datetime.now(tz) if tz else datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")



def render_pdf(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]], printed_by: str) -> bytes:
    buf = BytesIO()

    def _needs_landscape(cols: Sequence[str], data_rows: Sequence[Sequence[Any]]) -> bool:
        if len(cols) >= 7:
            return True
        for r in data_rows[:40]:
            for v in r:
                s = "" if v is None else str(v)
                if len(s) > 55:
                    return True
        return False

    page_size = landscape(letter) if _needs_landscape(columns, rows) else letter

    doc = SimpleDocTemplate(
        buf,
        pagesize=page_size,
        leftMargin=0.45 * inch,
        rightMargin=0.45 * inch,
        topMargin=1.25 * inch,
        bottomMargin=0.85 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        spaceAfter=8,
        alignment=1,
    )
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=9.2,
        wordWrap="CJK",
    )
    header_cell_style = ParagraphStyle(
        "HeaderCell",
        parent=cell_style,
        fontName="Helvetica-Bold",
        alignment=1,
    )
    normal_style = ParagraphStyle(
        "NormalSmall",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=10,
    )

    def _cell(v: Any, is_header: bool = False) -> Paragraph:
        s = "" if v is None else str(v)
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return Paragraph(s, header_cell_style if is_header else cell_style)

    data: List[List[Any]] = [[_cell(c, True) for c in columns]]
    for r in rows:
        data.append([_cell(v, False) for v in r])

    available_width = doc.width

    def _estimate_width(col_idx: int) -> float:
        max_len = len(str(columns[col_idx]))
        for r in rows[:200]:
            if col_idx < len(r):
                s = "" if r[col_idx] is None else str(r[col_idx])
                max_len = max(max_len, len(s))
        w = 12 + (max_len * 2.6)
        w = max(55, min(w, 220))
        return w

    raw_widths = [_estimate_width(i) for i in range(len(columns))]
    total = sum(raw_widths) if raw_widths else 1
    scale = min(1.0, available_width / total) if total > 0 else 1.0
    col_widths = [w * scale for w in raw_widths]

    if sum(col_widths) < available_width and col_widths:
        extra = available_width - sum(col_widths)
        add = extra / len(col_widths)
        col_widths = [w + add for w in col_widths]

    table = Table(data, hAlign="LEFT", repeatRows=1, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    story = [
        Paragraph(report_title, title_style),
        Spacer(1, 0.10 * inch),
        table,
        Spacer(1, 0.10 * inch),
        Paragraph(f"Registros: {max(len(rows), 0)}", normal_style),
    ]

    company = _company_name()
    logo = _logo_path()
    printed_at = _now_str()

    def on_page(canvas, doc_obj):
        width, height = page_size
        canvas.saveState()

        header_y_top = height - 0.55 * inch
        if logo:
            try:
                img = ImageReader(logo)
                canvas.drawImage(
                    img,
                    doc_obj.leftMargin,
                    height - 0.92 * inch,
                    width=0.70 * inch,
                    height=0.70 * inch,
                    preserveAspectRatio=True,
                    mask="auto",
                )
            except Exception:
                pass

        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(doc_obj.leftMargin + (0.82 * inch), header_y_top, company)

        canvas.setFont("Helvetica", 10)
        canvas.drawString(doc_obj.leftMargin + (0.82 * inch), header_y_top - 14, report_title)

        canvas.setLineWidth(1)
        canvas.line(doc_obj.leftMargin, height - 1.02 * inch, width - doc_obj.rightMargin, height - 1.02 * inch)

        footer_y = 0.55 * inch
        canvas.setLineWidth(1)
        canvas.line(doc_obj.leftMargin, footer_y + 18, width - doc_obj.rightMargin, footer_y + 18)

        canvas.setFont("Helvetica", 8.5)
        canvas.drawString(doc_obj.leftMargin, footer_y + 6, f"Imprimió: {printed_by}")
        canvas.drawString(doc_obj.leftMargin, footer_y - 6, f"Fecha/Hora: {printed_at}")

        page_text = f"Página {canvas.getPageNumber()}"
        canvas.drawCentredString(width / 2, footer_y, page_text)

        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return buf.getvalue()



def render_excel(report_title: str, columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    company = _company_name()
    logo = _logo_path()
    printed_at = _now_str()

    if logo:
        try:
            img = XLImage(logo)
            img.height = 72
            img.width = 72
            ws.add_image(img, "A1")
        except Exception:
            pass

    ws["C1"] = company
    ws["C1"].font = Font(bold=True, size=14)
    ws["C2"] = report_title
    ws["C2"].font = Font(bold=True, size=12)
    ws["C3"] = f"Fecha/Hora: {printed_at}"
    ws["C3"].font = Font(size=10)

    header_row = 5

    for col_idx, col_name in enumerate(columns, start=1):
        cell = ws.cell(row=header_row, column=col_idx, value=col_name)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    data_row = header_row
    for r in rows:
        data_row += 1
        for col_idx, v in enumerate(r, start=1):
            value = "" if v is None else str(v)
            cell = ws.cell(row=data_row, column=col_idx, value=value)
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    ws.freeze_panes = ws["A6"]

    for col_idx in range(1, len(columns) + 1):
        max_len = 10
        for r_idx in range(header_row, data_row + 1):
            val = ws.cell(row=r_idx, column=col_idx).value
            if val is None:
                continue
            max_len = max(max_len, min(len(str(val)), 70))
        ws.column_dimensions[get_column_letter(col_idx)].width = max_len + 2

    out = BytesIO()
    wb.save(out)
    return out.getvalue()
