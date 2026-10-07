from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    recipient_name: str,
    event_name: str,
    event_date: str,
    certificate_id: int
) -> str:

    filename = f"certificate_{certificate_id}.pdf"
    file_path = OUTPUT_DIR / filename

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=landscape(A4)
    )

    # Outer border
    pdf.setStrokeColor(colors.HexColor("#1B5E20"))
    pdf.setLineWidth(4)
    pdf.rect(
        25,
        25,
        page_width - 50,
        page_height - 50
    )

    # Inner border
    pdf.setStrokeColor(colors.HexColor("#66BB6A"))
    pdf.setLineWidth(1.5)
    pdf.rect(
        38,
        38,
        page_width - 76,
        page_height - 76
    )

    # Title
    pdf.setFillColor(colors.HexColor("#1B5E20"))
    pdf.setFont("Helvetica-Bold", 30)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 110,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Subtitle
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 155,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFillColor(colors.HexColor("#1B5E20"))
    pdf.setFont("Helvetica-Bold", 32)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 215,
        recipient_name
    )

    # Description
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 270,
        "for successfully participating in"
    )

    # Event name
    pdf.setFillColor(colors.HexColor("#2E7D32"))
    pdf.setFont("Helvetica-Bold", 21)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 305,
        event_name
    )

    # Date
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 14)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 345,
        f"Date: {event_date}"
    )

    # Certificate ID
    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        55,
        55,
        f"Certificate ID: {certificate_id}"
    )

    pdf.drawRightString(
        page_width - 55,
        55,
        "Bulk Certificate Generator"
    )

    pdf.save()

    return str(file_path)