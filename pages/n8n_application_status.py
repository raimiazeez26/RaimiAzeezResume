"""Launcher for the n8n Job Application Status form workflow."""

import dash

from .n8n_form_page import form_page

dash.register_page(__name__, path="/n8n-application-status", order=4, name="Application Status")


def layout():
    return form_page(
        title="Update Job Application Status",
        environment_key="N8N_APPLICATION_STATUS_FORM_URL",
        description=(
            "Select an existing application, record its latest status, and add an "
            "optional next action or interview date."
        ),
        warning="Use fictional or non-sensitive sample data when trying this demonstration.",
    )
