from logging import Logger
from typing import Any, List

from celery import shared_task
from email_validator import EmailNotValidError, validate_email
from flask import Flask
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer

from app.DBHandler import DBHandler
from app.utils import get_date


class MailHandler:
    def __init__(self, flask_app: Flask, db_handler: DBHandler, logger: Logger) -> None:
        self.flask_app = flask_app
        self.flask_mail = Mail(flask_app)
        self.db_handler = db_handler
        self.logger = logger

    @shared_task()
    def _send_email(
        recipients: str | list[str],
        subject: str,
        message: str,
        extra_headers: dict[str, str] | None = None,
        verbose: bool = True,
    ):
        """Celery task to send emails.
        This method is a celery task. So: 1. cannot access class state,
        2. cannot get non-json-serializable arguments. Thus, we access
        app.app directly and instantiate a flask_mail.Mail instance.
        """

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
            from app import app, logger

            Mail(app).send(msg)
        except Exception as e:
            logger.debug(f"Failed to send email: '{subject}' with {e}")
            return False
        else:
            if verbose:
                logger.debug(f"Sent email to: {recipients}")
            return True

    def _send_confirmation_email(self, email_address: str) -> bool:

        signed_email_address = self._sign_email(
            email_address,
            salt="confirmation",
        )

        subject = "Confirm your text(o)s subscription!"
        message = f"""<p>Dear reader,<p>

        <p>You have requested to be part of the text(o)s newsletter. In order to confirm this subscription
            <a href="http://{self.flask_app.config["DOMAIN_NAME"]}/newsletter-confirmation/{signed_email_address}">click here </a>
        </p>

        <p>If you did not request access to the text(o)s newsletter, ignore this email. You will not be subscribed. </p>

        <a href="__unsubscribe_url__"></a>
        """

        sent_status = self._send_email(email_address, subject, message)

        return sent_status

    def _validate_email_format(
        self, email_address: str, return_normalized=False
    ) -> str | None:

        try:
            email_info = validate_email(email_address)
            email_address = email_info.normalized.lower()

        except EmailNotValidError:
            return None
        else:
            if return_normalized:
                return email_address

    def _check_email_exists(self, email_address: str) -> bool:

        n_rows_with_email = len(
            self.db_handler.execute_read(
                "select id from email where email_address=?;", (email_address,)
            )
        )
        if n_rows_with_email > 0:
            return True

        return False

    def _get_confirmed_emails(self) -> List:
        confirmed_emails = self.db_handler.execute_read(
            "SELECT email_address FROM email WHERE confirmed=1;"
        )

        # get first element per singleton
        confirmed_emails = [row[0] for row in confirmed_emails]
        return confirmed_emails

    def _sign_email(self, data: Any, salt: str) -> str:
        s = URLSafeSerializer(self.flask_app.config["ADMIN_KEY_HASH"], salt)
        signed_data = s.dumps(data)
        return signed_data

    def _load_signed_email(self, signed_data: str | bytes, salt: str) -> str:
        s = URLSafeSerializer(self.flask_app.config["ADMIN_KEY_HASH"], salt)
        data = s.loads(signed_data)
        return data

    def send_newsletter(self, post_id: int, post_title: str, post_preview: str) -> None:

        email_addresses = self._get_confirmed_emails()
        n_email_addresses = len(email_addresses)

        if n_email_addresses == 0:
            self.logger.debug("Newsletter not sent due to 0 subscribers")
            return

        self.logger.debug(f"Sending newsletter to {n_email_addresses} subscribers")
        unsubscribe_links = [
            self._sign_email(email_address, salt="unsubscribe")
            for email_address in email_addresses
        ]

        inline_post_preview = post_preview.replace("<p>", "").replace("</p>", "")
        subject = "New post!"

        for i in range(n_email_addresses):
            message = f"""
                <p>Dear reader,</p>
                <p>We just wrote something called <a href="http://{self.flask_app.config["DOMAIN_NAME"]}/post/{post_id}"><b>{post_title}</b></a>
                It is described to be about: {inline_post_preview}. Hope you enjoy it! </p>

                <p style="margin-top:25px">No longer interested? You can 
                <a href="http://{self.flask_app.config["DOMAIN_NAME"]}/newsletter-unsubscribe/{unsubscribe_links[i]}">
                unsubscribe</a> from the newsletter</p>

                """

            self._send_email.delay(email_addresses[i], subject, message, verbose=False)

    def add_email(self, email_address: str) -> str:

        normalized_email_address = self._validate_email_format(email_address, return_normalized=True)
        if normalized_email_address == None:
            return "validation_error"

        if self._check_email_exists(normalized_email_address):
            return "not_new_error"

        sent_status = self._send_confirmation_email(normalized_email_address)
        if not sent_status:
            return "sending_error"

        # else:
        confirmed = False
        self.db_handler.execute_write(
            "INSERT INTO email(date, email_address, confirmed) VALUES (?,?,?)",
            (get_date(), normalized_email_address, confirmed),
        )
        self.logger.debug(f"{normalized_email_address} suscribed [not confirmed]")
        return "no_error"

    def confirm_email(self, signed_email_address: str) -> bool:

        try:
            email_address = self._load_signed_email(
                signed_email_address,
                salt="confirmation",
            )
            self.db_handler.execute_write(
                "UPDATE email SET (confirmed) = (?) where email_address = ?",
                (True, email_address),
            )
        except Exception as e:
            self.logger.error(f"Email confirmation failed with exception: {e}")
            return False
        else:
            self.logger.debug(f"{email_address} suscribed [confirmed]")
            return True

    def delete_email(self, signed_email_address: str) -> bool:

        try:
            email_address = self._load_signed_email(
                signed_email_address,
                salt="unsubscribe",
            )
            self.db_handler.execute_write(
                "DELETE FROM email WHERE email_address=?;", (email_address,)
            )
        except Exception as e:
            self.logger.error(f"Failed unsubscribing email, whith exception: {e}")
            return False
        else:
            self.logger.debug(f"{email_address} unsubscribed")
            return True
