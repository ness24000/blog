from flask_mail import Message
from app import mail
from logging import Logger

def send_confirmation_email(recipients:str, logger: Logger):
    msg = Message(
        subject="Confirm your text(o)s subscription!",
        sender=("textos", "newsletter@txtos.eu"),
        recipients=[recipients],
        body="""
Dear reader, 

You have requested to be part of the text(o)s newsletter. 
In order to confirm this subscription click here. 

If you did not request access to the text(o)s newsletter, ignore this email. 
You will not be subscribed. 
""",
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        logger.info(f"Failed to send to {recipients} with {e}")
        return False
