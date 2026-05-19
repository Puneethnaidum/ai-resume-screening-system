from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import re


SKILLS = [
    "python", "java", "sql", "aws", "docker", "kubernetes",
    "react", "fastapi", "machine learning", "tensorflow",
    "pandas", "numpy", "power bi", "snowflake", "ci/cd",
    "git", "jenkins", "azure", "tableau", "api",
    "rest api", "mongodb", "postgresql"
]


INTERVIEW_QUESTIONS = {
    "python": [
        "Explain Python decorators.",
        "Explain generators in Python.",
        "Difference between list and tuple?"
    ],
    "sql": [
        "Difference between INNER JOIN and LEFT JOIN?",
        "Explain normalization.",
        "What are indexes in SQL?"
    ],
    "aws": [
        "What is AWS Lambda?",
        "Difference between EC2 and S3?",
        "Explain AWS IAM."
    ],
    "docker": [
        "What is Docker?",
        "Difference between Docker and virtual machine?"
    ],
    "kubernetes": [
        "Explain Kubernetes pods.",
        "Difference between pod and deployment?"
    ],
    "machine learning": [
        "Difference between supervised and unsupervised learning?",
        "Explain overfitting and underfitting."
    ]
}


STOPWORDS = [
    "the", "is", "and", "to", "in", "for", "of",
    "with", "a", "an", "on", "at", "by", "from"
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


def extract_skills(text):
    text = clean_text(text)
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))


def calculate_match_score(job_description, resume_text):
    documents = [job_description, resume_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity_score * 100, 2)


def extract_top_keywords(text, top_n=10):
    text = clean_text(text)
    words = text.split()

    filtered_words = [
        word for word in words
        if word not in STOPWORDS and len(word) > 2
    ]

    word_counts = Counter(filtered_words)

    return [
        word[0]
        for word in word_counts.most_common(top_n)
    ]


def generate_interview_questions(skills):
    questions = []

    for skill in skills:
        if skill in INTERVIEW_QUESTIONS:
            questions.extend(INTERVIEW_QUESTIONS[skill])

    return questions[:5]


def generate_resume_feedback(matched_skills, missing_skills, match_score):
    feedback = []

    if match_score >= 70:
        feedback.append("Strong overall match for the job role.")
    elif match_score >= 50:
        feedback.append("Moderate match. Resume can be improved further.")
    else:
        feedback.append("Low match score. Resume needs optimization.")

    if matched_skills:
        feedback.append(
            f"Strong skills detected: {', '.join(matched_skills)}."
        )

    if missing_skills:
        feedback.append(
            f"Consider adding skills like: {', '.join(missing_skills)}."
        )

    return feedback


def generate_improvement_suggestions(missing_skills, match_score):
    suggestions = []

    if match_score < 50:
        suggestions.append(
            "Add more job-specific keywords from the job description."
        )
        suggestions.append(
            "Include measurable achievements with numbers and business impact."
        )

    if missing_skills:
        for skill in missing_skills:
            suggestions.append(
                f"Add relevant experience or project details related to {skill}."
            )

    suggestions.append(
        "Use clear project bullet points with tools, action, and result."
    )

    suggestions.append(
        "Mention real-world impact such as time saved, accuracy improved, or cost reduced."
    )

    return suggestions[:6]


def get_hiring_recommendation(match_score):
    if match_score >= 80:
        return "Strong Hire"
    elif match_score >= 50:
        return "Moderate Hire"
    else:
        return "Low Match"


def get_skill_analysis(job_description, resume_text):
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    matched_skills = list(set(jd_skills) & set(resume_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    match_score = calculate_match_score(job_description, resume_text)

    interview_questions = generate_interview_questions(matched_skills)
    top_keywords = extract_top_keywords(resume_text)

    feedback = generate_resume_feedback(
        matched_skills,
        missing_skills,
        match_score
    )

    improvement_suggestions = generate_improvement_suggestions(
        missing_skills,
        match_score
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "interview_questions": interview_questions,
        "top_keywords": top_keywords,
        "feedback": feedback,
        "improvement_suggestions": improvement_suggestions
    }