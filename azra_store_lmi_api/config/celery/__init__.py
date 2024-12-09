"""This module initializes Celery configuration for the Azra Bills API.

It imports the async_task decorator from the decorator module, which can be used to define
asynchronous tasks for Celery.
"""

from azra_store_lmi_api.config.celery.decorator import async_task as async_task
