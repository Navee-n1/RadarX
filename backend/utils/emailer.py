import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from models import EmailLog, db
from datetime import datetime

load_dotenv()
EMAIL_ID = os.getenv("EMAIL_ID")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email_with_attachments(subject, body, to_email, cc_list, attachment_paths, jd_id, explanation=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ID
        msg["To"] = to_email
        msg["Cc"] = ', '.join(cc_list)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        for path in attachment_paths:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
                    msg.attach(part)
            else:
                print(f"❌ Attachment not found: {path}")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ID, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ID, [to_email] + cc_list, msg.as_string())
        server.quit()

        db.session.add(EmailLog(
            jd_id=jd_id,
            sent_to=to_email,
            cc=', '.join(cc_list),
            status='Sent',
            sent_at=datetime.utcnow(),
            pdf_path=''  # update if needed
        ))
        db.session.commit()

        return "✅ Email Sent"

    except Exception as e:
        print("❌ Email Error:", e)
        return f"❌ Failed: {str(e)}"

# def generate_pdf_report(jd_id, explanation):
#     filename = f"jd_{jd_id}_match_report.pdf"
#     filepath = os.path.join("static", "reports", filename)

#     c = canvas.Canvas(filepath, pagesize=letter)
#     width, height = letter
#     y = height - 50

#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(50, y, f"Match Explanation Report - JD ID: {jd_id}")
#     y -= 30

#     c.setFont("Helvetica", 12)
#     def write_line(label, value):
#         nonlocal y
#         c.drawString(50, y, f"{label}: {value}")
#         y -= 20

#     write_line("Matched Skills", ", ".join(explanation.get("skills_matched", [])))
#     write_line("Missing Skills", ", ".join(explanation.get("skills_missing", [])))
#     write_line("Required Experience", explanation.get("jd_experience_required"))
#     write_line("Resume Experience", explanation.get("resume_experience_found"))
#     write_line("JD Role", explanation.get("jd_role"))
#     write_line("Resume Role", explanation.get("resume_role"))
#     y -= 10

#     highlights = explanation.get("highlights_found", [])
#     if highlights:
#         c.setFont("Helvetica-Bold", 13)
#         c.drawString(50, y, "Candidate Highlights:")
#         y -= 20
#         c.setFont("Helvetica", 11)
#         for h in highlights:
#             c.drawString(60, y, f"- {h}")
#             y -= 15

#     c.save()
#     return filepath
