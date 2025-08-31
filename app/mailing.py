from flask_mail import Message
from app import app, mail

def sending_test_email():
    msg = Message(
        subject = "Test email",
        sender = ("text(o)s' newsletter", "info@txtos.eu"),
        recipients=["nestor.chulvi@gmail.com"],
        body="Just a test."
    )
    try:
        mail.send(msg)
        return "Success"
    except Exception as e:
        return f"Failed with {e}"
        
    