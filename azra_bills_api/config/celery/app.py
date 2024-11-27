"""Module for configuring and initializing Celery for running background tasks.

This module provides functionality for setting up Celery with the appropriate broker URL
and result backend, using settings from the Settings class. It also configures
automatic task discovery for various application modules.

The main components of this module include:
1. Importing necessary modules (Celery and settings)
2. Creating a Celery instance
3. Configuring the broker URL and connection retry settings
4. Setting up automatic task discovery

Usage:
    Import the 'celery' instance from this module to use in other parts of the application
    for defining and executing background tasks.

Returns:
    Celery: A configured Celery instance ready for task execution.
"""

from celery import Celery

from azra_bills_api.config.settings import settings

celery = Celery(__name__)


celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.broker_connection_retry_on_startup = True


celery.autodiscover_tasks([])  # point the app background module in list
