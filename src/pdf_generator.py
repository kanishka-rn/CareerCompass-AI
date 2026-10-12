"""
Professional PDF Report Generator for CareerCompass AI using ReportLab
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)

def generate_career_report_pdf(
    age: int,
    education: str,
    skills: str,
    interests: str,
    result: dict
) -> bytes:
    """
    Generates a beautifully formatted, comprehensive Career Report as a PDF byte buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1e3a8a")     # Deep blue
    secondary_color = colors.HexColor("#0284c7")   # Bright cyan
    text_color = colors.HexColor("#1e293b")        # Slate 800
    subtle_bg = colors.HexColor("#f8fafc")         # Light slate

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=0
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=text_color
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=text_color,
        leftIndent=15
    )

    story = []

    # Header Title & Metadata
    story.append(Paragraph("CareerCompass AI", title_style))
    story.append(Paragraph("Personalized Career Recommendation & Strategic Roadmap", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2, color=secondary_color, spaceAfter=12))

    # Candidate Profile Summary Table
    profile_data = [
        [
            Paragraph("<b>Age:</b>", body_style), Paragraph(str(age), body_style),
            Paragraph("<b>Date:</b>", body_style), Paragraph(datetime.now().strftime("%B %d, %Y"), body_style)
        ],
        [
            Paragraph("<b>Education:</b>", body_style), Paragraph(education or "Not specified", body_style),
            Paragraph("<b>Status:</b>", body_style), Paragraph("Completed Analysis", body_style)
        ],
        [
            Paragraph("<b>Provided Skills:</b>", body_style), Paragraph(skills or "None", body_style),
            Paragraph("<b>Interests:</b>", body_style), Paragraph(interests or "None", body_style)
        ]
    ]

    profile_table = Table(profile_data, colWidths=[90, 175, 75, 190])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), subtle_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 14))

    # Recommendation Headline Box
    career_domain = result.get("career_domain", "Undetermined")
    confidence = result.get("confidence", 0.0) * 100
    skill_match = result.get("skill_match", 0.0)

    score_data = [
        [
            Paragraph("<b>Recommended Career Domain</b>", subtitle_style),
            Paragraph("<b>AI Confidence</b>", subtitle_style),
            Paragraph("<b>Skill Match</b>", subtitle_style)
        ],
        [
            Paragraph(f"<font size=13 color='#1e3a8a'><b>{career_domain}</b></font>", body_style),
            Paragraph(f"<font size=13 color='#059669'><b>{confidence:.1f}%</b></font>", body_style),
            Paragraph(f"<font size=13 color='#0284c7'><b>{skill_match:.1f}%</b></font>", body_style)
        ]
    ]
    score_table = Table(score_data, colWidths=[240, 145, 145])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#bfdbfe")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dbeafe")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 14))

    # Suggested Career Roles
    career_roles = result.get("career_roles", [])
    if career_roles:
        story.append(Paragraph("Suggested Career Roles", h1_style))
        for role in career_roles:
            story.append(Paragraph(f"• <b>{role}</b>", bullet_style))
        story.append(Spacer(1, 10))

    # Skill Gap Analysis Section
    story.append(Paragraph("Skill Gap & Competency Analysis", h1_style))
    
    matched_skills = result.get("matched_skills", [])
    missing_skills = result.get("missing_skills", [])
    recommended_skills = result.get("recommended_skills", [])

    matched_text = ", ".join(matched_skills) if matched_skills else "No direct matches identified."
    missing_text = ", ".join(missing_skills) if missing_skills else "No critical gaps identified."
    rec_text = ", ".join(recommended_skills) if recommended_skills else "Continue advancing technical depth."

    skills_data = [
        [Paragraph("<b>Skills You Have:</b>", body_style), Paragraph(f"<font color='#059669'>{matched_text}</font>", body_style)],
        [Paragraph("<b>Skills To Improve:</b>", body_style), Paragraph(f"<font color='#dc2626'>{missing_text}</font>", body_style)],
        [Paragraph("<b>Recommended Skills:</b>", body_style), Paragraph(f"<font color='#2563eb'>{rec_text}</font>", body_style)],
    ]
    skills_table = Table(skills_data, colWidths=[140, 390])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), subtle_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 14))

    # Personalized Roadmap
    roadmap = result.get("roadmap", [])
    if roadmap:
        story.append(KeepTogether([
            Paragraph("Personalized Career Learning Roadmap", h1_style),
            Spacer(1, 4)
        ]))
        for i, step in enumerate(roadmap, start=1):
            step_box = [
                [Paragraph(f"<b>STEP {i}</b>", subtitle_style)],
                [Paragraph(step, body_style)]
            ]
            step_table = Table(step_box, colWidths=[530])
            step_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(step_table)
            story.append(Spacer(1, 6))

    # Footer note
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
    footer_style = ParagraphStyle(
        "Footer_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    )
    story.append(Paragraph("Generated by CareerCompass AI • https://github.com/kanishka-rn/CareerCompass-AI", footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
