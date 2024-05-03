from dash import Dash, dcc, html, Input, Output, callback, State
import dash
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from utils import data
import calendar 

def filter_box(children, label):
    return html.Div(
        [
            html.Label(label),
            html.Div(
                children,
                className="filter-box",
                style={
                    "width": "100%",
                    "color": "var(--color-black)",
                }
            ),
        ],
        className="filter-box-container",
        style={
            "width": "100%",
            "display": "flex",
            "flexDirection": "column",
        }
    )

def get_available_dates():
    today = datetime.today()
    future = today + relativedelta(months=18)

    available_dates = []

    date = datetime.strptime("2019-08-01", "%Y-%m-%d")

    while date <= future:
        available_dates.append({
            "label": date.strftime("%Y-%m"),
            "value": date.strftime("%Y-%m")
        })
        date = date + relativedelta(months=1)
    
    return available_dates


@callback(
    Output('filtro', 'data'),
    [Input('filtro-btn-aplicar', 'n_clicks')],
    [
        State('filtro-mes-inicial', 'value'),
        State('filtro-mes-final', 'value'),
        State('filtro-ano-inicial', 'value'),
        State('filtro-ano-final', 'value'),
        State('filtro-projeto', 'value'),
    ],
    prevent_initial_call=False  # Important: Allow this callback to run on initial load
)
def update_filtro(n_clicks_apply, mes_inicial, mes_final, ano_inicial, ano_final, projeto):
    ctx = dash.callback_context

    if not ctx.triggered or ctx.triggered[0]['value'] is None:
        # This is the initial load, no button has been clicked yet
        # Set default filter values here
        mes_inicial = mes_inicial or 1
        mes_final = mes_final or 12
        ano_inicial = ano_inicial or 2019
        ano_final = ano_final or datetime.now().year
    else:
        # Convert inputs to integers or use default values
        mes_inicial = int(mes_inicial) if mes_inicial else 1
        mes_final = int(mes_final) if mes_final else 12
        ano_inicial = int(ano_inicial) if ano_inicial else 2019
        ano_final = int(ano_final) if ano_final else datetime.now().year

    inicio = datetime(ano_inicial, mes_inicial, 1)
    ultimo_dia = calendar.monthrange(ano_final, mes_final)[1]
    fim = datetime(ano_final, mes_final, ultimo_dia)

    return {
        "inicio": inicio.strftime("%Y-%m-%d"),
        "fim": fim.strftime("%Y-%m-%d"),
        "agrupamento": "",
        "projeto": projeto
    }
    
@callback(
    Output("filtro-projeto", "options"),
    Input("db_a_pagar", "data"),
    Input("db_a_receber", "data"),
    Input("db_a_receber_vencimento", "data"),
)
def get_projects(data1, data2, data3):
    df1 = data.json_to_df(data1)[["projectName", "projectId"]]
    df2 = data.json_to_df(data2)[["projectName", "projectId"]]
    df3 = data.json_to_df(data3)[["projectName", "projectId"]]

    df = pd.concat([df1, df2, df3]).drop_duplicates().rename(columns={"projectName":"label", "projectId":"value"})

    return df.to_dict(orient="records")


def filtros():
    available_dates = get_available_dates()

    # Set the initial state of the filters
    start_date = available_dates[0]['value']
    end_date = available_dates[-1]['value']

    return html.Div(
        className="filtros",
        id="div-filtro",
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
            html.H1(
                "Filtros", 
                style={
                    "marginBottom": "20px", 
                    "fontSize": "22px"
                }
            ),
            html.Div([
                html.Div(id='n_clicks_hidden', style={'display': 'none'}),  # Hidden Div to store n_clicks
                filter_box(
                    dcc.Dropdown(
                        options=[], 
                        id='filtro-projeto',
                        style={
                            "width": "100%",
                        },
                        optionHeight=50,
                    ),
                    label="Projeto"
                ),
                html.Div([
                    filter_box(
                        dcc.Dropdown(
                            options=[
                                {"label": calendar.month_name[month], "value": month} for month in range(1, 13)
                            ],
                            value=None,
                            id='filtro-mes-inicial',
                            style={
                                "width": "100%",
                            },
                            optionHeight=30,
                            maxHeight=100
                        ),
                        label="Mês Inicial"
                    ),
                    filter_box(
                        dcc.Dropdown(
                            options=[
                                {"label": calendar.month_name[month], "value": month} for month in range(1, 13)
                            ], 
                            value=None,
                            id='filtro-mes-final',
                            style={
                                "width": "100%",
                            },
                            optionHeight=30,
                            maxHeight=100
                        ),
                        label="Mês Final"
                    ),
                    filter_box(
                        dcc.Dropdown(
                            options=[
                                {"label": year, "value": year} for year in range(2019, datetime.now().year + 1)
                            ], 
                            value=None,
                            id='filtro-ano-inicial',
                            style={
                                "width": "100%",
                            },
                            optionHeight=30,
                            maxHeight=100
                        ),
                        label="Ano Inicial"
                    ),
                    filter_box(
                        dcc.Dropdown(
                            options=[
                                {"label": year, "value": year} for year in range(2019, datetime.now().year + 1)
                            ], 
                            value=None,
                            id='filtro-ano-final',
                            style={
                                "width": "100%",
                                "height": "30px"
                            },
                            optionHeight=30,
                            maxHeight=100
                        ),
                        label="Ano Final"
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "grid",
                    "gap": "var(--default-padding)",
                    "grid-template-columns": "1fr 1fr",
                    "grid-template-rows": "1fr 1fr",
                }),
                html.Div([
                    html.Button('Aplicar Filtro', id='filtro-btn-aplicar', style={"margin-top":"5%"}),
                    html.Button('Resetar Filtros', id='filtro-btn-reset', style={"display":"None","margin-top":"5%"}),
                ], style={"display":"flex","justify-content":"center","flexDirection":"column"}),
            ],
            style={
                "width": "100%",
                "display": "flex",
                "gap": "var(--default-padding)",
                "flexDirection": "column",
            }),
        ],
    )