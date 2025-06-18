import os
from flask import Blueprint, request, jsonify
from models import db, JD, Resume, MatchResult
from utils.parser import extract_text
from utils.matcher import compute_similarity_score
from utils.explainer import generate_explanation
from utils.skill_extractor import extract_skills

match_bp = Blueprint('match_bp', __name__)

# ─────────────────────────────────────────────
# JD TO RESUMES (Bulk)
# ─────────────────────────────────────────────
@match_bp.route('/match/jd-to-resumes', methods=['POST'])
def match_jd_to_resumes():
    jd_id = request.json.get('jd_id')
    jd = JD.query.get(jd_id)
    if not jd:
        return jsonify({"error": "JD not found"}), 404

    jd_text = extract_text(jd.file_path)
    jd_skills = extract_skills(jd_text)
    jd_domain = detect_domain(jd_text)

    results = []
    resumes = Resume.query.all()

    for resume in resumes:
        res_text = extract_text(resume.file_path)
        res_skills = extract_skills(res_text)
        base_score = compute_similarity_score(jd_text, res_text)

        # domain bonus
        if jd_domain and jd_domain in res_text.lower():
            base_score += 0.05

        explanation = generate_explanation(jd_text, res_text)
        label = get_label(base_score)

        # Save match result to DB
        match = MatchResult(
            jd_id=jd.id,
            resume_id=resume.id,
            score=base_score,
            explanation=str(explanation)
        )
        db.session.add(match)
        db.session.commit()

        results.append({
            "resume_id": resume.id,
            "file": os.path.basename(resume.file_path),
            "file_path": resume.file_path,  # ✅ needed for email
            "score": round(base_score, 2),
            "label": label,
            "explanation": explanation
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({"top_matches": results[:3]})

# ─────────────────────────────────────────────
# RESUME TO JDs (Reverse Match)
# ─────────────────────────────────────────────
@match_bp.route('/match/resume-to-jds', methods=['POST'])
def match_resume_to_jds():
    resume_id = request.json.get('resume_id')
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    res_text = extract_text(resume.file_path)
    res_skills = extract_skills(res_text)

    results = []
    jds = JD.query.all()
    for jd in jds:
        jd_text = extract_text(jd.file_path)
        jd_skills = extract_skills(jd_text)
        base_score = compute_similarity_score(jd_text, res_text)
        label = get_label(base_score)
        explanation = generate_explanation(jd_text, res_text)

        results.append({
            "jd_id": jd.id,
            "jd_file": os.path.basename(jd.file_path),
            "score": round(base_score, 2),
            "label": label,
            "explanation": explanation
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({"top_matches": results[:3]})

# ─────────────────────────────────────────────
# ONE-TO-ONE MATCH
# ─────────────────────────────────────────────
@match_bp.route('/match/one-to-one', methods=['POST'])
def one_to_one_match():
    jd_id = request.json.get('jd_id')
    resume_id = request.json.get('resume_id')

    jd = JD.query.get(jd_id)
    resume = Resume.query.get(resume_id)
    if not jd or not resume:
        return jsonify({"error": "Invalid IDs"}), 404

    jd_text = extract_text(jd.file_path)
    res_text = extract_text(resume.file_path)

    score = compute_similarity_score(jd_text, res_text)
    explanation = generate_explanation(jd_text, res_text)
    label = get_label(score)

    return jsonify({
        "score": round(score, 2),
        "label": label,
        "explanation": explanation
    })

# ─────────────────────────────────────────────
# HEATMAP VISUALIZER
# ─────────────────────────────────────────────
@match_bp.route('/heatmap/<int:jd_id>/<int:resume_id>', methods=["GET"])
def get_heatmap_data(jd_id, resume_id):
    jd = JD.query.get(jd_id)
    resume = Resume.query.get(resume_id)

    if not jd or not resume:
        return jsonify({"error": "Invalid JD or Resume ID"}), 404

    jd_text = extract_text(jd.file_path)
    resume_text = extract_text(resume.file_path)

    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    heatmap_data = {
        "skills": list(set(jd_skills + resume_skills)),
        "resume_match": [1 if skill in resume_skills else 0 for skill in jd_skills]
    }

    return jsonify(heatmap_data)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_label(score):
    if score >= 0.85:
        return "✅ Highly Recommended"
    elif score >= 0.70:
        return "☑️ Recommended"
    elif score >= 0.50:
        return "🟡 Decent – Can Explore"
    else:
        return "🔴 Not Recommended"

def detect_domain(text):
    domains = ['banking', 'healthcare', 'ecommerce', 'automotive', 'insurance', 'retail']
    text = text.lower()
    for domain in domains:
        if domain in text:
            return domain
    return None
