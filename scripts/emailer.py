import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

def send_email(sender_email, app_password, recipient_email, subject, body, attachment_paths=None):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if attachment_paths:
        for path in attachment_paths:
            try:
                with open(path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
                msg.attach(part)
            except Exception as e:
                print(f"⚠️ Could not attach {path}: {e}")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("📬 Email with attachments sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
