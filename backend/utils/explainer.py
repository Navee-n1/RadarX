import re
from collections import Counter
from utils.skill_extractor import extract_skills
import spacy
from models import db
nlp = spacy.load("en_core_web_sm")

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s+(years|yrs)', text.lower())
    return int(matches[0][0]) if matches else None

def extract_role(text):
    doc = nlp(text.lower())
    roles = ["data scientist", "backend developer", "frontend engineer", "full stack developer", "ml engineer", "sde", "software developer"]
    for role in roles:
        if role in text.lower():
            return role
    return "unspecified"

def generate_explanation(jd_text, resume_text):
    jd_skills = extract_skills(jd_text, top_n=20)
    resume_skills = extract_skills(resume_text, top_n=20)

    resume_word_count = Counter(resume_text.lower().split())
    skill_freq = {skill: resume_word_count.get(skill.lower(), 0) for skill in jd_skills}

    matched = [skill for skill in jd_skills if skill in resume_skills]
    missing = [skill for skill in jd_skills if skill not in resume_skills]

    explanation = {
        "skills_matched": matched,
        "skills_missing": missing,
        "skills_frequency": skill_freq,
        "jd_experience_required": extract_experience(jd_text),
        "resume_experience_found": extract_experience(resume_text),
        "jd_role": extract_role(jd_text),
        "resume_role": extract_role(resume_text),
        "highlights_found": extract_highlights(resume_text)
    }

    return explanation

def extract_highlights(resume_text):
    lines = resume_text.splitlines()
    highlights = []

    for line in lines:
        l = line.lower()
        if any(keyword in l for keyword in ["certified", "certification", "completed", "credential"]):
            highlights.append(f"🎓 {line.strip()}")
        elif any(keyword in l for keyword in ["worked on", "implemented", "built", "created", "led"]):
            highlights.append(f"🛠️ {line.strip()}")
        elif any(keyword in l for keyword in ["trained", "attended", "mentored", "contributed"]):
            highlights.append(f"📌 {line.strip()}")

    return highlights[:5]  # Limit to top 5 highlights for clarity
