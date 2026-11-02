"""External form for the n8n client onboarding automation."""

import os

import dash
import dash_bootstrap_components as dbc
import requests
from dash import Input, Output, State, callback, dcc, html

from .side_bar import sidebar

dash.register_page(__name__, path="/n8n-client-onboarding", order=1, name="n8n Onboarding")

COMPANY_SIZES = [
    "1 person",
    "2-10 employees",
    "11-50 employees",
    "51-200 employees",
    "More than 200 employees",
]
SERVICES = [
    "AI Automation",
    "Data Analysis",
    "Dashboard Development",
    "Python Development",
    "Workflow Integration",
    "Consulting",
    "Other",
]
COMMUNICATION_CHANNELS = ["Email", "Phone", "Whatsapp", "Google Meet", "Zoom"]


def _field(label, component, required=False, help_text=None):
    children = [dbc.Label(label, html_for=component.id)]
    if required:
        children.append(html.Span(" *", className="text-danger"))
    if help_text:
        children.append(html.Small(help_text, className="form-text text-muted d-block"))
    children.append(component)
    return dbc.Form(children, className="mb-3")


def layout():
    form = dbc.Card(
        dbc.CardBody(
            [
                html.H2("New Client Onboarding Form"),
                html.P(
                    "Share a brief about your project. Submissions are processed by the linked n8n workflow.",
                    className="text-muted",
                ),
                dbc.Alert(
                    [
                        html.Strong("Demo environment. "),
                        "Use fictional information only. Do not submit confidential, financial, identity, or sensitive personal data.",
                    ],
                    color="warning",
                ),
                _field("Full name", dbc.Input(id="onboarding-full-name", type="text", required=True, maxLength=160), True),
                _field("Email address", dbc.Input(id="onboarding-email", type="email", required=True, maxLength=254), True),
                _field("Phone number", dbc.Input(id="onboarding-phone", type="tel", maxLength=40)),
                _field("Company name", dbc.Input(id="onboarding-company", type="text", required=True, maxLength=200), True),
                _field("Company size", dbc.Select(id="onboarding-company-size", options=[{"label": "Select a range (optional)", "value": ""}] + [{"label": value, "value": value} for value in COMPANY_SIZES], value="")),
                _field("Industry", dbc.Input(id="onboarding-industry", type="text", maxLength=120)),
                _field(
                    "Service required",
                    dbc.Checklist(
                        id="onboarding-services",
                        options=[{"label": value, "value": value} for value in SERVICES],
                        value=[],
                        inline=False,
                        inputClassName="me-2",
                    ),
                    True,
                ),
                _field("Describe your project", dbc.Textarea(id="onboarding-description", required=True, minLength=10, maxLength=5000, rows=5, placeholder="What are you looking to accomplish?"), True),
                _field("Preferred start date", dbc.Input(id="onboarding-start-date", type="date")),
                _field("Estimated budget", dbc.Input(id="onboarding-budget", type="number", min=0, step="any", placeholder="Optional")),
                _field("Preferred communication channel", dbc.Select(id="onboarding-channel", options=[{"label": "Select a channel (optional)", "value": ""}] + [{"label": value, "value": value} for value in COMMUNICATION_CHANNELS], value="")),
                _field(
                    "I understand this is a demonstration environment and will submit fictional information only.",
                    dbc.Checkbox(id="onboarding-demo-ack", value=False),
                    True,
                ),
                dbc.Button("Submit onboarding request", id="onboarding-submit", color="primary", type="submit"),
                html.Div(id="onboarding-result", role="status", className="mt-3", **{"aria-live": "polite"}),
            ]
        ),
        className="shadow-sm",
    )
    return dbc.Row(
        [
            dbc.Col(sidebar(), xs=4, sm=4, md=2),
            dbc.Col(
                [
                    dcc.Loading(form, type="dot"),
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


@callback(
    Output("onboarding-result", "children"),
    Input("onboarding-submit", "n_clicks"),
    State("onboarding-full-name", "value"),
    State("onboarding-email", "value"),
    State("onboarding-phone", "value"),
    State("onboarding-company", "value"),
    State("onboarding-company-size", "value"),
    State("onboarding-industry", "value"),
    State("onboarding-services", "value"),
    State("onboarding-description", "value"),
    State("onboarding-start-date", "value"),
    State("onboarding-budget", "value"),
    State("onboarding-channel", "value"),
    State("onboarding-demo-ack", "value"),
    prevent_initial_call=True,
)
def submit_onboarding(
    n_clicks,
    full_name,
    email,
    phone,
    company_name,
    company_size,
    industry,
    services,
    project_description,
    preferred_start_date,
    estimated_budget,
    communication_channel,
    demo_ack,
):
    """Validate and forward an onboarding submission from the server."""
    if not n_clicks:
        return ""

    full_name = (full_name or "").strip()
    email = (email or "").strip()
    company_name = (company_name or "").strip()
    project_description = (project_description or "").strip()
    services = [service for service in (services or []) if service in SERVICES]

    if not full_name or not email or not company_name or not project_description or not services or not demo_ack:
        return dbc.Alert("Please complete all required fields and confirm the demo-data notice.", color="danger")
    if len(project_description) < 10:
        return dbc.Alert("Please provide at least 10 characters describing the project.", color="danger")
    if len(full_name) > 160 or len(email) > 254 or len(company_name) > 200 or len(project_description) > 5000:
        return dbc.Alert("One or more fields exceed the allowed length.", color="danger")
    if estimated_budget not in (None, ""):
        try:
            estimated_budget = float(estimated_budget)
            if estimated_budget < 0:
                raise ValueError
        except (TypeError, ValueError):
            return dbc.Alert("Estimated budget must be a non-negative number.", color="danger")
    else:
        estimated_budget = None

    webhook_url = os.environ.get("N8N_CLIENT_ONBOARDING_WEBHOOK_URL", "").strip()
    if not webhook_url:
        return dbc.Alert(
            "Onboarding submission is not configured yet. Set N8N_CLIENT_ONBOARDING_WEBHOOK_URL on the app server.",
            color="warning",
        )

    payload = {
        "full_name": full_name,
        "email": email,
        "phone": (phone or "").strip(),
        "company_name": company_name,
        "company_size": company_size or "",
        "industry": (industry or "").strip(),
        "service_required": services,
        "project_description": project_description,
        "preferred_start_date": preferred_start_date or "",
        "estimated_budget": estimated_budget,
        "communication_channel": communication_channel or "",
        "demo_data_acknowledged": True,
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=(5, 20))
    except requests.RequestException:
        return dbc.Alert("We could not reach the onboarding workflow. Please try again later.", color="danger")

    if not response.ok:
        return dbc.Alert("The onboarding workflow could not accept this request. Please try again later.", color="danger")
    return dbc.Alert("Your onboarding request was submitted successfully.", color="success")
