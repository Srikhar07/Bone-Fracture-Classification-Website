import smtplib
import os
import socket
from email.message import EmailMessage

# prevent long blocking
socket.setdefaulttimeout(25)

my_mail = os.environ.get("SENDER_MAIL")
password = os.environ.get("SENDER_PASSWORD")

def send_email(to_email, username, age, result, image_path, phone_number):
    if not my_mail or not password:
        print("Email credentials missing")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Bone Fracture Classification Report'
    msg['From'] = my_mail
    msg['To'] = to_email

    msg.set_content(f"""
Hello {username},

Bone Fracture Analysis Report

Name: {username}
Age: {age}
Email: {to_email}
Phone: {phone_number}

Prediction: {result}

If result is NORMAL → take care.
If FRACTURED → consult a doctor.

Regards,
Bone Fracture AI System
""")

    # attach image safely
    try:
        with open(image_path, 'rb') as img:
            msg.add_attachment(
                img.read(),
                maintype='image',
                subtype='png',
                filename='bone.png'
            )
    except:
        print("Image attach failed")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=25)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(my_mail, password)
        server.send_message(msg)
        server.quit()
        print("Mail sent")
    except Exception as e:
        print("EMAIL ERROR:", e)
