"""This module contains the BaseMail class for sending emails asynchronously.

This module provides a base class for sending emails with various features such as formatting email
addresses, building multipart content, adding attachments, and composing extra email fields like CC
and BCC.
"""

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union

import aiofiles


class BaseMail:
    """Mail Base class contains the helper functions for sending emails asynchronously.

    This class provides utility methods for formatting email addresses, building multipart content,
    adding attachments, and composing extra email fields. It serves as a foundation for creating
    more specific email sending classes.
    """

    def _format_emails_address(self, email_address: Union[str, tuple]) -> str:
        """Format the email address by adding the name if provided.

        This method takes an email address as either a string or a tuple containing
        a name and an email address. It formats the email address appropriately,
        including the name if provided.

        Args:
            email_address (Union[str, tuple]): The email address to be formatted.

        Returns:
            str: The formatted email address.
        """
        name: Optional[str] = None
        if isinstance(email_address, tuple):
            name, email_address = email_address

        if name is not None:
            parsed = f"{name} <{email_address}>"
            return parsed
        return f"<{email_address}>"

    async def build_multipart_content(
        self, email: MIMEMultipart, type_: str, content: str
    ) -> None:
        """Build multipart content and attach it to the email asynchronously.

        This method creates a MIMEText object with the given content and type,
        and attaches it to the provided email message.

        Args:
            email (MIMEMultipart): The email to attach the content to.
            type_ (str): The type of content (e.g., 'plain', 'html').
            content (str): The actual content to attach.

        Returns:
            None
        """
        data = MIMEText(content, type_)
        email.attach(data)

    async def _add_attachment(
        self, file_path: str, filename: Optional[str], msg: MIMEMultipart
    ) -> None:
        """Add an attachment to the email message asynchronously.

        This method reads a file from the given file path and attaches it to the
        email message as an attachment.

        Args:
            file_path (str): The path to the file to be attached.
            filename (Optional[str]): The filename to be used for the attachment.
                If None, the original file name will be used.
            msg (MIMEMultipart): The email message to attach the file to.

        Returns:
            None
        """
        async with aiofiles.open(file_path, "rb") as attachment_file:
            content = await attachment_file.read()
            part = MIMEApplication(content)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={file_path if not filename else filename}",
            )
            msg.attach(part)

    def _compose_extra_emails(
        self,
        message: dict,
        msg: MIMEMultipart,
    ) -> None:
        """Add extra email fields to the email message asynchronously.

        This method adds CC and BCC fields to the email message if they are
        provided in the message dictionary.

        Args:
            message (dict): A dictionary containing email information.
            msg (MIMEMultipart): The email message to add the extra fields to.

        Returns:
            None
        """
        if "cc" in message and message["cc"] is not None:
            msg["Cc"] = ",".join(message["cc"])
        if "bcc" in message and message["bcc"] is not None:
            msg["Bcc"] = ",".join(message["bcc"])
