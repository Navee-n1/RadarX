from sentence_transformers import SentenceTransformer, util
from utils.parser import extract_text
from utils.skill_extractor import extract_skills
from models import Resume, JD, MatchResult
from models import db

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity_score(jd_text, resume_text):
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    score = util.cos_sim(jd_emb, resume_emb).item()
    return score

def run_batch_match(jd_id):
    jd = JD.query.get(jd_id)
    jd_text = extract_text(jd.file_path)
    jd_skills = extract_skills(jd_text)

    top_matches = []
    resumes = Resume.query.all()

    for resume in resumes:
        resume_text = extract_text(resume.file_path)
        resume_skills = extract_skills(resume_text)

        skill_overlap = len(set(jd_skills) & set(resume_skills))
        if skill_overlap < 1:
            continue  # skip low-skill-match resumes

        score = compute_similarity_score(jd_text, resume_text)
        label = get_label(score)

        result = MatchResult(jd_id=jd.id, resume_id=resume.id, score=score, label=label)
        db.session.add(result)

        top_matches.append({
            "resume_id": resume.id,
            "file": resume.file_path,
            "score": round(score, 2),
            "label": label
        })

    db.session.commit()
    top_matches.sort(key=lambda x: x['score'], reverse=True)
    return top_matches[:3]

def run_one_to_one_match(jd_text, resume_text):
    return round(compute_similarity_score(jd_text, resume_text), 2)

def get_label(score):
    if score >= 0.85:
        return "✅ Highly Recommended"
    elif score >= 0.70:
        return "☑️ Recommended"
    elif score >= 0.50:
        return "🟡 Decent – Can Explore"
    else:
        return "🔴 Not Recommended"
