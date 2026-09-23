
from datetime import datetime
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Preformatted
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


def create_report(findings):

    if not findings:
        findings = []


    # ========================================================
    # RISK COUNTS
    # ========================================================

    critical = sum(
        1 for f in findings
        if f.get("risk", "").upper() == "CRITICAL"
    )

    high = sum(
        1 for f in findings
        if f.get("risk", "").upper() == "HIGH"
    )

    medium = sum(
        1 for f in findings
        if f.get("risk", "").upper() == "MEDIUM"
    )

    low = sum(
        1 for f in findings
        if f.get("risk", "").upper() == "LOW"
    )


    # ========================================================
    # TOTAL EFFORT
    # ========================================================

    total_days = sum(
        f.get("effort", {}).get(
            "engineering_days",
            0
        )
        for f in findings
    )


    total_resources = sum(
        f.get("effort", {}).get(
            "resources",
            0
        )
        for f in findings
    )


    total_sprints = max(
        1,
        round(total_days / 10 + 0.5)
    )


    # ========================================================
    # PDF PATH
    # ========================================================

    filename = (
        "Y2038_Technical_Assessment_Report.pdf"
    )

    output_path = os.path.join(
        REPORT_DIR,
        filename
    )


    # ========================================================
    # DOCUMENT
    # ========================================================

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20
    )


    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading1"],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10
    )


    subheading_style = ParagraphStyle(
        "SubHeadingCustom",
        parent=styles["Heading2"],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6
    )


    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )


    code_style = ParagraphStyle(
        "CodeCustom",
        parent=styles["Code"],
        fontSize=8,
        leading=10
    )


    story = []


    # ========================================================
    # COVER PAGE
    # ========================================================

    story.append(
        Spacer(1, 100)
    )

    story.append(
        Paragraph(
            "Y2038 TECHNICAL ASSESSMENT REPORT",
            title_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Code Analysis Assistant",
            heading_style
        )
    )

    story.append(
        Spacer(1, 30)
    )

    story.append(
        Paragraph(
            "Automated Code Risk Analysis, "
            "Knowledge Retrieval and "
            "Remediation Assessment",
            normal_style
        )
    )

    story.append(
        Spacer(1, 40)
    )

    story.append(
        Paragraph(
            "Generated: "
            + datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            normal_style
        )
    )

    story.append(
        PageBreak()
    )


    # ========================================================
    # 1. EXECUTIVE SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "1. Executive Summary",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"The automated assessment analyzed "
            f"{len(findings)} finding(s). The assessment "
            f"combines machine-learning based Y2038 "
            f"detection, rule-based validation, "
            f"false-positive suppression and a "
            f"knowledge-base retrieval layer.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 10)
    )


    # ========================================================
    # 2. RISK SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "2. Risk Summary",
            heading_style
        )
    )


    risk_data = [
        ["Risk Level", "Count"],
        ["Critical", str(critical)],
        ["High", str(high)],
        ["Medium", str(medium)],
        ["Low", str(low)]
    ]


    risk_table = Table(
        risk_data,
        colWidths=[250, 100]
    )


    risk_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1,
             colors.black),
            ("ALIGN", (1, 0), (1, -1),
             "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )


    story.append(
        risk_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # 3. BUSINESS RISK
    # ========================================================

    story.append(
        Paragraph(
            "3. Business Risk Assessment",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "Operational Risk: Potential application "
            "or timestamp processing failure for "
            "affected code paths.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    story.append(
        Paragraph(
            "Financial Risk: Identified findings may "
            "result in remediation costs, operational "
            "disruption and potential business impact. "
            "No unsupported monetary values are "
            "invented in this assessment.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    story.append(
        Paragraph(
            "Regulatory Risk: Findings should be tracked "
            "through applicable technology risk, audit "
            "and compliance processes.",
            normal_style
        )
    )


    # ========================================================
    # 4. REMEDIATION EFFORT
    # ========================================================

    story.append(
        Paragraph(
            "4. Remediation Effort Estimation",
            heading_style
        )
    )


    effort_data = [
        ["Metric", "Estimate"],
        ["Engineering Days",
         str(round(total_days, 1))],
        ["Estimated Sprints",
         str(total_sprints)],
        ["Resource Units",
         str(total_resources)]
    ]


    effort_table = Table(
        effort_data,
        colWidths=[250, 100]
    )


    effort_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1,
             colors.black),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )


    story.append(
        effort_table
    )


    story.append(
        Spacer(1, 10)
    )


    story.append(
        Paragraph(
            "Effort estimates are configurable planning "
            "assumptions based on risk, technology and "
            "complexity. They are not actual client "
            "project estimates.",
            normal_style
        )
    )


    # ========================================================
    # 5. REMEDIATION ROADMAP
    # ========================================================

    story.append(
        Paragraph(
            "5. Prioritized Remediation Roadmap",
            heading_style
        )
    )


    roadmap_data = [
        [
            "Priority",
            "Action"
        ],
        [
            "CRITICAL",
            "Immediate remediation"
        ],
        [
            "HIGH",
            "Plan remediation for next quarter"
        ],
        [
            "MEDIUM",
            "Track as technical debt"
        ]
    ]


    roadmap_table = Table(
        roadmap_data,
        colWidths=[120, 230]
    )


    roadmap_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1,
             colors.black),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )


    story.append(
        roadmap_table
    )


    # ========================================================
    # 6. FINDINGS
    # ========================================================

    story.append(
        Paragraph(
            "6. Detailed Findings",
            heading_style
        )
    )


    if not findings:

        story.append(
            Paragraph(
                "No findings were supplied for this report.",
                normal_style
            )
        )


    for index, finding in enumerate(
        findings,
        1
    ):

        story.append(
            Paragraph(
                f"Finding {index}",
                subheading_style
            )
        )


        story.append(
            Paragraph(
                f"<b>Risk:</b> "
                f"{finding.get('risk', 'UNKNOWN')}",
                normal_style
            )
        )


        story.append(
            Paragraph(
                f"<b>Language:</b> "
                f"{finding.get('language', 'UNKNOWN')}",
                normal_style
            )
        )


        story.append(
            Spacer(1, 5)
        )


        code = finding.get(
            "code",
            ""
        )


        if code:

            story.append(
                Paragraph(
                    "<b>Code Snippet:</b>",
                    normal_style
                )
            )

            story.append(
                Preformatted(
                    code,
                    code_style
                )
            )


        story.append(
            Paragraph(
                "<b>Recommendation:</b> "
                + finding.get(
                    "recommendation",
                    "Review the finding."
                ),
                normal_style
            )
        )


        effort = finding.get(
            "effort",
            {}
        )


        story.append(
            Paragraph(
                "<b>Estimated Effort:</b> "
                + str(
                    effort.get(
                        "engineering_days",
                        0
                    )
                )
                + " engineering days",
                normal_style
            )
        )


        story.append(
            Spacer(1, 15)
        )


    # ========================================================
    # 7. METHODOLOGY
    # ========================================================

    story.append(
        PageBreak()
    )


    story.append(
        Paragraph(
            "7. Assessment Methodology",
            heading_style
        )
    )


    methodology = [
        "1. Code is submitted to the Y2038 analysis engine.",
        "2. Existing TF-IDF and SVM models generate an ML prediction.",
        "3. Rule-based checks identify known timestamp patterns.",
        "4. False-positive suppression validates potentially risky integer variables.",
        "5. The knowledge base retrieves similar historical patterns and recommendations.",
        "6. Business risk categories are generated.",
        "7. Remediation effort is estimated.",
        "8. Findings are prioritized using weighted risk factors.",
        "9. Findings are assembled into the technical assessment report."
    ]


    for item in methodology:

        story.append(
            Paragraph(
                item,
                normal_style
            )
        )

        story.append(
            Spacer(1, 5)
        )


    # ========================================================
    # 8. METRICS
    # ========================================================

    story.append(
        Paragraph(
            "8. Assessment Metrics",
            heading_style
        )
    )


    metrics_data = [
        ["Metric", "Value"],
        ["Total Findings", str(len(findings))],
        ["Critical Findings", str(critical)],
        ["High Findings", str(high)],
        ["Medium Findings", str(medium)],
        ["Low Findings", str(low)],
        ["Engineering Days", str(round(total_days, 1))],
        ["Estimated Sprints", str(total_sprints)]
    ]


    metrics_table = Table(
        metrics_data,
        colWidths=[250, 100]
    )


    metrics_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1,
             colors.black),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )


    story.append(
        metrics_table
    )


    # ========================================================
    # 9. CONCLUSION
    # ========================================================

    story.append(
        Paragraph(
            "9. Conclusion",
            heading_style
        )
    )


    story.append(
        Paragraph(
            "The Code Analysis Assistant provides an "
            "automated assessment workflow combining "
            "machine learning, deterministic validation, "
            "false-positive suppression, knowledge "
            "retrieval and remediation planning. "
            "The generated findings can be used as an "
            "engineering planning input and should be "
            "validated by technical stakeholders before "
            "production remediation.",
            normal_style
        )
    )


    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )


    return output_path
