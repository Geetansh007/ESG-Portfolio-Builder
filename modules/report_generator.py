from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(filename, portfolio_df, impact_text):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("InsightAgent ESG Impact Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Portfolio Summary:", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    for _, row in portfolio_df.iterrows():
        text = f"{row['Company']} - Investment: {round(row['Investment_Amount'],2)}"
        elements.append(Paragraph(text, styles["Normal"]))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Impact Explanation:", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(impact_text, styles["Normal"]))

    doc.build(elements)
