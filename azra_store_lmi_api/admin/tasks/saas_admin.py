"""This module contains tasks related to SaaS admin operations.

It includes functions for sending credentials to SaaS administrators via email.
"""

from azra_store_lmi_api.config.celery.decorator import async_task
from azra_store_lmi_api.config.logger.app import logger
from azra_store_lmi_api.config.mailer import EmailMessage


@async_task()
async def send_saas_admin_credentials(username: str, email: str, password: str):
    """Send SaaS admin credentials via email.

    This asynchronous function sends an email containing the credentials
    (username, email, and password) to a newly created SaaS admin.

    Args:
        username (str): The username of the SaaS admin.
        email (str): The email address of the SaaS admin.
        password (str): The password for the SaaS admin account.

    Raises:
        Exception: If there's an error while sending the email.

    Returns:
        None

    Logs:
        - Info: When the credentials are successfully sent.
        - Exception: When an error occurs while sending the credentials.
    """
    try:
        message = EmailMessage(to=[email], subject="SAAS Admin Credentials")
        message.set_content(
            "plain",
            f"See your credentials \nusername: {username}\nemail: {email}\npassword: {password}",
        )
        await message.send()
        logger.info("SAAS Admin credentials send successfully.")
    except Exception as exception:
        logger.exception(
            "Error occurred while sending SAAS Admin creadetials: \n%s", str(exception)
        )
