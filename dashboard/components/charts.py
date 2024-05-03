from dash import dcc
import plotly.express as px


def analise_fluxo(id):
    fruits = ["apples", "oranges", "bananas"]
    fig = px.line(x=fruits, y=[1,3,2], color=px.Constant("This year"),
                labels=dict(x="Fruit", y="Amount", color="Time Period"))
    fig.add_bar(x=fruits, y=[2,1,3], name="Last year")

    return dcc.Graph(
        figure=fig, 
        style={
            "height": "100%", 
            "width": "100%"
        },
        id=id
    )


def resultados(id):
    years = ['2016', '2017', '2018']

    fig = px.bar(
        x=years,
        y=[500, 600, 700],
        base=[-500, -600, -700],
        color_discrete_sequence=['crimson'],
        labels={'y': 'Amount'},
        title='Expenses'
    )

    fig.add_bar(
        x=years,
        y=[300, 400, 700],
        base=0,
        marker_color='lightslategrey',
        name='Revenue'
    )

    fig.update_layout(
        xaxis_title='Years',
        yaxis_title='Amount',
        barmode='relative'
    )

    return dcc.Graph(
        figure=fig, 
        style={
            "height": "100%", 
            "width": "100%"
        },
        id=id
    ) 


def ranking_credores(id):

    df = px.data.tips()
    fig = px.bar(df, x="total_bill", y="day", orientation='h')

    return dcc.Graph(
        figure=fig, 
        style={
            "height": "100%", 
            "width": "100%"
        },
        id=id
    )
