import os
from parser import extract_text
from matcher import compute_similarity
from emailer import send_email

# -------------------- SETUP --------------------
DATA_FOLDER = os.path.join("..", "data")

# Locate JD file
jd_file = None
for file in os.listdir(DATA_FOLDER):
    if file.lower().startswith("jd") and file.lower().endswith((".docx", ".pdf")):
        jd_file = os.path.join(DATA_FOLDER, file)
        break

if not jd_file:
    raise FileNotFoundError("❌ JD file not found. Please name it like 'jd.docx' or 'jd.pdf'")

# Load resume files (excluding JD)
resume_files = [
    os.path.join(DATA_FOLDER, file)
    for file in os.listdir(DATA_FOLDER)
    if file != os.path.basename(jd_file) and file.lower().endswith((".docx", ".pdf"))
]

if not resume_files:
    raise FileNotFoundError("❌ No resume files found in the data folder.")

# -------------------- TEXT EXTRACTION --------------------
jd_text = extract_text(jd_file)
resumes = {os.path.basename(path): extract_text(path) for path in resume_files}

# -------------------- SIMILARITY SCORING --------------------
top_matches = compute_similarity(jd_text, resumes)

# -------------------- EMAIL CONTENT BUILDING --------------------
print(f"\n📄 JD: {os.path.basename(jd_file)}")
print("\n🧑‍💼 Top Consultant Matches:")

# Default email body
if not top_matches:
    email_body = (
        "Dear Recruiter,\n\n"
        "Unfortunately, no strong consultant matches were found for the provided job description.\n\n"
        "Thank you,\n"
        "Hexaware Recruitment Team"
    )
    subject = "No Suitable Matches Found"
    attachment_paths = []
else:
    email_body = (
        "Dear Recruiter,\n\n"
        "Based on the job description provided, we have identified the top consultant profiles that match your requirements.\n\n"
        f"📄 Job Description: {os.path.basename(jd_file)}\n\n"
        "🧑‍💼 Top 3 Matching Profiles:\n"
    )

    attachment_paths = []

    def get_label(score):
        if score >= 0.85:
            return "✅ Highly Recommended"
        elif score >= 0.70:
            return "☑️ Recommended"
        elif score >= 0.50:
            return "🟡 Decent – Can Explore"
        else:
            return "🔴 Not Recommended"

    for i, (name, score) in enumerate(top_matches, start=1):
        label = get_label(score)
        match_line = f"{i}. {name} - Match Score: {score:.2f} – {label}"
        print(match_line)
        email_body += match_line + "\n"

        resume_path = os.path.join(DATA_FOLDER, name)
        if os.path.exists(resume_path):
            attachment_paths.append(resume_path)

    email_body += "\nThank you,\nHexaware Recruitment Team"
    subject = "Top 3 Consultant Matches for JD"

# -------------------- EMAIL SENDING --------------------

recipient = input("\n📧 Enter the recruiter's email address: ").strip()
sender = input("📤 Enter your Gmail address to send from: ").strip()
password = input("🔑 Enter your app password (not Gmail login password): ").strip()

send_email(sender, password, recipient, subject, email_body, attachment_paths)
