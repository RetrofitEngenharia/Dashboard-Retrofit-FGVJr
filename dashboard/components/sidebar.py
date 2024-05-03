import dash
from dash import html
import dash_bootstrap_components as dbc

def sidebar():

    return html.Div(
        className="sidebar",
        style={
            "width": "100%",
            "height": "50%",
            "backgroundColor": "var(--color-sb)",
            "borderRadius": "var(--border-radius)",
            "padding": "20px",
            "color": "#FFFFFF",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "flex-start",
            "alignItems": "center",
        },
        children=[
            dbc.NavLink(
                [
                    html.Img(src="/assets/logo.png", height="100%"),
                ],
                href="/",
                active="exact",
                style={
                       "position": "relative",
                       "top": "0%",
                       "height": "50%"
                       },
            ),
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.P(page["name"], style={"marginBottom": "20px"}),
                        ],
                        href=page["path"],
                        active="exact",
                        style={
                            "position": "relative",
                            "top": "20%",
                            "padding": "0.7rem",
                            "color": "white",
                            "display": "flex",
                            "borderRadius": "var(--border-radius-items)",
                            "width": "100%",
                            "height": "50%"
                        }
                    ) for page in dash.page_registry.values()
                ],
                vertical=True,
                pills=True,
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "0.5rem",
                    "width": "100%",
                }
            ),
        ],
    )

