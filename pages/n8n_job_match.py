"""Launcher for the n8n Job and CV AI Match form workflow."""

import dash

from .n8n_form_page import form_page

dash.register_page(__name__, path="/n8n-job-match", order=3, name="AI Job Match")


def layout():
    return form_page(
        title="Analyse Job and CV Match",
        environment_key="N8N_AI_MATCH_FORM_URL",
        description=(
            "Enter an existing application ID and choose whether to rerun the "
            "AI comparison against the selected CV."
        ),
        warning="Use fictional or non-sensitive sample data when trying this demonstration.",
    )
