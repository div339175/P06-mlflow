import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (on page > 1)
        if self._pageNumber > 1:
            self.drawString(45, 755, "SCSE3040 — Machine Learning Operations | Practical 06")
            self.drawRightString(612 - 45, 755, "Divakar Maurya (S24CSEU0807) | Batch EB31")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(45, 748, 612 - 45, 748)
            
        # Footer (on all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 45, 28, page_str)
        self.drawString(45, 28, "Bennett University — School of Computer Science Engineering & Technology")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(45, 38, 612 - 45, 38)
        
        self.restoreState()


def create_submission_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=40,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0F172A')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#475569')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=7,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#64748B'),
        spaceBefore=3,
        spaceAfter=6
    )

    link_style = ParagraphStyle(
        'RepoLink',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1D4ED8')
    )

    table_label_style = ParagraphStyle(
        'TableLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1E293B')
    )

    table_val_style = ParagraphStyle(
        'TableValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A')
    )

    elements = []

    # ==================== PAGE 1 ====================
    # Title & Header
    elements.append(Paragraph("SCSE3040: Machine Learning Operations (MLOps)", title_style))
    elements.append(Paragraph("Practical 06: Tracking Runs, Comparing Experiments, and Model Registry with MLflow", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=4, spaceAfter=7))

    # 1. Student & Laboratory Session Details
    elements.append(Paragraph("1. Student &amp; Laboratory Session Details", section_heading))
    
    student_table_data = [
        [Paragraph("Student Name:", table_label_style), Paragraph("Divakar Maurya", table_val_style),
         Paragraph("Batch:", table_label_style), Paragraph("EB31", table_val_style)],
        [Paragraph("Roll Number:", table_label_style), Paragraph("S24CSEU0807", table_val_style),
         Paragraph("Date of Lab Session:", table_label_style), Paragraph("04 October 2026", table_val_style)],
        [Paragraph("Course Name:", table_label_style), Paragraph("SCSE3040 — Machine Learning Operations", table_val_style),
         Paragraph("Academic Session:", table_label_style), Paragraph("2026–2027 (Session L11 / CO5)", table_val_style)]
    ]

    col_widths = [95, 165, 115, 147]
    t_student = Table(student_table_data, colWidths=col_widths)
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    elements.append(t_student)
    elements.append(Spacer(1, 6))

    # 2. Repository Link
    elements.append(Paragraph("2. Repository Link", section_heading))
    repo_url = "https://github.com/div339175/P06-mlflow"
    elements.append(Paragraph(
        f'<font color="#334155">Full Repository URL: </font><a href="{repo_url}"><font color="#1D4ED8"><u><b>{repo_url}</b></u></font></a>',
        link_style
    ))
    elements.append(Spacer(1, 6))

    # 3. Screenshot of MLflow UI Runs Table
    elements.append(Paragraph("3. MLflow UI Runs Table (Parameters and Metrics Side-by-Side)", section_heading))
    elements.append(Paragraph(
        "Screenshot of the MLflow Tracking UI (backend store: <font face='Courier'>sqlite:///work/mlflow.db</font>) showing all 11 runs recorded in the <b>delivery-time</b> experiment. Both metrics (<font face='Courier'>mae_minutes</font>, <font face='Courier'>rmse_minutes</font>) and hyperparameter columns (<font face='Courier'>max_depth</font>, <font face='Courier'>model_type</font>, <font face='Courier'>n_estimators</font>) are clearly visible side by side across models:",
        body_style
    ))
    elements.append(Spacer(1, 4))

    table_img_path = "runs_table_final.png"
    if os.path.exists(table_img_path):
        disp_width = 522
        disp_height = 522 * (1100 / 2000)
        img_table = Image(table_img_path, width=disp_width, height=disp_height)
        elements.append(img_table)
        elements.append(Paragraph("Figure 1: MLflow UI experiment runs table displaying 11 tracked runs with metrics and hyperparameters side-by-side.", caption_style))

    # PageBreak to cleanly place Section 4, 5, 6 on Page 2
    elements.append(PageBreak())

    # ==================== PAGE 2 ====================
    # 4. Screenshot of Run Detail Page for Best Run
    elements.append(Paragraph("4. Run Detail Page for Selected Best Run (linear-baseline)", section_heading))
    elements.append(Paragraph(
        "Detailed view of the winning run (<font face='Courier'>linear-baseline</font>) in MLflow UI showing execution metadata, tracked parameters, and recorded evaluation metrics:",
        body_style
    ))
    elements.append(Spacer(1, 4))

    detail_img_path = "run_detail_best_clean.png"
    if os.path.exists(detail_img_path):
        disp_width = 522
        disp_height = 522 * (1050 / 1800)
        img_detail = Image(detail_img_path, width=disp_width, height=disp_height)
        elements.append(img_detail)
        elements.append(Paragraph("Figure 2: MLflow UI run detail page for selected run linear-baseline (Run ID: 2b20306d7ad34f2e8d8f26d08ad4c7e0).", caption_style))
    elements.append(Spacer(1, 8))

    # 5. Run ID, Metric, and Justification
    elements.append(Paragraph("5. Best Run Selection &amp; Justification", section_heading))
    
    selection_table_data = [
        [Paragraph("Selected Run Name:", table_label_style), Paragraph("<b>linear-baseline</b>", table_val_style),
         Paragraph("Logged Model Type:", table_label_style), Paragraph("<font face='Courier'>LinearRegression</font>", table_val_style)],
        [Paragraph("Selected Run ID:", table_label_style), Paragraph("<font face='Courier'>2b20306d7ad34f2e8d8f26d08ad4c7e0</font>", table_val_style),
         Paragraph("Best Test Metric:", table_label_style), Paragraph("<b>MAE = 1.925 minutes</b> (1.92465 min)", table_val_style)],
        [Paragraph("Model Registry Status:", table_label_style), Paragraph("<font face='Courier'>delivery-time-model</font> (v1 champion: rf-n300-d12, MAE 2.375)", table_val_style),
         Paragraph("Total Runs Compared:", table_label_style), Paragraph("11 runs across 3 model families", table_val_style)]
    ]
    t_sel = Table(selection_table_data, colWidths=col_widths)
    t_sel.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    elements.append(t_sel)
    elements.append(Spacer(1, 6))

    justification_text = (
        "<b>Selection Rationale:</b> I selected the <font face='Courier'>linear-baseline</font> run "
        "(Run ID: <font face='Courier'>2b20306d7ad34f2e8d8f26d08ad4c7e0</font>) because it achieved the lowest Mean Absolute "
        "Error of <b>1.925 minutes</b> across the entire experiment, outperforming the decision tree models "
        "(worst MAE: 5.834 minutes for depth 2) by 3.909 minutes and beating the best random forest configuration "
        "(<font face='Courier'>rf-n300-d12</font> / <font face='Courier'>champion</font> with MAE 2.375 minutes) by 0.450 minutes "
        "because the delivery duration in this benchmark is governed predominantly by direct linear relationships with distance and preparation time."
    )
    elements.append(Paragraph(justification_text, body_style))
    elements.append(Spacer(1, 10))

    # 6. AI Use Disclosure
    elements.append(Paragraph("6. AI Use Disclosure", section_heading))
    disclosure_box_data = [
        [Paragraph("<b>Disclosure:</b> None", body_style)]
    ]
    t_disc = Table(disclosure_box_data, colWidths=[522])
    t_disc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_disc)

    # Build document
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Generated {output_path} successfully!")

if __name__ == "__main__":
    create_submission_pdf("SCSE3040_P06_S24CSEU0807.pdf")
