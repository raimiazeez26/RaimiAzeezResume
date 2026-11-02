"""Dash entry point for the portfolio and interactive analytics pages."""

import os

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, html
from dash_bootstrap_templates import ThemeSwitchAIO

FONT_AWESOME = "https://use.fontawesome.com/releases/v6.4.0/css/all.css"

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SLATE, FONT_AWESOME],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

theme_switch = ThemeSwitchAIO(
    aio_id="theme",
    themes=[dbc.themes.SLATE, dbc.themes.SUPERHERO],
)

navigation = dbc.Nav(
    [
        dbc.NavLink(page["name"], href=page["path"], active="exact")
        for page in dash.page_registry.values()
        if not page["path"].startswith("/app")
    ],
    navbar=True,
    className="ms-auto",
)

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Raimi Azeez Babatunde", href="/"),
            dbc.NavbarToggler(id="navbar-toggler", title="Toggle navigation"),
            dbc.Collapse(
                navigation,
                id="navbar-collapse",
                navbar=True,
                is_open=False,
            ),
            theme_switch,
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    expand="lg",
)

app.layout = dbc.Container(
    [header, dash.page_container],
    fluid=True,
    className="border p-4",
)


@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_navigation(n_clicks, is_open):
    """Expand or collapse the mobile navigation menu."""
    if not n_clicks:
        return is_open
    return not is_open


if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8050")),
        debug=False,
    )
