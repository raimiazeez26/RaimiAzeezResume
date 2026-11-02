"""Embedded RAIMI-ANALYST technical market assistant page."""

import dash
import dash_bootstrap_components as dbc
from dash import html

from .side_bar import sidebar


dash.register_page(__name__, name="RAIMI-ANALYST", path="/app-tagpt", order=32)

_ANALYST_URL = "https://raimianalyst-acf53a71f53d.herokuapp.com/"


def layout():
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(sidebar(), xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col(
                    [
                        html.H2("RAIMI-ANALYST", className="text-center"),
                        html.P("An intelligent technical analyst for financial-market exploration."),
                        html.Iframe(
                            src=_ANALYST_URL,
                            title="RAIMI-ANALYST",
                            style={"width": "100%", "height": "76vh", "minHeight": "560px", "border": "0", "borderRadius": "8px"},
                        ),
                        html.P(
                            ["If the assistant does not load, open it directly: ", html.A("RAIMI-ANALYST", href=_ANALYST_URL, target="_blank", rel="noopener noreferrer")],
                            className="small text-muted mt-2",
                        ),
                    ],
                    xs=8,
                    sm=8,
                    md=10,
                    lg=10,
                    xl=10,
                    xxl=10,
                    className="p-3",
                ),
            ],
            className="g-0",
        ),
        fluid=True,
    )
