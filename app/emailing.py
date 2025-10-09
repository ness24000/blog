from logging import Logger

from flask_mail import Message

from app import app, mail
from app.utils import sign_data


def send_confirmation_email(email_address: str, logger: Logger):

    signed_email_address = sign_data(
        email_address, secret_key=app.config["ADMIN_KEY_HASH"], salt="confirmation"
    )    
    msg = Message(
        subject="Confirm your text(o)s subscription!",
        sender=("textos", "newsletter@txtos.eu"),
        recipients=[email_address],
        html=f"""
<p>Dear reader,<p>

<p>You have requested to be part of the text(o)s newsletter. In order to confirm this subscription
    <a href="http://{app.config["DOMAIN_NAME"]}/newsletter-confirmation/{signed_email_address}">click here </a>
</p>

<p>If you did not request access to the text(o)s newsletter, ignore this email. You will not be subscribed. </p>
""",
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        logger.info(f"Failed to send to {email_address} with {e}")
        return False
