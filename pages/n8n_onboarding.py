"""Embed the n8n-hosted client onboarding form."""

import os
from urllib.parse import urlparse

import dash
import dash_bootstrap_components as dbc
from dash import html

from .side_bar import sidebar

dash.register_page(__name__, path="/n8n-client-onboarding", order=1, name="n8n Onboarding")


def _configured_form_url():
    """Return an HTTPS n8n form URL, rejecting malformed configuration."""
    url = os.environ.get("N8N_CLIENT_ONBOARDING_FORM_URL", "").strip()
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        return None
    return url


def layout():
    form_url = _configured_form_url()
    if form_url:
        form_content = dbc.Button(
            "Open secure onboarding form",
            href=form_url,
            target="_blank",
            rel="noopener noreferrer",
            color="primary",
            className="my-3",
        )
    else:
        form_content = dbc.Alert(
            "The onboarding form is not configured yet. Set N8N_CLIENT_ONBOARDING_FORM_URL to the active Production URL from the n8n Form Trigger.",
            color="warning",
        )

    return dbc.Row(
        [
            dbc.Col(sidebar(), xs=4, sm=4, md=2),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("New Client Onboarding Form"),
                                html.P(
                                    "Open the n8n-hosted form to start the client onboarding workflow.",
                                    className="text-muted",
                                ),
                                dbc.Alert(
                                    [
                                        html.Strong("Demo environment. "),
                                        "Use fictional information only. Do not submit confidential, financial, identity, or sensitive personal data.",
                                    ],
                                    color="warning",
                                ),
                                form_content,
                            ]
                        ),
                        className="shadow-sm",
                    ),
                    html.P(
                        [
                            "Workflow source: ",
                            html.A(
                                "n8n Client Onboarding",
                                href="https://github.com/raimiazeez26/n8n-client-onboarding",
                                target="_blank",
                                rel="noopener noreferrer",
                            ),
                        ],
                        className="small text-muted mt-3",
                    ),
                ],
                xs=8,
                sm=8,
                md=10,
                className="p-3",
            ),
        ]
    )
