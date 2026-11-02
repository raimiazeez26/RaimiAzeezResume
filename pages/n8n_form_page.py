"""Shared launcher layout for n8n-hosted form-trigger workflows."""

import os
from urllib.parse import urlparse

import dash_bootstrap_components as dbc
from dash import html

from .side_bar import sidebar

REPOSITORY_URL = "https://github.com/raimiazeez26/n8n-client-onboarding"


def form_page(title, environment_key, description, warning=None):
    """Build a page that opens a configured production n8n form."""
    url = os.environ.get(environment_key, "").strip()
    parsed = urlparse(url)
    is_secure_url = parsed.scheme == "https" and bool(parsed.netloc)

    if is_secure_url:
        form_action = dbc.Button(
            "Open form",
            href=url,
            target="_blank",
            rel="noopener noreferrer",
            color="primary",
            className="my-3",
        )
    else:
        form_action = dbc.Alert(
            f"This form is not configured yet. Set {environment_key} to the active Production URL from its n8n Form Trigger.",
            color="warning",
        )

    content = [
        html.H2(title),
        html.P(description, className="text-muted"),
    ]
    if warning:
        content.append(dbc.Alert(warning, color="warning"))
    content.append(form_action)
    content.append(
        html.P(
            [
                "Workflow source: ",
                html.A(
                    "n8n Client Onboarding",
                    href=REPOSITORY_URL,
                    target="_blank",
                    rel="noopener noreferrer",
                ),
            ],
            className="small text-muted mt-3",
        )
    )

    return dbc.Row(
        [
            dbc.Col(sidebar(), xs=4, sm=4, md=2),
            dbc.Col(
                dbc.Card(dbc.CardBody(content), className="shadow-sm"),
                xs=8,
                sm=8,
                md=10,
                className="p-3",
            ),
        ]
    )
