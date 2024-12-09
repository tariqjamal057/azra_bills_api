"""Module for sending emails using SMTP.

This module provides a class SMTPMail for sending emails using SMTP.
It utilizes the smtplib library for SMTP operations.

Classes:
    SMTPMail: A class for sending emails using SMTP.

Dependencies:
    - smtplib: For SMTP operations.
    - email.mime.multipart: For creating multipart email messages.
    - typing: For type hinting.
    - azra_store_lmi_api.config.logger.app: For logging.
    - azra_store_lmi_api.config.mailer.base: For the base mail class.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from typing import Optional

from azra_store_lmi_api.config.logger.app import logger
from azra_store_lmi_api.config.mailer.base import BaseMail


class SMTPMail(BaseMail):
    """Class for sending emails using SMTP.

    This class provides methods to initialize SMTP credentials and send email messages
    using the SMTP protocol.

    Attributes:
        hostname (Optional[str]): The SMTP hostname.
        port (Optional[int]): The SMTP port.
        username (Optional[str]): The SMTP username.
        password (Optional[str]): The SMTP password.
        use_ssl (Optional[bool]): Whether to use SSL for the SMTP connection.
    """

    def __init__(
        self,
        hostname: Optional[str] = None,
        port: Optional[int] = 25,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ssl: Optional[bool] = True,
    ):
        """Initialize the SMTP credentials with the provided parameters.

        Args:
            hostname (Optional[str]): The SMTP hostname.
            port (Optional[int]): The SMTP port. Defaults to 25.
            username (Optional[str]): The SMTP username.
            password (Optional[str]): The SMTP password.
            use_ssl (Optional[bool]): Whether to use SSL. Defaults to True.
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl

    async def send(self, message: dict) -> None:
        """Send an email message using the SMTP protocol.

        Args:
            message (dict): A dictionary containing the email message details.

        Raises:
            Exception: If the hostname is not set or if there's an SMTP error.

        Returns:
            None
        """
        if self.hostname is None:
            raise Exception("Hostname is not set")

        email = MIMEMultipart("alternative")
        email["From"] = self._format_emails_address(message["from_"])
        email["To"] = ",".join(message["to"])
        email["Subject"] = message["subject"]

        self._compose_extra_emails(message, email)

        for type_, content in message["content"].items():
            await self.build_multipart_content(email, type_, content)

        for filename, file in message["attachments"].items():
            await self._add_attachment(file, filename, email)

        with smtplib.SMTP(self.hostname, self.port) as server:
            if self.username is not None:
                server.user = self.username
                server.password = self.password
            try:
                server.ehlo()
                if self.use_ssl:
                    try:
                        server.starttls()
                    except smtplib.SMTPNotSupportedError:
                        raise Exception("Server does not suport STARTTLS command")
                if self.username:
                    server.auth_login()
                    server.login(self.username, self.password)

                server.send_message(email)
                logger.info("Email Sent Successfully!")
            except (
                smtplib.SMTPConnectError,
                smtplib.SMTPSenderRefused,
                smtplib.SMTPAuthenticationError,
                smtplib.SMTPRecipientsRefused,
                smtplib.SMTPServerDisconnected,
                smtplib.SMTPException,
            ) as e:
                raise Exception(f"SMTP Error: {str(e)}")
