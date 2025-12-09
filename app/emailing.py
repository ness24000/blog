from logging import Logger

from celery import shared_task
from flask_mail import Message

from app import app, mail
from app.db_interface import get_confirmed_emails_in_db
from app.utils import sign_data


def send_email(
    recipients: str | list[str],
    subject: str,
    message: str,
    logger: Logger = None,
    extra_headers: dict[str, str] = None,
):

    if isinstance(recipients, str):
        recipients = [recipients]

    msg = Message(
        subject=subject,
        sender=("textos", "newsletter@txtos.eu"),
        recipients=recipients,
        html=message,
        extra_headers=extra_headers,
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        if logger != None: 
            logger.info(f"Failed to send email: '{subject}' with {e}")
        return False


def send_confirmation_email(email_address: str, logger: Logger):

    signed_email_address = sign_data(
        email_address, secret_key=app.config["ADMIN_KEY_HASH"], salt="confirmation"
    )

    subject = "Confirm your text(o)s subscription!"
    message = f"""<p>Dear reader,<p>

    <p>You have requested to be part of the text(o)s newsletter. In order to confirm this subscription
        <a href="http://{app.config["DOMAIN_NAME"]}/newsletter-confirmation/{signed_email_address}">click here </a>
    </p>

    <p>If you did not request access to the text(o)s newsletter, ignore this email. You will not be subscribed. </p>

    <a href="__unsubscribe_url__"></a>
    """

    sent_status = send_email(email_address, subject, message, logger)

    return sent_status


@shared_task(ignore_result=False)
def send_newsletter(post_title: str, post_preview: str, secret_key):

    email_addresses = get_confirmed_emails_in_db(app.config["PATH_TO_DB"])

    if len(email_addresses) == 0:
        return "Newsletter not sent due to 0 subscribers"

    email_addresses_and_links = {
        email_address: sign_data(
                email_address,
                secret_key=secret_key,
                salt="unsubscribe"
            )
        
        for email_address in email_addresses
    }

    inline_post_preview = post_preview.replace("<p>", "").replace("</p>", "")
    subject = "New post!"
    
    for email, unsubscribe_link in email_addresses_and_links.items():
        message = f"""
            <p>Dear reader,</p>
            <p>We just wrote something called <b>{post_title}</b>. It is described to be
            about: {inline_post_preview}. Hope you enjoy it! </p>
            
            <p style="margin-top:25px">No longer interested? You can 
            <a href="http://{app.config["DOMAIN_NAME"]}/newsletter-unsubscribe/{unsubscribe_link}">
            unsubscribe</a> from the newsletter</p>

            """

        send_email(email, subject, message)

    return f"Sent newsletter to {len(email_addresses)} people"