from lib2to3.pgen2.pgen import DFAState
from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app
import pdb
#from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

# Get the current date
now = datetime.now()

# Get the first day of the current month
start_of_month = datetime(now.year, now.month, 1)




card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin=dict(l=25, r=25, t=25, b=0)


# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        # Saldo
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Saldo"),
                    html.H5("R$ -", id="p-saldo-dashboards", style={}),
                ], style={"padding-left": "20px", "padding-top": "10px"}),
                dbc.Card(
                    html.Div(className="fa fa-university", style=card_icon), 
                    color="warning",
                    style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                )
            ])
        ], lg=4, md=6, sm=12),

        # Receita
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Receita"),
                    html.H5("R$ -", id="p-receita-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),
                dbc.Card(
                    html.Div(className="fa fa-meh-o", style=card_icon), 
                    color="success",
                    style={"maxWidth": 75, "height": 100, "margin-left": "0px"},
                )
            ])
        ], lg=4, md=6, sm=12),

        # Despesa
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Despesas"),
                    html.H5("R$ -", id="p-despesa-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),
                dbc.Card(
                    html.Div(className="fa fa-meh-o", style=card_icon), 
                    color="danger",
                    style={"maxWidth": 75, "height": 100, "margin-left": "0px"},
                )
            ])
        ], lg=4, md=6, sm=12),
    ], style={"margin": "10px", "margin-left": "0px"}),

    dbc.Row([
        # Filter Card
        dbc.Col([
            dbc.Card([
                html.Legend("Selecionar lançamentos", className="card-filtro"),
                html.Label("Categorias das receitas"),
                html.Div(
                    dcc.Dropdown(
                        id="dropdown-receita",
                        clearable=False,
                        style={"width": "100%"},
                        persistence=True,
                        persistence_type="session",
                        multi=True)                       
                ),

                html.Label("Categorias das despesas", style={"margin-top": "10px"}),
                dcc.Dropdown(
                    id="dropdown-despesa",
                    clearable=False,
                    style={"width": "100%"},
                    persistence=True,
                    persistence_type="session",
                    multi=True
                ),
                html.Legend("Intervalo de Análise", style={"margin-top": "10px"}),
                dcc.DatePickerRange(
                    month_format='DD/MM/YYYY',
                    end_date_placeholder_text='Data...',
                    start_date=start_of_month,
                    end_date=now,
                    with_portal=True,
                    updatemode='singledate',
                    id='date-picker-config',
                    style={'z-index': '100', 'width': '100%', 'height': 'auto'})
            ], className="cardfiltro", style={"padding": "20px"}), 

        ], lg=4, md=12, sm=12),  # Adjust lg, md, and sm properties based on your needs

        # Graph Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody(dcc.Graph(id="graph1"), style={"padding": "50px",}),
            ], style={"margin-left": "0px"},className="graph1")
        ]),
    ]),
])

















# =========  Callbacks  =========== #

# Dropdown Receita
@app.callback([Output("dropdown-receita", "options"),
    Output("dropdown-receita", "value"),
    Output("p-receita-dashboards", "children")],
    Input("store-receitas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return [([{"label": x, "value": x} for x in df.Categoria.unique()]), val, f"R$ {valor}"]

# Dropdown Despesa
@app.callback([Output("dropdown-despesa", "options"),
    Output("dropdown-despesa", "value"),
    Output("p-despesa-dashboards", "children")],
    Input("store-despesas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return [([{"label": x, "value": x} for x in df.Categoria.unique()]), val, f"R$ {valor}"]

# VALOR - saldo
@app.callback(
    Output("p-saldo-dashboards", "children"),
    [Input("store-despesas", "data"),
    Input("store-receitas", "data")])
    
def saldo_total(despesas, receitas):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)

    valor = df_receitas['Valor'].sum() - df_despesas['Valor'].sum()

    return f"R$ {valor}"

@app.callback(
    Output('date-picker-config', 'start_date'),
    [Input('date-picker-config', 'start_date')]
)
def update_start_date(selected_start_date):
    # Atualiza a data de início com a seleção do usuário
    return selected_start_date

if __name__ == '__main__':
    app.run_server(debug=True)




    

# Gráfico 1
@app.callback(
    Output('graph1', 'figure'),
    [Input('store-receitas', 'data'),
    Input('store-despesas', 'data'),
    Input('dropdown-receita', 'value'),
    Input('dropdown-despesa', 'value'),
    Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date'), 
  
          ]    
)
def graph1_show(data_receita, data_despesa, receita, despesa, start_date, end_date):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)

    mask = (df_final['Data'] > start_date) & (df_final['Data'] <= end_date) 
    df_final = df_final.loc[mask]

    df_final = df_final[df_final['Categoria'].isin(receita) | df_final['Categoria'].isin(despesa)]

    # Create traces for revenues and expenses
    trace_receitas = go.Bar(
        x=df_final[df_final['Output']=='Receitas']['Data'],
        y=df_final[df_final['Output']=='Receitas']['Valor'],
        name='Receitas',
        marker=dict(color='green'),  # Set color for revenues
    )

    trace_despesas = go.Bar(
        x=df_final[df_final['Output']=='Despesas']['Data'],
        y=df_final[df_final['Output']=='Despesas']['Valor'],
        name='Despesas',
        marker=dict(color='red'),  # Set color for expenses
    )

    # Create layout for the chart
    layout = go.Layout(
        barmode='group',
        xaxis=dict(title='Data'),
        yaxis=dict(title='Valor'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # Create figure and add traces
    fig = go.Figure(data=[trace_receitas, trace_despesas], layout=layout)

    return fig