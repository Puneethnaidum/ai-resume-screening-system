from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

from app.ai_feedback import get_ai_resume_feedback

import os
import shutil

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": None,
            "analytics": None
        }
    )


@app.post("/match-resume/", response_class=HTMLResponse)
async def match_resume(
    request: Request,
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...),
    use_gemini: str = Form(None)
):
    results = []

    total_score = 0
    strong_hire_count = 0
    moderate_hire_count = 0
    low_match_count = 0

    for resume in resumes:
        file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        with open(file_path, "rb") as pdf_file:
            resume_text = extract_text_from_pdf(pdf_file)

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

        if hiring_recommendation == "Strong Hire":
            strong_hire_count += 1
        elif hiring_recommendation == "Moderate Hire":
            moderate_hire_count += 1
        else:
            low_match_count += 1

        total_score += match_score

        if use_gemini == "yes":
            ai_resume_analysis = get_ai_resume_feedback(
                resume_text,
                job_description
            )
        else:
            ai_resume_analysis = """
Candidate Summary:
Gemini AI analysis was not enabled for this scan.

Technical Strengths:
The resume was analyzed successfully using the local NLP matching engine.

Missing Skills:
Please review the Missing Skills section generated above.

Resume Improvement Suggestions:
Enable Gemini AI Analysis for deeper AI-generated suggestions.

Hiring Recommendation:
Use the match score and skill matching results for evaluation.
"""

        result = {
            "resume_name": resume.filename,
            "candidate_name": extract_name(resume_text),
            "email": extract_email(resume_text),
            "phone": extract_phone(resume_text),
            "experience": extract_experience(resume_text),
            "education": extract_education(resume_text),
            "match_score": round(match_score, 2),
            "matched_skills": skill_analysis["matched_skills"],
            "missing_skills": skill_analysis["missing_skills"],
            "top_keywords": skill_analysis["top_keywords"],
            "hiring_recommendation": hiring_recommendation,
            "feedback": skill_analysis["feedback"],
            "improvement_suggestions": skill_analysis["improvement_suggestions"],
            "ai_resume_analysis": ai_resume_analysis,
            "interview_questions": skill_analysis["interview_questions"],
            "report_path": "#"
        }

        results.append(result)

    results = sorted(
        results,
        key=lambda x: x["match_score"],
        reverse=True
    )

    analytics = {
        "total_resumes": len(results),
        "highest_score": round(max([r["match_score"] for r in results]), 2) if results else 0,
        "average_score": round(total_score / len(results), 2) if results else 0,
        "strong_hire_count": strong_hire_count,
        "moderate_hire_count": moderate_hire_count,
        "low_match_count": low_match_count
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": results,
            "analytics": analytics
        }
    )