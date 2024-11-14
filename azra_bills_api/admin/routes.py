"""This module defines a application of azra_bills project in FastAPI.

It setup FastApi instance 'admin and includes multiple API routers for endpoints related to the
admin app

This module also configures CORS middleware for the application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

admin_app = FastAPI(
    title="AZRA Bills Admin App",
    summary="This is the admin app for AZRA Bills project",
    description="In this app we can manage all multi and single store's setup and manage the "
    "'AZRA Bills' Saas Admin users along with common primary data such as "
    "countries, states, cities, holidays, and store's setup",
    version="1.0.0",
)

admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
