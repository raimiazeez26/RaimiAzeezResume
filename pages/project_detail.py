"""Reusable layout for repository-backed project detail pages."""

import dash_bootstrap_components as dbc
from dash import html

from .side_bar import sidebar


def render_project(title, category, summary, features, technologies, repository, status, notes=None, local_copy=None):
    """Render a structured project overview with source and status context."""
    feature_list = [html.Li(item) for item in features]
    content = [
        html.Div(category.upper(), className="small text-info fw-bold mb-2"),
        html.H2(title, className="mb-3"),
        html.P(summary, className="lead"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(dbc.CardBody([html.H4("What it does"), html.Ul(feature_list)]), className="h-100"),
                    md=7,
                    className="mb-3",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Project details"),
                                html.P([html.Strong("Technology: "), technologies]),
                                html.P([html.Strong("Status: "), status]),
                                html.A("View source repository", href=repository, target="_blank", rel="noopener noreferrer", className="btn btn-outline-info btn-sm"),
                            ]
                        ),
                        className="h-100",
                    ),
                    md=5,
                    className="mb-3",
                ),
            ]
        ),
    ]
    if notes:
        content.extend([html.H4("Implementation notes", className="mt-3"), html.Ul([html.Li(note) for note in notes])])
    if local_copy:
        content.extend(
            [
                html.Hr(),
                html.H4("Local source copy"),
                html.P(local_copy),
            ]
        )
    content.extend([html.Hr(), html.A("← All projects", href="/projects", className="btn btn-outline-light btn-sm")])
    return html.Div(
        dbc.Row(
            [
                dbc.Col(sidebar(), xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col(content, xs=8, sm=8, md=10, lg=10, xl=10, xxl=10, className="p-3"),
            ]
        )
    )
