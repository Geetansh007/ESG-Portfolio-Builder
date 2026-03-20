
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

def generate_report(filename, portfolio_df, impact_text):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    # Custom styles for better design
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=22, textColor=colors.HexColor('#6366f1'), spaceAfter=16)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#1e293b'), spaceAfter=10)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#1e293b'))
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#ffffff'), backColor=colors.HexColor('#6366f1'), alignment=1)

    elements = []

    # Title
    elements.append(Paragraph("🌍 ESG Investment & Impact Report", title_style))
    elements.append(Spacer(1, 8))

    # Portfolio Table
    elements.append(Paragraph("Portfolio Overview", section_style))
    table_data = [[
        Paragraph("<b>Company</b>", table_header_style),
        Paragraph("<b>Industry</b>", table_header_style),
        Paragraph("<b>Investment (₹)</b>", table_header_style),
        Paragraph("<b>ESG Score</b>", table_header_style),
        Paragraph("<b>1Y Return</b>", table_header_style),
        Paragraph("<b>3Y Return</b>", table_header_style),
        Paragraph("<b>Allocation %</b>", table_header_style),
        Paragraph("<b>ESG Impact</b>", table_header_style)
    ]]
    for _, row in portfolio_df.iterrows():
        esg_score = row.get('ESG_score', 'N/A')
        ret_1y = row.get('Return_1Y', None)
        ret_3y = row.get('Return_3Y', None)
        alloc_pct = row.get('Allocation_%', 0)
        # Simple ESG impact explanation
        if esg_score != 'N/A' and esg_score >= 85:
            esg_impact = "Strong positive ESG impact"
        elif esg_score != 'N/A' and esg_score >= 75:
            esg_impact = "Good ESG performance"
        elif esg_score != 'N/A' and esg_score >= 65:
            esg_impact = "Moderate ESG impact"
        else:
            esg_impact = "Needs improvement"
        table_data.append([
            row.get('Company', ''),
            row.get('Industry', ''),
            f"{round(row.get('Investment_Amount', 0), 2)}",
            f"{esg_score:.1f}" if esg_score != 'N/A' else 'N/A',
            f"{ret_1y:.2f}%" if ret_1y is not None else 'N/A',
            f"{ret_3y:.2f}%" if ret_3y is not None else 'N/A',
            f"{alloc_pct:.1%}",
            esg_impact
        ])
    table = Table(table_data, colWidths=[80, 80, 70, 60, 60, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Detailed ESG Impact Breakdown
    elements.append(Paragraph("<b>Detailed ESG Impact Analysis</b>", section_style))
    # Industry averages for ESG
    import pandas as pd
    from modules.esg_scorer import get_industry_averages
    industry_averages = get_industry_averages(portfolio_df)
    for _, row in portfolio_df.iterrows():
        company = row.get('Company', '')
        industry = row.get('Industry', '')
        e = row.get('E_score', 'N/A')
        s = row.get('S_score', 'N/A')
        g = row.get('G_score', 'N/A')
        esg_score = row.get('ESG_score', 'N/A')
        investment = row.get('Investment_Amount', 'N/A')
        e_avg = industry_averages[industry]['E_score']
        s_avg = industry_averages[industry]['S_score']
        g_avg = industry_averages[industry]['G_score']
        e_diff = e - e_avg if e != 'N/A' else 0
        s_diff = s - s_avg if s != 'N/A' else 0
        g_diff = g - g_avg if g != 'N/A' else 0
        elements.append(Paragraph(f"<b>{company}</b> ({industry})", normal_style))
        elements.append(Paragraph(
            f"Investment: ₹{investment} | ESG Score: {esg_score}", normal_style))
        elements.append(Paragraph(
            f"Environmental: <b>{e}</b> ({e_diff:+.1f} vs industry avg {e_avg:.1f}) | "
            f"Social: <b>{s}</b> ({s_diff:+.1f} vs industry avg {s_avg:.1f}) | "
            f"Governance: <b>{g}</b> ({g_diff:+.1f} vs industry avg {g_avg:.1f})", normal_style))
        # Custom impact summary
        summary = []
        if e_diff > 0:
            summary.append(f"Environmental score is {e_diff:.1f} above industry average.")
        if s_diff > 0:
            summary.append(f"Social score is {s_diff:.1f} above industry average.")
        if g_diff > 0:
            summary.append(f"Governance score is {g_diff:.1f} above industry average.")
        if not summary:
            summary.append("ESG scores are in line with or below industry averages.")
        elements.append(Paragraph(" ".join(summary), normal_style))
        elements.append(Spacer(1, 8))

    # Past Returns Note
    elements.append(Paragraph("<font size=9 color='#64748b'>*Past Returns are based on the Financial Score from the ESG dataset and are for illustration only.</font>", styles['Normal']))

    doc.build(elements)
