from logging import Logger

from flask_mail import Message

from app import app, mail
from app.utils import sign_data
from app.db_interface import get_confirmed_emails_in_db


def send_email(
    recipients: str | list[str],
    subject: str,
    message: str,
    logger: Logger,
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


def send_newsletter(post_title: str, post_preview: str, logger: Logger):

    list_email_addresses = get_confirmed_emails_in_db(app.config["PATH_TO_DB"])

    if len(list_email_addresses == 0):
        logger.debug("Newsletter not sent due to 0 suscribers")
        return False

    unsuscribe_links = {
        email_address: {
            "unsuscribe_link": sign_data(
                email_address,
                secret_key=app.config["ADMIN_KEY_HASH"],
                salt="unsubscribe",
            )
        }
        for email_address in list_email_addresses
    }

    extra_headers = {"X-Mailgun-Recipient-Variables": str(unsuscribe_links)}

    inline_post_preview = post_preview.replace("<p>", "").replace("</p>", "")
    subject = "New post!"
    message = f"""
        <p>Dear reader,</p>
        <p>We just wrote something called <b>{post_title}</b>. It is described to be
          about: {inline_post_preview}. Hope you enjoy it! </p>
        
        <p style="margin-top:25px">No longer interested? You can 
        <a href="txtos.eu/unsuscribe/%recipient.unsuscribe_link%">unsubscribe</a> 
        from the newsletter</p>

        """

    send_email(r"%recipient%", subject, message, logger, extra_headers)
