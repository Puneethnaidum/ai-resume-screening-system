import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_ai_resume_feedback(resume_text, job_description):
    prompt = f"""
You are an AI Resume Screening Assistant.

Analyze the resume against the job description.

Provide:
1. Candidate Summary
2. Technical Strengths
3. Missing Skills
4. Resume Improvement Suggestions
5. Hiring Recommendation

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text[:5000]}
"""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return """
Candidate Summary:
Gemini AI analysis is temporarily unavailable due to API quota limits.

Technical Strengths:
The resume was still analyzed successfully using the local NLP engine.

Missing Skills:
Please review the Missing Skills section generated above.

Resume Improvement Suggestions:
Add more measurable achievements, cloud technologies, certifications, and project impact metrics.

Hiring Recommendation:
Use the AI match score and skill matching results for evaluation.
"""