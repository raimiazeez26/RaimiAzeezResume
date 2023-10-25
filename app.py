import dash
from dash import Dash, html
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings('ignore')

#import dash_auth

#theme switch
theme_switch = ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.SLATE, dbc.themes.SUPERHERO]) #CYBORG

font_awesome = 'https://use.fontawesome.com/releases/v6.4.0/css/all.css'
    #'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/font-awesome.min.css'
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE, font_awesome], #DARKLY
           suppress_callback_exceptions=True, prevent_initial_callbacks=True,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}]
           )

server = app.server
# auth = dash_auth.BasicAuth(
#     app,
#     {
#         'raimiazeez': 'raimiresume',
#         'myprojects': 'myprojects'
#
#     }
# )

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Nav([
                        dbc.NavLink(page["name"], href=page["path"])
                        for page in dash.page_registry.values()
                        if not page["path"].startswith("/app")
                    ])
            ]),
            theme_switch,
        ],
        fluid=True,
    ),
    dark=True,
    color='dark'
)

app.layout = dbc.Container([header, dash.page_container],
                           style={'textAlign':'center'}, fluid=True,
                           className="border p-4")

if __name__ == '__main__':
	app.run_server()
