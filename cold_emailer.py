import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Get the details
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")

# Reading the list of emails to cold email. 
with open("email_list.txt") as email_list:
    for receiver_email in email_list:
        msg = EmailMessage()
        msg["Subject"] = "Test Email from Python"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        # Message Content
        email_content = open("email_template.html","r", encoding="utf-8").read()
        msg.set_content("This email requires an HTML-supported client.")
        msg.add_alternative(email_content, subtype="html")

        # Adding the resume
        with open("resume.pdf", "rb") as resume:
            msg.add_attachment(
                resume.read(),
                maintype="application",
                subtype="pdf",
                filename="resume.pdf"
            )

        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)

        print(f"Email sent to: {receiver_email}")