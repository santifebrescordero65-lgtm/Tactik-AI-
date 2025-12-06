"""
TACTIK AI - PDF Report Generator
Generates professional PDF reports with transparency cards
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


def generate_pdf_report(session_id: str, report: Dict[str, Any]) -> str:
    """
    Generate PDF report from TACTIK Advisor data

    Args:
        session_id: Session identifier
        report: Report data from generate_tactik_advisor()

    Returns:
        Path to generated PDF file
    """
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    pdf_path = reports_dir / f"tactik_report_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Container for PDF elements
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY
    )

    # ═══════════════════════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════════════════════

    story.append(Spacer(1, 1*inch))

    title = Paragraph("TACTIK AI 5.3 PREMIUM", title_style)
    story.append(title)

    subtitle = Paragraph(
        "Strategic Intelligence Report<br/>Scientific Validation & Transparency",
        ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=colors.HexColor('#7f8c8d'))
    )
    story.append(subtitle)
    story.append(Spacer(1, 0.5*inch))

    # Session info box
    session_summary = report['session_summary']
    session_data = [
        ['Session ID:', session_summary['session_id']],
        ['Goal:', session_summary['goal']],
        ['Total Turns:', str(session_summary['total_turns'])],
        ['TACTIK Score:', f"{session_summary['tactik_score']}/10"],
        ['Duration:', session_summary['duration']],
        ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    ]

    session_table = Table(session_data, colWidths=[2*inch, 4*inch])
    session_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
    ]))

    story.append(session_table)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # AVATAR VALIDATION
    # ═══════════════════════════════════════════════════════════════════

    story.append(Paragraph("Avatar Validation Metrics", heading_style))
    story.append(Spacer(1, 0.2*inch))

    avatar_scores = report['avatar_avda_scores']

    for avatar_id, avda in avatar_scores.items():
        avatar_data = [
            ['Avatar ID', avatar_id],
            ['AVDA Score', f"{avda['avda_score']}%"],
            ['Classification', avda['classification']],
            ['Accuracy', f"{avda['accuracy']}%"],
            ['Source Coverage', f"{avda['source_coverage']}%"],
            ['Drift Risk', f"{avda['drift_risk']}%"],
            ['GT Quality', f"{avda['ground_truth_quality']}%"],
            ['Confidence Interval', f"[{avda['confidence_interval'][0]}% - {avda['confidence_interval'][1]}%]"]
        ]

        avatar_table = Table(avatar_data, colWidths=[2.5*inch, 3.5*inch])
        avatar_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ecf0f1')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
        ]))

        story.append(avatar_table)
        story.append(Spacer(1, 0.3*inch))

    # ═══════════════════════════════════════════════════════════════════
    # KEY INSIGHTS
    # ═══════════════════════════════════════════════════════════════════

    story.append(Paragraph("Key Insights", heading_style))
    story.append(Spacer(1, 0.1*inch))

    for insight in report['key_insights']:
        story.append(Paragraph(f"• {insight}", body_style))
        story.append(Spacer(1, 0.1*inch))

    story.append(Spacer(1, 0.3*inch))

    # ═══════════════════════════════════════════════════════════════════
    # RECOMMENDATIONS
    # ═══════════════════════════════════════════════════════════════════

    story.append(Paragraph("Strategic Recommendations", heading_style))
    story.append(Spacer(1, 0.1*inch))

    for rec in report['recommendations']:
        story.append(Paragraph(rec, body_style))
        story.append(Spacer(1, 0.1*inch))

    story.append(Spacer(1, 0.3*inch))

    # ═══════════════════════════════════════════════════════════════════
    # 72-HOUR ACTION PLAN
    # ═══════════════════════════════════════════════════════════════════

    story.append(Paragraph("72-Hour Action Plan", heading_style))
    story.append(Spacer(1, 0.2*inch))

    action_data = [['Timeframe', 'Action', 'Priority']]

    for action in report['action_plan_72h']:
        action_data.append([
            action['timeframe'],
            action['action'],
            action['priority']
        ])

    action_table = Table(action_data, colWidths=[1.5*inch, 3.5*inch, 1*inch])
    action_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))

    story.append(action_table)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # TRANSPARENCY CARD
    # ═══════════════════════════════════════════════════════════════════

    story.append(Paragraph("Transparency Card", heading_style))
    story.append(Spacer(1, 0.2*inch))

    tc = report['transparency_card']

    story.append(Paragraph(f"<b>Certification:</b> {tc['certification']}", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"<b>Timestamp:</b> {tc['timestamp']}", body_style))
    story.append(Spacer(1, 0.2*inch))

    # Quality Assurance
    qa = tc['quality_assurance']
    qa_data = [
        ['Quality Metric', 'Value'],
        ['Empathy Pauses', str(qa['empathy_pauses'])],
        ['Backflow Corrections', str(qa['backflow_corrections'])],
        ['Avg TACTIK Score', f"{qa['avg_tactik_score']}/10"]
    ]

    qa_table = Table(qa_data, colWidths=[3*inch, 3*inch])
    qa_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
    ]))

    story.append(qa_table)
    story.append(Spacer(1, 0.3*inch))

    # Usage Guidelines
    guidelines = tc['usage_guidelines']
    story.append(Paragraph("<b>Usage Guidelines:</b>", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"<b>Recommended Use:</b> {guidelines['recommended_use']}", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"<b>Validation Required:</b> {guidelines['validation_required']}", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"<b>Update Frequency:</b> {guidelines['update_frequency']}", body_style))

    story.append(Spacer(1, 0.5*inch))

    # Footer
    footer = Paragraph(
        "TACTIK AI 5.3 Premium Edition - Strategic Intelligence with Scientific Validation",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER, textColor=colors.HexColor('#95a5a6'))
    )
    story.append(footer)

    # Build PDF
    doc.build(story)

    return str(pdf_path)


if __name__ == "__main__":
    # Test with sample data
    sample_report = {
        "session_summary": {
            "session_id": "test_001",
            "goal": "Test PDF generation",
            "total_turns": 5,
            "tactik_score": 8.5,
            "duration": "10 minutes"
        },
        "avatar_avda_scores": {
            "test_avatar": {
                "avda_score": 84.0,
                "classification": "HIGH FIDELITY",
                "accuracy": 86.0,
                "source_coverage": 86.0,
                "drift_risk": 30.0,
                "ground_truth_quality": 87.5,
                "confidence_interval": [79.0, 92.0]
            }
        },
        "key_insights": [
            "Test insight 1",
            "Test insight 2"
        ],
        "recommendations": [
            "✓ Test recommendation 1",
            "⚠ Test recommendation 2"
        ],
        "action_plan_72h": [
            {"timeframe": "24 hours", "action": "Test action 1", "priority": "HIGH"},
            {"timeframe": "48 hours", "action": "Test action 2", "priority": "MEDIUM"}
        ],
        "transparency_card": {
            "certification": "TACTIK 5.3 Premium - Scientific Validation",
            "timestamp": datetime.now().isoformat(),
            "quality_assurance": {
                "empathy_pauses": 0,
                "backflow_corrections": 1,
                "avg_tactik_score": 8.5
            },
            "usage_guidelines": {
                "recommended_use": "SUITABLE for strategic preparation",
                "validation_required": "Cross-verify critical insights",
                "update_frequency": "Re-validate quarterly"
            }
        }
    }

    pdf_path = generate_pdf_report("test_001", sample_report)
    print(f"✅ PDF generated: {pdf_path}")
