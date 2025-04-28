from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from pathlib import Path


#BUILDING NEW CV
def generate_resume_pdf(result, output_path):
    """
    Generate a PDF resume from the JSON result
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10
    )
    
    # Contact Information
    contact = result["personalized_resume"]["contact"]
    elements.append(Paragraph(f"<para align='center'>{contact['name']}</para>", title_style))
    elements.append(Paragraph(f"<para align='center'>Email: {contact['email']}</para>", styles["Normal"]))
    elements.append(Paragraph(f"<para align='center'>LinkedIn: {contact['linkedin']}</para>", styles["Normal"]))
    elements.append(Spacer(1, 20))
    
    # Add a blue line separator
    elements.append(Spacer(1, 10))
    elements.append(Table(
        [[Paragraph("", styles["Normal"])]],
        colWidths=[doc.width],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.blue),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.blue),
        ])
    ))
    elements.append(Spacer(1, 10))


    # Academic Background
    elements.append(Paragraph("Formação Acadêmica", heading_style))
    elements.append(Paragraph(f"<b>{result['personalized_resume']['academic_background']['degree']}</b>", styles["Normal"]))
    elements.append(Paragraph(f"{result['personalized_resume']['academic_background']['institution']}", styles["Normal"]))  
    elements.append(Paragraph(f"<i>{result['personalized_resume']['academic_background']['year']}</i>", styles["Normal"]))
    elements.append(Spacer(1, 20))
    

    # Skills
    elements.append(Paragraph("Habilidades Relevantes", heading_style))
    skills_text = ", ".join(result["personalized_resume"]["skills"])
    elements.append(Paragraph(skills_text, styles["Normal"]))
    elements.append(Spacer(1, 20))
    
    # Experience
    elements.append(Paragraph("Experiência Profissional", heading_style))
    for exp in result["personalized_resume"]["experiences"]:
        elements.append(Paragraph(f"<b>{exp['role']}</b> - {exp['company']}", styles["Normal"]))
        elements.append(Paragraph(f"<i>{exp['duration']}</i>", styles["Normal"]))
        elements.append(Paragraph(exp["description"], styles["Normal"]))
        elements.append(Spacer(1, 10))
    
    # Requirements Analysis
    elements.append(Paragraph("Habilidades e Competências", heading_style))
    
    # Create table data
    for req in result["matched_requirements"]:
        elements.append(Paragraph(f"✓ {req}", styles["Normal"]))
        elements.append(Spacer(1, 5))
    # Build PDF
    doc.build(elements)