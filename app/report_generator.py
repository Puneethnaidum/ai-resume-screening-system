from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generate_pdf_report(result):
    reports_folder = "reports"

    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)

    file_name = result["resume_name"].replace(".pdf", "_report.pdf")
    file_path = os.path.join(reports_folder, file_name)

    pdf = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "AI Resume Screening Report")

    y -= 40

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Candidate Name: {result['candidate_name']}")

    y -= 22
    pdf.drawString(50, y, f"Email: {result['email']}")

    y -= 22
    pdf.drawString(50, y, f"Phone: {result['phone']}")

    y -= 22
    pdf.drawString(50, y, f"Experience: {result['experience']}")

    y -= 22
    pdf.drawString(
        50,
        y,
        f"Education Keywords: {', '.join(result['education']) or 'Not Found'}"
    )

    y -= 22
    pdf.drawString(50, y, f"Match Score: {result['match_score']}%")

    y -= 22
    pdf.drawString(
        50,
        y,
        f"Hiring Recommendation: {result['hiring_recommendation']}"
    )

    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Matched Skills:")

    y -= 25
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, y, ", ".join(result["matched_skills"]) or "None")

    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Missing Skills:")

    y -= 25
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, y, ", ".join(result["missing_skills"]) or "None")

    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Top Resume Keywords:")

    y -= 25
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, y, ", ".join(result["top_keywords"]) or "None")

    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "AI Resume Feedback:")

    y -= 25
    pdf.setFont("Helvetica", 12)

    for feedback in result["feedback"]:
        pdf.drawString(70, y, f"- {feedback}")
        y -= 20

    y -= 15
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Resume Improvement Suggestions:")

    y -= 25
    pdf.setFont("Helvetica", 12)

    for suggestion in result["improvement_suggestions"]:
        pdf.drawString(70, y, f"- {suggestion}")
        y -= 20

    y -= 15
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Suggested Interview Questions:")

    y -= 25
    pdf.setFont("Helvetica", 12)

    for index, question in enumerate(
        result["interview_questions"],
        start=1
    ):
        pdf.drawString(70, y, f"{index}. {question}")
        y -= 20

    pdf.save()

    return file_path