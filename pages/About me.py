import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', order=0)

#image card
picture_card = dbc.Card(
    [
        dbc.CardImg(
            src=dash.get_asset_url("Raimi Portrait.jpg"),
            top=True,
            alt="Portrait of Raimi Azeez Babatunde",
            style={"objectFit": "cover", "objectPosition": "center 28%"},
        ),
    ],
    className='border rounded-lg',
)

RESEARCH_INTERESTS = [
    (
        "Evaluating learned policies honestly",
        "Out-of-sample testing, walk-forward validation and strict no-look-ahead replay, so a policy's "
        "reported performance reflects what it would do on data it has never seen.",
    ),
    (
        "Reward design and specification gaming",
        "How the objectives we write down diverge from the behaviour we want, and how agents exploit "
        "the gap between a reward signal and the real goal.",
    ),
    (
        "Constraints, oversight and safe action",
        "Agents that act through limits they cannot bypass, with every decision traced and auditable, "
        "so humans can understand and correct what a policy does.",
    ),
    (
        "Generalisation under distribution shift",
        "Why policies that look strong in training fail when the environment changes, and how to detect "
        "that before deployment rather than after.",
    ),
]

EVIDENCE = [
    (
        "TradingPlayground",
        "/project/trading-playground",
        "A replay environment for Stable-Baselines3 policies (PPO, A2C, DQN, SAC, TD3, RecurrentPPO). "
        "Models act bar by bar with no look-ahead, every action passes an independent risk engine, and "
        "each decision is traced from observation to outcome.",
    ),
    (
        "RA-StrategyLab",
        "/project/ra-strategylab",
        "A research platform where AI interprets ideas but a deterministic engine computes every number, "
        "with look-ahead audits, walk-forward validation, Monte Carlo tests and overfitting warnings.",
    ),
    (
        "NGX Short-Horizon Alpha",
        "/project/ngx-short-horizon-alpha",
        "Reproducible machine-learning research with point-in-time data, expanding walk-forward folds, "
        "and block-bootstrap and Newey–West inference.",
    ),
    (
        "WorldQuant University MSc capstone",
        "https://github.com/raimiazeez26/WQU_Capstone",
        "Co-authored study of a hybrid filter approach to FX signal prediction with an LSTM model.",
    ),
]


def interest_card(title, text):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody([html.H3(title, className="h6 text-info"), html.P(text, className="small mb-0")]),
            className="h-100",
        ),
        xs=12,
        md=6,
        className="mb-3",
    )


def evidence_item(title, href, text):
    external = href.startswith("http")
    return html.Li(
        [
            html.A(
                title,
                href=href,
                target="_blank" if external else None,
                rel="noopener noreferrer" if external else None,
                className="fw-semibold",
            ),
            " — ",
            text,
        ],
        className="mb-2",
    )


def layout():
    return dbc.Row([
        dbc.Col([
            picture_card
        ], xs=12, sm=4, md=3, lg=3, xl=3, xxl=3, className='pt-5 mb-3'),

        dbc.Col([
            html.H1('Raimi Azeez Babatunde', style={'textAlign': 'center'}, className='p4'),
            html.P(
                "Data Scientist · Quantitative Developer · Reinforcement Learning Research",
                className="lead text-center",
            ),
            html.Hr(),
            html.P(
                "I build and evaluate systems that learn to make decisions under uncertainty. I hold an MSc in "
                "Financial Engineering from WorldQuant University, and for several years I have worked on "
                "machine learning, time-series modelling and systematic trading, where a model's mistakes cost "
                "real money and an optimistic backtest is easy to produce and hard to trust."
            ),
            html.P(
                "That experience is why I am drawn to reinforcement learning research. Financial markets are a "
                "demanding testbed for RL: rewards are noisy and delayed, the environment shifts underneath the "
                "agent, and a policy can look excellent while exploiting quirks of its training data. I want to "
                "work on the questions that sit underneath that problem in general: how to specify what an agent "
                "should do, how to evaluate what it has actually learned, and how to keep its behaviour within "
                "limits people can oversee."
            ),

            html.H2("Research interests", className="h4 mt-4 mb-3"),
            dbc.Row([interest_card(title, text) for title, text in RESEARCH_INTERESTS]),

            html.H2("Related work", className="h4 mt-3 mb-3"),
            html.Ul([evidence_item(*item) for item in EVIDENCE]),

            html.H2("What I'm looking for", className="h4 mt-4 mb-3"),
            html.P(
                "Research roles in reinforcement learning, particularly work on evaluation, reward "
                "specification, and the reliability and safety of learning agents. I bring rigorous "
                "experimental practice from quantitative finance, strong Python engineering, and a habit of "
                "building the tooling needed to test an idea properly."
            ),
            html.P(
                [
                    "See my ",
                    html.A("projects", href="/projects"),
                    " and ",
                    html.A("resume", href="/resume"),
                    ", or reach me at ",
                    html.A("LinkedIn", href="https://www.linkedin.com/in/raimi-azeez/", target="_blank", rel="noopener noreferrer"),
                    " and ",
                    html.A("GitHub", href="https://github.com/raimiazeez26", target="_blank", rel="noopener noreferrer"),
                    ".",
                ]
            ),
        ], xs=12, sm=8, md=8, lg=8, xl=8, xxl=8)

    ], justify='center', className='p-3')
