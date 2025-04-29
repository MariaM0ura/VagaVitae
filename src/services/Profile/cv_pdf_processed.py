def generate_resume_pdf(result, output_path):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=60,
        leftMargin=60,
        topMargin=60,
        bottomMargin=60
    )
    
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=26,
        alignment=1,
        textColor=colors.HexColor("#003366"),
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor("#0066cc"),
        spaceAfter=10
    )
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14
    )
    highlight_style = ParagraphStyle(
        'HighlightStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14
    )
    
    # Informações de Contato
    contact = result["personalized_resume"]["contact"]
    elements.append(Paragraph(contact['name'], title_style))
    elements.append(Paragraph(f"Email: {contact['email']}", normal_style))
    elements.append(Paragraph(f"LinkedIn: {contact['linkedin']}", normal_style))
    elements.append(Spacer(1, 20))

    # Resumo Profissional
    elements.append(Paragraph("🧠 Resumo Profissional", heading_style))
    elements.append(Paragraph(result["personalized_resume"]["professional_summary"], normal_style))
    elements.append(Spacer(1, 20))

    # Objetivo Profissional
    elements.append(Paragraph("🎯 Objetivo Profissional", heading_style))
    elements.append(Paragraph(result["personalized_resume"]["career_objective"], normal_style))
    elements.append(Spacer(1, 20))

    # Separador
    elements.append(Table(
        [[" "]],
        colWidths=[doc.width],
        style=TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#0066cc"))
        ])
    ))
    elements.append(Spacer(1, 20))

    # Formação Acadêmica
    elements.append(Paragraph("🎓 Formação Acadêmica", heading_style))
    acad = result['personalized_resume']['academic_background']
    elements.append(Paragraph(f"<b>{acad['degree']}</b> - {acad['institution']} ({acad['year']})", normal_style))
    elements.append(Spacer(1, 20))

    # Habilidades
    elements.append(Paragraph("🛠️ Habilidades Relevantes", heading_style))
    skills_text = ", ".join(result["personalized_resume"]["skills"])
    elements.append(Paragraph(skills_text, normal_style))
    elements.append(Spacer(1, 20))

    # Experiências
    elements.append(Paragraph("💼 Experiência Profissional", heading_style))
    for exp in result["personalized_resume"]["experiences"]:
        elements.append(Paragraph(f"<b>{exp['role']}</b> - {exp['company']}", normal_style))
        elements.append(Paragraph(f"<i>{exp['duration']}</i>", normal_style))
        elements.append(Paragraph(exp["description"], normal_style))
        elements.append(Spacer(1, 10))
    elements.append(Spacer(1, 20))

    # Análise de Requisitos
    elements.append(Paragraph("📋 Habilidades e Competências", heading_style))
    for req in result["matched_requirements"]:
        elements.append(Paragraph(f"✔ {req}", highlight_style))
        elements.append(Spacer(1, 5))

    # Gerar o PDF
    doc.build(elements)
