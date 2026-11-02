"""Launcher for the n8n Job Application Tracker form workflow."""

import dash

from .n8n_form_page import form_page

dash.register_page(__name__, path="/n8n-job-application", order=2, name="Job Application Form")


def layout():
    return form_page(
        title="Job Application Tracker",
        environment_key="N8N_JOB_APPLICATION_FORM_URL",
        description=(
            "Record a job opportunity or submitted application. The workflow stores "
            "the application and can continue with matching and follow-up automations."
        ),
        warning="Use fictional or non-sensitive sample data when trying this demonstration.",
    )
