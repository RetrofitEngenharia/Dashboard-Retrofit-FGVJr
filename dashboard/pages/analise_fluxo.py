from dash import Input, Output, callback, State
import dash
from components import *
from utils import data, formaters
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np

name = "Análise de Fluxo"

dash.register_page(__name__, path="/analise_fluxo", name=name)

@callback(
    Output("container-cards-fluxo", "children"),
    Output("table-fluxo", "children"),
    Output("analise_fluxo", "figure"),
    Input("filtro", "data"),
    State("db_a_pagar", "data"),
    State("db_a_receber", "data"),
)
def update_fluxo(filtro, db_a_pagar, db_a_receber):
    df_a_pagar = data.json_to_df(db_a_pagar)
    # dont_display = ['(+) Crédito de INSS Retido', '(-) Crédito de INSS Retido', 'Crédito de INSS Retido', '(-) INSS', '(+) INSS', 'INSS', 'INSS S/ Folha de Pagamento']
    # df_a_pagar = df_a_pagar[~df_a_pagar["financialCategoryName"].isin(dont_display)]
    df_a_pagar = data.apply_filter(df_a_pagar[["paymentDate", "projectName", "amount", "projectId"]], filtro, ["projectName", "projectId"]).rename(columns={"amount":"pagamentos"})

    df_a_receber = data.apply_filter(data.json_to_df(db_a_receber)[["paymentDate", "projectName", "amount", "projectId"]], filtro, ["projectName", "projectId"]).rename(columns={"amount":"recebimentos"})

    # Define aggregation methods for different types of columns
    aggregations = {col: 'sum' for col in df_a_pagar.select_dtypes(include=[np.number]).columns}
    aggregations["paymentDate"] = 'first'  # For datetime columns

    # Group by and aggregate without setting groupby columns as index
    df_a_pagar = df_a_pagar.groupby(["projectName", "projectId"], as_index=False).agg(aggregations)
    # df_a_pagar = df_a_pagar.group_by(["projectName", "projectId","financialCategoryName"])

    # Cards
    receita = df_a_receber["recebimentos"].sum()
    despesa = df_a_pagar["pagamentos"].sum()
    resultado = receita - despesa

    cards = [
        card("Receitas", formaters.real(receita), "card-resultados-receita"),
        card("Despesas", formaters.real(despesa), "card-resultados-receita"),
        card("Resultado", formaters.real(resultado), "card-resultados-receita")
    ]

    # Tabela
    df = pd.merge(df_a_pagar, df_a_receber, on=["paymentDate", "projectName"], how="outer")[["projectName", "paymentDate", "pagamentos", "recebimentos"]].rename(columns={"projectName":"Projeto", "paymentDate":"Período", "pagamentos":"Pagamentos", "recebimentos":"Recebimentos"})
    df["Período"] = pd.to_datetime(df["Período"], format="%Y%m")
    df.sort_values(by="Período", inplace=True)
    df["Período"] = df["Período"].dt.strftime('%b %Y')
    df["Pagamentos"].fillna(0, inplace=True)
    df["Recebimentos"].fillna(0, inplace=True)
    df["Pagamentos"] = df["Pagamentos"].apply(lambda x: formaters.real(x, 10))
    df["Recebimentos"] = df["Recebimentos"].apply(lambda x: formaters.real(x, 10))
    
    table = dbc.Table.from_dataframe(
        df, 
        striped=True, 
        bordered=True, 
        hover=True, 
        index=False,
        className="table-bordered",
        style={
            "width": "100%",
            "height": "100%",
            "margin": "0",
        }
    )

    # Figura
    pagamentos_agrupados = df_a_pagar.groupby("paymentDate")["pagamentos"].sum().reset_index()
    recebimentos_agrupados = df_a_receber.groupby("paymentDate")["recebimentos"].sum().reset_index()

    df_final = pd.merge(pagamentos_agrupados, recebimentos_agrupados, on="paymentDate", how="outer")
    df_final["paymentDate"] = pd.to_datetime(df_final["paymentDate"], format="%Y%m")
    df_final.sort_values('paymentDate', inplace=True)

    df_final["pagamentos"].fillna(0, inplace=True)
    df_final["recebimentos"].fillna(0, inplace=True)

    df_final["dif_receb_pag"] = df_final["recebimentos"] - df_final["pagamentos"]
    df_final["dif_receb_pag_acumulada"] = df_final["dif_receb_pag"].cumsum()

    fig = px.bar(df_final, 
        x="paymentDate", 
        y=["recebimentos", "pagamentos"],
        color_discrete_map={"recebimentos": "green", "pagamentos": "red"},
        labels={"value": "Valor", "variable": "Categoria"},
        template="plotly"
    )

    fig.add_trace(
        go.Scatter(
            x=df_final["paymentDate"],
            y=df_final["dif_receb_pag_acumulada"],
            mode="lines",  # Use only "lines" to avoid markers
            line=dict(color="blue"),
            name="Resultado Acumulado"
        )
    )

    fig.update_layout(
        title="Diferença Acumulada entre Recebimentos e Pagamentos",
        xaxis_title="Data de Pagamento",
        yaxis_title="Montante",
        showlegend=True,
        barmode="group"
    )
    
    return (cards, table, fig)


layout = content(
    [
        grid(
            [
                container(
                    [
                        analise_fluxo("analise_fluxo")
                    ],
                    style={
                        "gridColumn": "1 / 6",
                        "gridRow": "1 / 2",
                    }
                ),
                container(
                    [],
                    style={
                        "gridColumn": "6 / 7",
                        "gridRow": "1 / 2",
                    },
                    id="container-cards-fluxo"
                ),
                container(
                    [
                        table(id="table-fluxo")
                    ],
                    style={
                        "gridColumn": "1 / 7",
                        "gridRow": "2 / 3",
                    }
                )
            ],
        )
    ]
)