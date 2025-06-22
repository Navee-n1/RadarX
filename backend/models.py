from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)  # 'recruiter' or 'ar'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password=db.Column(db.String,nullable=False)

class JD(db.Model):
    __tablename__ = 'jd'
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String, nullable=False)
    uploaded_by = db.Column(db.String)
    project_code = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Resume(db.Model):
    __tablename__ = 'resume'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    file_path = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class MatchResult(db.Model):
    __tablename__ = 'match_result'
    id = db.Column(db.Integer, primary_key=True)
    jd_id = db.Column(db.Integer, db.ForeignKey('jd.id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    score = db.Column(db.Float)
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmailLog(db.Model):
    __tablename__ = 'email_log'
    id = db.Column(db.Integer, primary_key=True)
    jd_id = db.Column(db.Integer)
    sent_to = db.Column(db.String)
    cc = db.Column(db.String)
    status = db.Column(db.String)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    pdf_path = db.Column(db.String)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer)
    jd_id = db.Column(db.Integer)
    given_by = db.Column(db.String)
    vote = db.Column(db.String)  # 'up' or 'down'
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class BulkUploadMeta(db.Model):
    __tablename__ = 'bulk_upload_meta'
    id = db.Column(db.Integer, primary_key=True)
    jd_id = db.Column(db.Integer)
    recruiter_email = db.Column(db.String)
    manager_email = db.Column(db.String)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
