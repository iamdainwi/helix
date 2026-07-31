"""
Premium Brand DNA PDF Generator
Uses ReportLab Platypus engine for beautiful reflowing typography and layouts.
"""
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def hex_to_rgb_tuple(hex_str: str):
    """Convert CSS hex to (r, g, b) normalized 0.0-1.0"""
    if not hex_str or not str(hex_str).strip().startswith("#"):
        return (0.9, 0.9, 0.9)
    h = str(hex_str).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) in (6, 8):
        try:
            return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)
        except ValueError:
            pass
    return (0.9, 0.9, 0.9)

class ColorSwatch(Flowable):
    def __init__(self, width, height, hex_color, rgb):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.hex_color = str(hex_color).upper()
        self.r, self.g, self.b = rgb

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColorRGB(self.r, self.g, self.b)
        self.canv.setStrokeColorRGB(0.85, 0.85, 0.85)
        self.canv.setLineWidth(0.5)
        
        # Draw a rounded rectangle for the color block
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)
        
        # Calculate contrast text color (luma)
        luma = 0.299 * self.r + 0.587 * self.g + 0.114 * self.b
        if luma > 0.6:
            self.canv.setFillColorRGB(0.1, 0.1, 0.1) # Dark text on light swatch
        else:
            self.canv.setFillColorRGB(1, 1, 1)       # Light text on dark swatch
        
        self.canv.setFont("Helvetica-Bold", 8)
        # Center the hex code in the box
        self.canv.drawCentredString(self.width / 2.0, self.height / 2.0 - 2.5, self.hex_color)
        self.canv.restoreState()

class HorizontalLine(Flowable):
    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width
        
    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColorRGB(0.9, 0.9, 0.9)
        self.canv.setLineWidth(1)
        self.canv.line(0, 0, self.width, 0)
        self.canv.restoreState()

def build_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='PremiumTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#111111"),
        spaceAfter=8,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumSubtitle',
        fontName='Helvetica-Oblique',
        fontSize=13,
        leading=20,
        textColor=colors.HexColor("#666666"),
        spaceAfter=20,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumHeading2',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#222222"),
        spaceBefore=22,
        spaceAfter=10,
        alignment=TA_LEFT
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumBody',
        fontName='Helvetica',
        fontSize=10,
        leading=16,
        textColor=colors.HexColor("#444444"),
        alignment=TA_LEFT
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumBullet',
        parent=styles['PremiumBody'],
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=6,
    ))
    
    return styles

def _escape(text):
    if text is None:
        return ""
    text = str(text)
    # XML escaping for ReportLab Paragraphs
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text

def generate_brand_dna_pdf(dna: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=25*mm,
        bottomMargin=30*mm  # Ensure space for absolute footer
    )
    
    styles = build_styles()
    story = []
    
    # ── Title & Tagline ──
    brand_name = dna.get("brand_name") or "Brand DNA"
    story.append(Paragraph(_escape(brand_name), styles['PremiumTitle']))
    
    tagline = dna.get("tagline")
    if tagline:
        story.append(Paragraph(f'"{_escape(tagline)}"', styles['PremiumSubtitle']))
        
    story.append(Spacer(1, 5*mm))
    story.append(HorizontalLine(A4[0] - 40*mm))
    story.append(Spacer(1, 5*mm))
    
    # ── Text Sections ──
    def add_text_section(title, content):
        if not content:
            return
        story.append(KeepTogether([
            Paragraph(title, styles['PremiumHeading2']),
            Paragraph(_escape(content), styles['PremiumBody'])
        ]))
        
    def add_bullet_section(title, items):
        if not items:
            return
        section_story = [Paragraph(title, styles['PremiumHeading2'])]
        for item in items:
            section_story.append(Paragraph(_escape(str(item)), styles['PremiumBullet'], bulletText="•"))
        story.append(KeepTogether(section_story))

    add_text_section("Tone of Voice", dna.get("tone_of_voice"))
    add_bullet_section("Brand Personality", dna.get("brand_personality", []))
    add_text_section("Target Audience", dna.get("audience"))
    add_bullet_section("Core Values", dna.get("values", []))
    add_text_section("Typography", dna.get("typography"))
    add_text_section("Design Style", dna.get("design_style"))
    
    # ── Color Palette ──
    raw_colors = dna.get("color_palette", [])
    if isinstance(raw_colors, str):
        raw_colors = [c.strip() for c in raw_colors.split(",") if c.strip()]
        
    if raw_colors:
        story.append(Paragraph("Color Palette", styles['PremiumHeading2']))
        story.append(Spacer(1, 5*mm))
        
        swatches = []
        for hex_code in raw_colors:
            rgb = hex_to_rgb_tuple(hex_code)
            swatch = ColorSwatch(width=30*mm, height=20*mm, hex_color=hex_code, rgb=rgb)
            swatches.append(swatch)
            
        # Group swatches into rows of 5
        cols = 5
        table_data = []
        for i in range(0, len(swatches), cols):
            row = swatches[i:i+cols]
            # Pad the row with empty strings if it has fewer than `cols` elements
            while len(row) < cols:
                row.append("")
            table_data.append(row)
            
        if table_data:
            # Table prevents layout glitches and handles reflowing rows naturally
            color_table = Table(
                table_data, 
                colWidths=[33*mm]*cols,
                rowHeights=[24*mm]*len(table_data)
            )
            color_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
            ]))
            story.append(color_table)
            
    # ── Dynamic Footer (Absolute bottom of every page) ──
    def on_page(canvas, doc):
        canvas.saveState()
        
        # Top accent line
        canvas.setStrokeColorRGB(0.92, 0.92, 0.92)
        canvas.setLineWidth(0.5)
        canvas.line(20*mm, A4[1] - 15*mm, A4[0] - 20*mm, A4[1] - 15*mm)

        # Bottom accent line (Footer separator)
        canvas.line(20*mm, 20*mm, A4[0] - 20*mm, 20*mm)

        # Bottom footer text & page number
        canvas.setFont('Helvetica-Oblique', 8)
        canvas.setFillColorRGB(0.6, 0.6, 0.6)
        footer_text = f"Brand DNA extracted by Helix. Generated for {_escape(brand_name)}.   |   Page {doc.page}"
        canvas.drawCentredString(A4[0] / 2.0, 14*mm, footer_text)
        
        canvas.restoreState()
    
    # Render PDF
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
