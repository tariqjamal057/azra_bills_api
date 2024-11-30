"""Module for sending emails asynchronously using different mailers.

This module provides an asynchronous class EmailMessage for sending emails using different
mailers, such as SMTP and log. It supports various email configurations including
attachments, CC, and BCC recipients.

Classes:
    EmailMessage: Asynchronous class for composing and sending emails.

Functions:
    None

Attributes:
    None
"""

import os
from typing import List, Optional

from azra_bills_api.config.mailer.log_mail import LogMail
from azra_bills_api.config.mailer.smtp import SMTPMail
from azra_bills_api.config.settings import settings


class EmailMessage:
    """Asynchronous class for composing and sending emails using different mailers.

    This class allows for the creation and sending of email messages with various
    configurations, including multiple recipients, CC, BCC, attachments, and
    different content types.

    Attributes:
        from_ (Optional[str]): The sender's email address.
        to (List[str]): A list of email addresses to send the email to.
        cc (Optional[List[str]]): A list of email addresses for CC recipients.
        bcc (Optional[List[str]]): A list of email addresses for BCC recipients.
        subject (Optional[str]): The subject of the email.
        content (Dict[str, str]): A dictionary to store different types of email content.
        attachments (Dict[str, str]): A dictionary to store attachment filenames and paths.
        suppress_mail (bool): Flag to determine whether to use LogMail instead of actual sending.
        mailer: The mailer object used for sending emails.
    """

    def __init__(
        self,
        to: List[str],
        subject: str,
        from_: str = ("AZRA Bills Admin", settings.MAIL_FROM),
        suppress_mail: bool = False,
        **kwargs,
    ):
        """Initialize the email message with the specified attributes.

        Args:
            to (Optional[List[str]]): A list of email addresses to send the email to.
            from_ (Optional[str]): The sender's email address.
            subject (Optional[str]): The subject of the email.
            suppress_mail (bool): Flag to determine whether to use LogMail instead of
            actual sending.
            **kwargs: Additional keyword arguments for CC and BCC recipients.
        """
        self.from_ = from_
        self.to = to or []
        self.cc = kwargs.get("cc")
        self.bcc = kwargs.get("bcc")
        self.subject = subject
        self.content = {}
        self.attachments = {}
        self.suppress_mail = suppress_mail
        self.mailer = None

    def set_from_email(self, email: str, username: Optional[str] = None) -> None:
        """Sets the sender's email address.

        Args:
            email (str): The sender's email address.
            username (Optional[str]): The username associated with the email address.
        """
        self.from_ = (username, email)

    def set_content(self, content_type: str, content: str) -> None:
        """Sets the content for the specified content type.

        Args:
            content_type (str): The type of content to set.
            content (str): The content to set.
        """
        self.content[content_type] = content

    def add_attachment(self, file_path: str, filename: Optional[str] = None) -> None:
        """Adds an attachment to the email message.

        Args:
            file_path (str): The path to the attachment file.
            filename (Optional[str]): The name of the attachment file. If None, uses
            the basename of file_path.
        """
        if filename is None:
            filename = os.path.basename(file_path)
        self.attachments[filename] = file_path

    async def send_email(self, message_content: dict) -> None:
        """Asynchronously send the email using the specified mailer.

        Args:
            message_content (dict): A dictionary containing the email message details.
        """
        await self.mailer.send(message_content)

    async def send(self):
        """Asynchronously send the email using the appropriate mailer based on configuration."""
        message_content = {
            "from_": self.from_,
            "to": self.to,
            "bcc": self.bcc,
            "cc": self.cc,
            "subject": self.subject,
            "content": self.content,
            "attachments": self.attachments,
        }
        self.mailer = (
            LogMail()
            if self.suppress_mail
            else SMTPMail(
                hostname=settings.MAIL_SERVER,
                port=settings.MAIL_PORT,
                username=settings.MAIL_USERNAME,
                password=settings.MAIL_PASSWORD,
                use_ssl=settings.MAIL_USE_SSL,
            )
        )
        await self.send_email(message_content)
