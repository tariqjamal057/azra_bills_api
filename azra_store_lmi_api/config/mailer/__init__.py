"""This module provides email functionality for the AZRA Store LMI API.

It imports the EmailMessage class from the adapter module, which is used
for creating and sending email messages within the application.

The EmailMessage class offers a convenient interface for composing
emails with various attributes such as recipients, subject, body,
and attachments.

Usage:
    from azra_store_lmi_api.config.mailer import EmailMessage
    import asyncio

    message = EmailMessage()
    message.from_ =('Sender Name', 'sender@example.com')
    message.to = ['recipient@example.com'[]
    message.subject = 'Hello'
    message.set_content('plain', 'This is a test email.')
    asyncio.run(message.send())

Note:
    Ensure proper configuration of email settings in the application
    before using this module.
"""

from azra_store_lmi_api.config.mailer.adapter import EmailMessage as EmailMessage
