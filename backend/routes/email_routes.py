from flask import Blueprint, request, jsonify
from utils.emailer import send_email_with_attachments

email_bp = Blueprint('email_bp', __name__)

@email_bp.route('/send-email/manual', methods=['POST'])
def send_manual_email():
    data = request.json
    jd_id = data.get('jd_id')
    to_email = data.get('to_email')
    cc_list = data.get('cc_list', [])
    attachments = data.get('attachments', [])
    subject = data.get('subject', 'Top Matches')
    body = data.get('body', '')

    if not jd_id or not to_email or not attachments:
        return jsonify({"error": "Missing required fields"}), 400

    status = send_email_with_attachments(
        subject, body, to_email, cc_list, attachments, jd_id
    )
    return jsonify({"message": status})
