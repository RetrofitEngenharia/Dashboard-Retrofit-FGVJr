from dash import dcc, html, Dash
from threading import Thread
import sys
import webview
import os
from components.sidebar import sidebar
from components.filtros import filtros
import dash
from api.sheets import Sheets
import plotly.express as px
from utils import data
import dash_auth


DASH_TITLE = "Dashboard Retrofit"

global_styles = os.path.join("assets/styles", "global.css")

px.defaults.template = "ggplot2"

app = Dash(
    __name__, 
    title=DASH_TITLE,
    pages_folder="pages",
    use_pages=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

auth = dash_auth.BasicAuth(
    app,
    {'admin':"admin"}
)

s = Sheets()

app.layout = html.Div(
    [
        dcc.Store(id='db_orcamento', storage_type='session', data=data.df_to_json(s.orcamento_empresarial)),
        dcc.Store(id='db_a_pagar', storage_type='session', data=data.df_to_json(s.pago)),
        dcc.Store(id='db_a_receber', storage_type='session', data=data.df_to_json(s.recebido)),
        dcc.Store(id='db_a_receber_vencimento', storage_type='session', data=data.df_to_json(s.contas_a_receber_vencimento)),
        dcc.Store(id='db_plano_financeiro', storage_type='session', data=data.df_to_json(s.plano_financeiro)),

        dcc.Store(
            id='filtro', 
            storage_type='session', 
            data={
                "inicio":None,
                "fim":None,
                "agrupamento":"mensal",
                "projeto":None
            }
        ),

        html.Div(
            [
                sidebar(),
                filtros(),
            ],
            style={
                "width": "300px",
                "display": "flex",
                "flexDirection": "column",
                "gap": "var(--default-padding)",
            }
        ),

        dash.page_container
    ],
    className="my_app",
    style={
        "width": "100%",
        "height": "100vh",
        "display": "flex",
        "flexDirection": "row",
        "padding":"var(--default-padding)",
        "gap":"var(--default-padding)",
    },
)

if __name__ == '__main__':

    if len(sys.argv) == 1:
        def run_app():
            app.run_server(debug=False)

        t = Thread(target=run_app)
        t.daemon = True
        t.start()

        window = webview.create_window(
            DASH_TITLE, 
            "http://127.0.0.1:8050/",
            maximized=True,
            zoomable=True
        )

        webview.start(
            debug=False,
        )
    
    elif len(sys.argv) == 2 and sys.argv[1] == 'debug':
        app.run_server(debug=True)

    else:
        app.run_server(debug=True)


