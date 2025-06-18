import os
import pandas as pd
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from models import db, JD, Resume

upload_bp = Blueprint('upload_bp', __name__)

# Get absolute paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER_JD = os.path.join(BASE_DIR, '..', 'uploads', 'jds')
UPLOAD_FOLDER_RESUME = os.path.join(BASE_DIR, '..', 'uploads', 'resumes')
UPLOAD_FOLDER_EXCEL = os.path.join(BASE_DIR, '..', 'uploads', 'excel')

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER_JD, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_RESUME, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_EXCEL, exist_ok=True)

# ─────────────────────────────────────────────
# UPLOAD JD FILE (Single Upload)
# ─────────────────────────────────────────────
@upload_bp.route('/upload-jd', methods=['POST'])
def upload_jd():
    file = request.files.get('file')
    uploaded_by = request.form.get('uploaded_by', 'anonymous')
    project_code = request.form.get('project_code', 'GENERIC')

    if not file:
        return jsonify({"error": "No file provided"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER_JD, filename)
    file.save(save_path)

    jd = JD(
        file_path=save_path,
        uploaded_by=uploaded_by,
        project_code=project_code
    )
    db.session.add(jd)
    db.session.commit()

    return jsonify({"message": "JD uploaded", "jd_id": jd.id})

# ─────────────────────────────────────────────
# UPLOAD RESUME FILE (Single Upload)
# ─────────────────────────────────────────────
@upload_bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    file = request.files.get('file')
    name = request.form.get('name', file.filename)

    if not file:
        return jsonify({"error": "No file provided"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER_RESUME, filename)
    file.save(save_path)

    resume = Resume(name=name, file_path=save_path)
    db.session.add(resume)
    db.session.commit()

    return jsonify({"message": "Resume uploaded", "resume_id": resume.id})

# ─────────────────────────────────────────────
# UPLOAD BULK EXCEL (Multi JD Upload + Routing Info)
# ─────────────────────────────────────────────
@upload_bp.route('/upload-excel', methods=['POST'])
def upload_excel():
    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file provided"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER_EXCEL, filename)
    file.save(save_path)

    # Read Excel for multiple JDs with routing info
    df = pd.read_excel(save_path)
    required_columns = {'JD Title', 'JD Text', 'Recruiter Email', 'Hiring Manager Email'}

    if not required_columns.issubset(df.columns):
        return jsonify({"error": f"Missing required columns: {required_columns}"}), 400

    jd_ids = []
    for _, row in df.iterrows():
        jd_text = row['JD Text']
        jd_title = row['JD Title']
        recruiter_email = row['Recruiter Email']
        hiring_manager = row['Hiring Manager Email']

        # Save text file with JD title (for demo purposes)
        jd_filename = secure_filename(jd_title.replace(" ", "_") + ".txt")
        jd_file_path = os.path.join(UPLOAD_FOLDER_JD, jd_filename)
        with open(jd_file_path, "w", encoding="utf-8") as f:
            f.write(jd_text)

        jd = JD(
            file_path=jd_file_path,
            uploaded_by=recruiter_email,
            project_code="EXCEL-BULK"
        )
        db.session.add(jd)
        db.session.flush()  # get jd.id before commit
        jd_ids.append({
            "jd_id": jd.id,
            "recruiter": recruiter_email,
            "manager": hiring_manager
        })

    db.session.commit()
    return jsonify({"message": "Excel processed", "jds": jd_ids})
