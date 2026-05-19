from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from app.resume_parser import (
    extract_text_from_pdf,
    extract_name,
    extract_email,
    extract_phone,
    extract_education,
    extract_experience
)

from app.matcher import (
    calculate_match_score,
    get_skill_analysis,
    get_hiring_recommendation
)

from app.report_generator import generate_pdf_report

app = FastAPI()

templates = Jinja2Templates(directory="templates")

os.makedirs("reports", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/reports", StaticFiles(directory="reports"), name="reports")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/match-resume/")
async def match_resume(
    request: Request,
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...)
):
    results = []

    for resume in resumes:
        resume_text = extract_text_from_pdf(resume.file)

        match_score = calculate_match_score(
            job_description,
            resume_text
        )

        skill_analysis = get_skill_analysis(
            job_description,
            resume_text
        )

        hiring_recommendation = get_hiring_recommendation(
            match_score
        )

        result = {
            "resume_name": resume.filename,
            "candidate_name": extract_name(resume_text),
            "email": extract_email(resume_text),
            "phone": extract_phone(resume_text),
            "education": extract_education(resume_text),
            "experience": extract_experience(resume_text),
            "match_score": match_score,
            "hiring_recommendation": hiring_recommendation,
            "matched_skills": skill_analysis["matched_skills"],
            "missing_skills": skill_analysis["missing_skills"],
            "interview_questions": skill_analysis["interview_questions"],
            "top_keywords": skill_analysis["top_keywords"],
            "feedback": skill_analysis["feedback"],
            "improvement_suggestions": skill_analysis["improvement_suggestions"]
        }

        report_path = generate_pdf_report(result)

        result["report_path"] = "/" + report_path.replace("\\", "/")

        results.append(result)

    results = sorted(
        results,
        key=lambda x: x["match_score"],
        reverse=True
    )

    total_resumes = len(results)

    highest_score = max(
        [r["match_score"] for r in results],
        default=0
    )

    average_score = round(
        sum([r["match_score"] for r in results]) / total_resumes,
        2
    ) if total_resumes > 0 else 0

    analytics = {
        "total_resumes": total_resumes,
        "highest_score": highest_score,
        "average_score": average_score,
        "strong_hire_count": len([
            r for r in results
            if r["hiring_recommendation"] == "Strong Hire"
        ]),
        "moderate_hire_count": len([
            r for r in results
            if r["hiring_recommendation"] == "Moderate Hire"
        ]),
        "low_match_count": len([
            r for r in results
            if r["hiring_recommendation"] == "Low Match"
        ])
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": results,
            "analytics": analytics
        }
    )