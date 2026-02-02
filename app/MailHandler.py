from logging import Logger
from typing import Any, Tuple

from email_validator import EmailNotValidError, validate_email
from flask import Flask
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer
from app.utils import get_date

from app.DBHandler import DBHandler


class MailHandler:
    def __init__(self, flask_app: Flask, db_handler: DBHandler, logger: Logger) -> None:
        self.flask_app = flask_app
        self.flask_mail = Mail(flask_app)
        self.db_handler = db_handler
        self.logger = logger

    def _send_email(
        self,
        recipients: str | list[str],
        subject: str,
        message: str,
        extra_headers: dict[str, str] | None = None,
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
            self.flask_mail.send(msg)
        except Exception as e:
            self.logger.info(f"Failed to send email: '{subject}' with {e}")
            return False
        else:
            return True

    def _send_confirmation_email(self, email_address: str) -> bool:

        signed_email_address = self._sign_data(
            email_address,
            secret_key=self.flask_app.config["ADMIN_KEY_HASH"],
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

    def _validate_email_format(self, email_address: str) -> str | None:

        try:
            email_info = validate_email(email_address)
            email_address = email_info.normalized
        except EmailNotValidError:
            return None
        else:
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

    def _sign_data(self, data: Any, secret_key: str, salt: str) -> str:
        s = URLSafeSerializer(secret_key, salt)
        signed_data = s.dumps(data)
        return signed_data

    def _load_signed_data(
        self, signed_data: str | bytes, secret_key: str | bytes, salt: str
    ) -> str:
        s = URLSafeSerializer(secret_key, salt)
        data = s.loads(signed_data)
        return data

    def send_newsletter(self) -> None:
        pass

    def add_email(self, email_address: str) -> str:

        normalized_email_address = self._validate_email_format(email_address)
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
        return "no_error"

    def confirm_email(self) -> None:
        pass

    def delete_email(self) -> None:
        pass
