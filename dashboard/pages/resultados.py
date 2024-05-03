from dash import Input, Output, callback, State
from components import card
from utils import data, formaters
import dash
from components import *
import pandas as pd
import plotly.express as px
import calendar

name = "Previsto - Recebido"

dash.register_page(__name__, path="/", name=name)

@callback(
    Output("container-cards", "children"),
    Output("table-resultados", "children"),
    Output("resultados", "figure"),
    Input("filtro", "data"),
    State("db_a_receber_vencimento", "data"),
    State("db_a_receber", "data"),
)
def update_resultados(filtro, db_a_receber_vencimento, db_a_receber):
    df_a_receber_vencimento = data.apply_filter(data.json_to_df(db_a_receber_vencimento)[["dueDate", "projectName", "amount", "projectId"]], filtro, ["projectName", "projectId"]).rename(columns={"amount":"recebimento_previsto", "dueDate":"data"})
    df_a_receber = data.apply_filter(data.json_to_df(db_a_receber)[["paymentDate", "projectName", "amount", "projectId"]], filtro, ["projectName", "projectId"]).rename(columns={"amount":"recebimentos", "paymentDate":"data"})

    # Cards
    receita = df_a_receber["recebimentos"].sum()
    receita_prevista = df_a_receber_vencimento["recebimento_previsto"].sum()
    resultado = receita - receita_prevista
    cards = [
        card("Previsto", formaters.real(receita_prevista), "card-resultados-receita"),
        card("Realizado", formaters.real(receita), "card-resultados-receita"),
        card("Distorção", formaters.real(resultado), "card-resultados-receita"),
    ]

    # Tabela
    df = pd.merge(df_a_receber_vencimento, df_a_receber, on=["data", "projectName"], how="outer")
    df["distorção"] = df["recebimentos"].fillna(0) - df["recebimento_previsto"].fillna(0)
    df = df[["projectName", "data", "recebimentos", "recebimento_previsto", "distorção"]].rename(columns={"projectName":"Projeto", "data":"Período", "recebimentos":"Recebimentos", "recebimento_previsto":"Recebimentos Previstos", "distorção":"Distorção"})

    df["Recebimentos"] = df["Recebimentos"].fillna(0).apply(lambda x: formaters.real(x))
    df["Recebimentos Previstos"] = df["Recebimentos Previstos"].fillna(0).apply(lambda x: formaters.real(x))
    df["Distorção"] = df["Distorção"].fillna(0).apply(lambda x: formaters.real(x))

    df['Período'] = pd.to_datetime(df['Período'], format='%Y%m')
    df['Período'] = df['Período'].dt.strftime('%Y-%m')  # Formatação da coluna 'Período' para string

    result = df.groupby(['Projeto', 'Período'], sort=False)[["Recebimentos", "Recebimentos Previstos", "Distorção"]].sum().unstack(level=1)
    result.columns = result.columns.swaplevel(0, 1)
    result.sort_index(axis=1, level=0, inplace=True)

    table = dbc.Table.from_dataframe(
        result, 
        striped=True, 
        bordered=True, 
        hover=True, 
        index=True,
        style={
            "width": "100%",
            "height": "100%",
            "margin": "0",
            "overflow-x": "auto",
        }
    )

    # Gráfico
    df_final = pd.merge(df_a_receber_vencimento, df_a_receber, on="data", how="outer")
    df_final["distorção"] = df_final["recebimentos"].fillna(0) - df_final["recebimento_previsto"].fillna(0)
    df_final["data"] = pd.to_datetime(df_final["data"], format="%Y%m")

    fig = px.bar(df_final, 
        x="data", 
        y=["recebimento_previsto", "recebimentos", "distorção"],
        labels={"value": "Valor", "variable": "Categoria"},
        title="Resultados - Previsto vs Realizado vs Distorção",
        template="plotly_white"
    )

    # Update the legend, names, and colors
    fig.update_traces(overwrite=True, marker=dict(line=dict(width=0)))
    fig.for_each_trace(lambda t: t.update(name=t.name.replace('recebimento_previsto', 'Previsto').replace('recebimentos', 'Realizado').replace('distorção', 'Distorção')))
    fig.update_layout(barmode='group', xaxis_tickformat='%b %Y', legend_title_text='Categoria')

    return (cards, table, fig)

layout = content(
    [
        grid(
            [
                container(
                    [
                        resultados("resultados")
                    ],
                    style={
                        "gridColumn": "1 / 6",
                        "gridRow": "1 / 2",
                    }
                ),
                container(
                    [],
                    id="container-cards",
                    style={
                        "gridColumn": "6 / 7",
                        "gridRow": "1 / 2",
                    }
                ),
                container(
                    [
                        table(id="table-resultados")
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
