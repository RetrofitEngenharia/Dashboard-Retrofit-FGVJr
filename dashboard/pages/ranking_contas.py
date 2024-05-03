from dash import Input, Output, callback, State
import dash
import pandas as pd
from components import *

from utils import data

name = "Ranking Contas"

dash.register_page(__name__, path="/ranking_credores", name=name)



@callback(
    Output('ranking_credores', 'figure'),
    Input('filtro', 'data'),
    State('db_a_pagar', 'data'),
)
def atualizar_ranking_grafico(filtro, db_a_pagar):
    df_a_pagar = data.json_to_df(db_a_pagar)
    df_a_pagar = data.apply_filter(df_a_pagar, filtro)

    df_a_pagar["financialCategoryName"].fillna("Desconhecido", inplace=True)

    pagamentos_agrupados = df_a_pagar.groupby("financialCategoryName")["amount"].sum().reset_index()

    pagamentos_agrupados = pagamentos_agrupados.sort_values(by="amount", ascending=True)

    fig = px.bar(
        pagamentos_agrupados,
        x="amount",
        y="financialCategoryName",
        orientation="h",
        text="amount",
        color="amount", 
        labels={"amount": "Quantia", "financialCategoryName": "Categoria Financeira"},
        title="Ranking Credores",
    )

    fig.update_traces(marker_color="blue", textposition="outside")

    return fig


@callback(
    Output("table-ranking", "children"),
    Input("db_plano_financeiro", "data"),
    Input("db_a_pagar", "data"),
)

def update_table(db_plano_financeiro, db_a_pagar2):
    # Step 1: Create auxiliary table
    df_a_pagar = data.json_to_df(db_a_pagar2)

    # Agrupe os dados por 'financialCategoryId' e some os valores de 'amount'
    df_grouped = df_a_pagar.groupby('financialCategoryId')['amount'].sum().reset_index()

    # Renomeie as colunas
    df_grouped.columns = ['Idindicado', 'valor']
    
    # Step 2: Merge values into the financial plan table
    df = data.json_to_df(db_plano_financeiro)

    df_merged = pd.merge(df_grouped, df, how='left', left_on='Idindicado', right_on='id')

    # Remova a coluna 'id', se desejar
    df_merged.drop(columns=['id'], inplace=True)

    # Renomeie a coluna 'Idindicado' para 'ID'
    df_merged.rename(columns={'Idindicado': 'ID'}, inplace=True)

    # Formate os valores na coluna 'valor' para terem o símbolo 'R$' e duas casas decimais
    df_merged['valor'] = 'R$' + df_merged['valor'].astype(str).apply(lambda x: '{:.2f}'.format(float(x)))

    # Reordene as colunas para ter 'name' seguido por 'valor'
    df_merged = df_merged[['ID', 'name', 'valor']]

    dont_display = ['(+) Crédito de INSS Retido', '(-) Crédito de INSS Retido', 'Crédito de INSS Retido', '(-) INSS', '(+) INSS', 'INSS']
    df_merged = df_merged.loc[~df_merged['name'].isin(dont_display)]
    
    return dbc.Table.from_dataframe(
        df_merged,
        striped=True,
        bordered=True, 
        hover=True, 
        index=False,
        style={
            "width": "100%",
            "height": "100%",
            "margin": "0",
        }
    )


layout = content(
    [
        grid(
            [
                container(
                    [
                        ranking_credores(id="ranking_credores")
                    ],
                    style={
                        "gridColumn": "1 / 7",
                        "gridRow": "1 / 2",
                    }
                ),
                container(
                    [
                        table(id="table-ranking")
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