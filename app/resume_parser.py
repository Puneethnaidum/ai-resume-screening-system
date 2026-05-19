import fitz
import re


def extract_text_from_pdf(pdf_file):

    text = ""

    pdf_document = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in pdf_document:
        text += page.get_text()

    return text


def extract_email(text):

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    emails = re.findall(
        email_pattern,
        text
    )

    return emails[0] if emails else "Not Found"


def extract_phone(text):

    phone_pattern = r"(\+?\d[\d\s\-]{8,}\d)"

    phones = re.findall(
        phone_pattern,
        text
    )

    return phones[0] if phones else "Not Found"


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:
            return line

    return "Not Found"


def extract_education(text):

    education_keywords = [
        "bachelor",
        "master",
        "university",
        "college",
        "b.tech",
        "m.tech",
        "computer science"
    ]

    found = []

    text_lower = text.lower()

    for keyword in education_keywords:

        if keyword in text_lower:
            found.append(keyword)

    return list(set(found))


def extract_experience(text):

    experience_pattern = r"(\d+)\+?\s+years"

    matches = re.findall(
        experience_pattern,
        text.lower()
    )

    return matches[0] + " Years" if matches else "Not Found"