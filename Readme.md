# AI Resume Screening System

An AI-powered Resume Screening System built using FastAPI, NLP, and Gemini AI to analyze resumes against job descriptions. The system performs ATS-style resume scoring, skill matching, AI-powered resume analysis, candidate ranking, interview question generation, and PDF report generation.

---

# Features

## Resume Parsing
- Extracts text from uploaded PDF resumes
- Identifies:
  - Candidate Name
  - Email
  - Phone Number
  - Skills
  - Education Keywords
  - Experience

## AI Resume Matching
- Compares resumes against Job Descriptions
- Calculates:
  - Match Score
  - Matched Skills
  - Missing Skills
  - Hiring Recommendation

## Gemini AI Analysis
- AI-generated resume feedback
- Resume improvement suggestions
- Candidate summary
- Technical strengths analysis
- Hiring recommendations

## Analytics Dashboard
- Total Resumes
- Highest Match Score
- Average Match Score
- Strong Hire Count
- Moderate Hire Count
- Low Match Count

## Interactive Charts
- Hiring Recommendation Pie Chart
- Candidate Match Score Bar Graph

## PDF Report Generation
- Downloadable AI-generated PDF reports for each candidate

## Modern UI
- Responsive dashboard
- Drag & Drop Resume Upload
- Animated Cards
- Progress Bars
- Modern ATS-like Interface

---

# Tech Stack

## Backend
- FastAPI
- Python

## Frontend
- HTML
- CSS
- Jinja2 Templates
- Chart.js

## AI / NLP
- Gemini AI API
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity

## PDF Processing
- PyMuPDF (fitz)

## Report Generation
- ReportLab

---

# Project Architecture

```plaintext
ai-resume-screening-system/
│
├── app/
│   ├── main.py
│   ├── matcher.py
│   ├── resume_parser.py
│   ├── ai_feedback.py
│   └── report_generator.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── uploads/
├── reports/
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env

Installation
Clone Repository
git clone https://github.com/YOUR_USERNAME/ai-resume-screening-system.git
cd ai-resume-screening-system

Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Mac/Linux
python3 -m venv venv
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Configure Gemini API Key

Create a .env file in the root directory:

GEMINI_API_KEY=your_api_key_here

Get Gemini API Key from:
https://aistudio.google.com/app/apikey

Run the Application
uvicorn app.main:app --reload --port 8001

Open browser:

http://127.0.0.1:8001