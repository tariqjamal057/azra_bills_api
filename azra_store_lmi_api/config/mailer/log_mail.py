"""Module for logging mail sending operations asynchronously.

This module provides asynchronous classes for logging details of mail sending operations. The
LogMail class inherits from BaseMail and overrides its send method to include logging functionality
in an asynchronous manner.
"""

from email.mime.text import MIMEText
from typing import Any, Dict

from azra_store_lmi_api.config.mailer.base import BaseMail


class EmailData:
    """A class to represent email data.

    Attributes:
        from_ (str): The sender's email address.
        to (str): The recipient's email address.
        bcc (str): The BCC recipients' email addresses.
        cc (str): The CC recipients' email addresses.
        subject (str): The subject of the email.
        content (str): The content of the email.
    """

    def __init__(self, from_: str, to: str, bcc: str, cc: str, subject: str, content: str):
        self.from_ = from_
        self.to = to
        self.bcc = bcc
        self.cc = cc
        self.subject = subject
        self.content = content

    def __str__(self) -> str:
        """Returns a string representation of the EmailData object.

        Returns:
            str: A string representation of the EmailData object.
        """
        return f"EmailData(from_={self.from_}, to={self.to}, subject={self.subject})"


class LogMail(BaseMail):
    """Class for logging mail sending asynchronously.

    This class provides an asynchronous method to log the details of a mail send operation.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize the LogMail object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.response = EmailData

    async def send(self, message: Dict[str, Any]) -> EmailData:
        """Sends the mail asynchronously and logs the details of the operation.

        Args:
            message (Dict[str, Any]): A dictionary containing the email message details.

        Returns:
            EmailData: An EmailData object containing the logged email information.
        """
        mail_content = None
        content_type = None
        for type_, content in message["content"].items():
            mail_content = content
            content_type = type_

        content = MIMEText(mail_content, content_type)

        return self.response(
            from_=self._format_emails_address(message["from_"]),
            to=",".join(message["to"]),
            bcc=",".join(message["bcc"]) if message["bcc"] else "",
            cc=",".join(message["cc"]) if message["cc"] else "",
            subject=message["subject"],
            content=content.get_payload(),
        )
