import io
import os
from django.conf import settings
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

def generate_order_pdf(order):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # Custom Oye Abbayi Style
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#2d6a4f"),
        alignment=1, # Center
        spaceAfter=12
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor("#2d6a4f"),
        spaceAfter=10
    )

    # 1. LOGO & BRANDING
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=0.8*inch, height=0.8*inch)
        elements.append(logo)
    
    elements.append(Paragraph("Oye Abbayi - Fresh from Farmers", title_style))
    elements.append(Spacer(1, 0.2*inch))

    # 2. ORDER INFO & CUSTOMER INFO
    info_data = [
        [Paragraph(f"<b>Order ID:</b> #{order.id}", styles['Normal']), Paragraph(f"<b>Date:</b> {order.created_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal'])],
        [Paragraph(f"<b>Customer:</b> {order.user.get_full_name() or order.user.username}", styles['Normal']), Paragraph(f"<b>Phone:</b> {order.phone_number or 'N/A'}", styles['Normal'])],
        [Paragraph(f"<b>Address:</b> {order.address or 'N/A'}", styles['Normal']), Paragraph(f"<b>Pincode:</b> {order.pin_code or 'N/A'}", styles['Normal'])]
    ]
    
    info_table = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))

    # 3. ITEMS TABLE
    elements.append(Paragraph("Items Ordered", header_style))
    
    table_data = [["Product", "Quantity", "Unit Price", "Subtotal"]]
    for item in order.items.all():
        table_data.append([
            item.product.name,
            str(item.quantity),
            f"Rs.{item.price} / {item.product.unit}",
            f"Rs.{item.subtotal()}"
        ])
    
    table_data.append(["", "", "<b>Grand Total</b>", f"<b>Rs.{order.total_amount}</b>"])
    
    item_table = Table(table_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2d6a4f")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,1), (0,-1), 'LEFT'), # Product name left
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor("#f8fdf8")),
        ('GRID', (0,0), (-1,-2), 1, colors.HexColor("#e9ecef")),
        ('LINEBELOW', (0,-1), (-1,-1), 2, colors.HexColor("#2d6a4f")),
        ('TOPPADDING', (0,-1), (-1,-1), 10),
    ]))
    
    elements.append(item_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # 4. FOOTER NOTE
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=1)
    elements.append(Paragraph("Thank you for shopping with Oye Abbayi! Your support helps local farmers.", footer_style))
    elements.append(Paragraph("This is a computer-generated invoice.", footer_style))

    # BUILD PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
