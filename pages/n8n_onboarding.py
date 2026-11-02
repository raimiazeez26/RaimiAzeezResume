"""Launcher for the n8n Client Onboarding form workflow."""

import dash

from .n8n_form_page import form_page

dash.register_page(__name__, path="/n8n-client-onboarding", order=1, name="Client Onboarding")


def layout():
    return form_page(
        title="New Client Onboarding Form",
        environment_key="N8N_CLIENT_ONBOARDING_FORM_URL",
        description="Open the n8n-hosted form to start the client onboarding workflow.",
        warning=(
            "Demo environment. Use fictional information only. Do not submit confidential, "
            "financial, identity, or sensitive personal data."
        ),
    )
