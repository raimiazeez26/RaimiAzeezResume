import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from .side_bar import sidebar

dash.register_page(__name__, title='Covid-19 TimeLapse', order=4, name='Covid-19')


def layout():
    from .COVID19_timelapse import covid_map

    try:
        figure = covid_map()
        chart = dcc.Graph(figure=figure, id='line_chart')
    except Exception:
        chart = dbc.Alert(
            "The source dataset is currently unavailable. Please try again when the data service is reachable.",
            color="warning",
        )

    return html.Div(
        dbc.Row(
            [
                dbc.Col(sidebar(), xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col(
                    [
                        html.H3(
                            "Covid-19 TimeLapse",
                            style={"textAlign": "center"},
                            className="p-4",
                        ),
                        html.P(
                            "Following questions about COVID-19 in Africa, I visualized "
                            "the spread around the world from January 2020 using the "
                            "Johns Hopkins repository. What explains the comparatively "
                            "limited spread reported in Africa?",
                            style={"textAlign": "left"},
                        ),
                        dcc.Markdown(
                            """
                            Possible explanations include inconsistent reporting, early
                            herd immunity, and natural resistance. The chart uses
                            historical case data from the Johns Hopkins repository.
                            """,
                            style={"textAlign": "left"},
                        ),
                        html.Hr(),
                        chart,
                    ],
                    xs=8,
                    sm=8,
                    md=10,
                    lg=10,
                    xl=10,
                    xxl=10,
                    className="p-3",
                ),
            ]
        )
    )


