import smtplib
import os
import socket
import mimetypes
from email.message import EmailMessage

# prevent long blocking
socket.setdefaulttimeout(15)

SENDER_MAIL = os.environ.get("SENDER_MAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

def send_email(to_email, username, age, result, image_path, phone_number):
    # -------- BASIC CHECKS --------
    if not to_email or to_email.strip() == "":
        print("No recipient email provided")
        return

    if not SENDER_MAIL or not SENDER_PASSWORD:
        print("Missing EMAIL ENV VARIABLES")
        return

    msg = EmailMessage()
    msg["Subject"] = "Bone Fracture Classification Report"
    msg["From"] = SENDER_MAIL
    msg["To"] = to_email

    msg.set_content(f"""
Hello {username},

Bone Fracture Analysis Report

Name: {username}
Age: {age}
Phone: {phone_number}

Prediction: {result}

If NORMAL → take care.
If FRACTURED → consult a doctor.

Regards,
Bone Fracture AI System
""")

    # -------- ATTACH IMAGE (AUTO TYPE) --------
    try:
        if os.path.exists(image_path):
            mime_type, _ = mimetypes.guess_type(image_path)
            if mime_type:
                maintype, subtype = mime_type.split("/")
            else:
                maintype, subtype = "application", "octet-stream"

            with open(image_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=os.path.basename(image_path)
                )
    except Exception as e:
        print("Attachment failed:", e)

    # -------- SEND EMAIL --------
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.starttls()
            server.login(SENDER_MAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print("EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("EMAIL ERROR:", e)
