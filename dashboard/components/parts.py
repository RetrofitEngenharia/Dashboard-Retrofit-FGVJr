from dash import html
import os

def table(id):
    return html.Div(
        [],
        className="my_table",
        id=id,
        style={
            "width": "100%",
            "height": "inherit",
            "overflowY": "auto",
        }
    )

def card(title, number, id=""):
    
    return html.Div(
        [
            html.H2(
                title,
                style={
                    "fontSize":"15px",
                    "margin": "0",
                }
            ),
            html.Div(
                [
                    html.P(
                        number, 
                        className="card_number",
                        style={
                            "fontSize": "20px",
                        }
                    ) if number else None,
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "flexDirection": "row",
                    "justifyContent": "center",
                    "gap": "var(--default-padding)",
                }
            )
        ],
        id=id,
        className="my_card",
        style={
            "backgroundColor": "var(--color-text)",
            "borderRadius": "var(--border-radius-items)",
            "width": "100%",
            "height": "100%",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
        },
    )

def svg(file_name):
    file_path = os.path.join("assets", file_name)
    return html.Img(src=file_path)

