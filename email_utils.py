import smtplib
import os
from email.message import EmailMessage

my_mail = os.environ.get("SENDER_MAIL")
password = os.environ.get("SENDER_PASSWORD") 

def send_email(to_email, username, age, result, image_path, phone_number):
    msg = EmailMessage()
    msg['Subject'] = 'Bone Fracture Classification report'
    msg['From'] = my_mail
    msg['To'] = to_email
    
    msg.set_content(f"""
    Hello, {username}, Greetings!
    Your Bone Fracture Analysis Report
    Name: {username}
    Age: {age}
    Email: {to_email}
    Phone number: {phone_number}
    Prediction: {result}
    
    If your prediction is Normal then no need to worry take extra care, and if your prediction is Fractured then Consult a medical professional.

    Regards,
    Bone Fracture AI System.
                    """)
    
    with open(image_path, 'rb') as img:
        msg.add_attachment(
            img.read(),
            subtype = 'png',
            filename = 'image.png',
            maintype = 'image'
        )
    
    

    with smtplib.SMTP("smtp.gmail.com",port=587, timeout=15) as connection:
        connection.starttls()
        connection.login(user=my_mail, password=password)
        connection.send_message(msg)
