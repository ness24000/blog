from flask_mail import Message
from app import mail
from logging import Logger

def send_confirmation_email(email_address:str, logger: Logger):
    msg = Message(
        subject="Confirm your text(o)s subscription!",
        sender=("textos", "newsletter@txtos.eu"),
        recipients=[email_address],
        html=f"""
<p>Dear reader,<p>

<p>You have requested to be part of the text(o)s newsletter. In order to confirm this subscription
    <a href="http://txtos.eu/newsletter-confirmation/{email_address}">click here </a>
</p>

<p>If you did not request access to the text(o)s newsletter, ignore this email. You will not be subscribed. </p>
""",
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        logger.info(f"Failed to send to {recipients} with {e}")
        return False
