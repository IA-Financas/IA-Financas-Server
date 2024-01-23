import os
import dash
import json
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from datetime import datetime, date

import pdb
from dash_bootstrap_templates import ThemeChangerAIO

# ========= DataFrames ========= #
import numpy as np
import pandas as pd
from globals import *

df_cat_receita = pd.read_csv("C:/Users/gabri/Downloads/Projeto Dashboard de Finanças--/Projeto Dashboard de Finanças--/arquivos CSV/df_cat_receita.csv")

cat_receita = df_cat_receita['Categoria'].tolist()

df_cat_despesa = pd.read_csv("C:/Users/gabri/Downloads/Projeto Dashboard de Finanças--/Projeto Dashboard de Finanças--/arquivos CSV/df_cat_despesa.csv")
cat_despesa = df_cat_despesa['Categoria'].tolist()

# ========= Layout ========= #
layout = dbc.Card([
   # html.H1(id="titulo-iafinanças",style={"width": "190px", "overflowY": "auto"}, className="text-primary"),
   # html.P("iafinanças", className="text-black"),  # Alterado para text-black
  #  html.Hr(),

 # html.Div([
 #  dcc.Input(id="input-titulo-iafinanças",style={"width": "150px", "overflowY": "auto"}, type="text", placeholder="iafinanças",
 #             value="iafinanças",  # Adicionado o valor padrão
 #             ),
              
#]),





    # Seção PERFIL ------------------------
                dbc.Button(id='botao_avatar',
                    children=[html.Img(src="/assets/img_hom.png", id="avatar_change", alt="Avatar", className='perfil_avatar'),
                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),

                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Selecionar Perfil")),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_hom.png", className='perfil_avatar', top=True),
                                    dbc.CardBody([
                                        html.H4("Perfil Pessoal", className="card-title"),
                                        html.P(
                                            "Seu perfil para finanças pessoais",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_fem2.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Perfil Empresa", className="card-title"),
                                        html.P(
                                            "Adicione um perfil de empresa, crie relatorios personalizados",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_home.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Perfil Casa", className="card-title"),
                                        html.P(
                                            "Crie um perfil para suas contas de casa e outras",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar",  color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_plus.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Adicionar Novo Perfil", className="card-title"),
                                        html.P(
                                            "Adicione um novo perfil personalizado",
                                            className="card-text",
                                        ),
                                        dbc.Button("Adicionar", color="success"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                    ]),
                ],
                style={"background-color": "rgba(0, 0, 0, 0.5)"},
                id="modal-perfil",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True
                ),  

    # Seção + NOVO ------------------------
            dbc.Row([
    dbc.Col([
        dbc.Button(
            color="success",
            id="open-novo-receita",
            children=["+ Receita"],
            style={"font-size": "10px", "padding": "5px 10px"}
        ),
    ], width=6),
    dbc.Col([
        dbc.Button(
            color="danger",
            id="open-novo-despesa",
            children=["+ Despesa"],
            style={"font-size": "10px", "padding": "5px 10px"}
        ),
    ], width=6)
]),

            # Modal Receita
            html.Div([
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Adicionar receita")),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                    dbc.Label("Descrição: "),
                                    dbc.Input(placeholder="Ex.: dividendos da bolsa, herança...", id="txt-receita"),
                            ], width=6), 
                            dbc.Col([
                                    dbc.Label("Valor: "),
                                    dbc.Input(placeholder="$100.00", id="valor_receita", value="")
                            ], width=6)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Data: "),
                                dcc.DatePickerSingle(id='date-receitas',
                                    min_date_allowed=date(2020, 1, 1),
                                    max_date_allowed=date(2030, 12, 31),
                                    date=datetime.today(),
                                    style={"width": "100%"}
                                ),
                            ], width=4),

                            dbc.Col([
                                dbc.Label("Extras"),
                                dbc.Checklist(
                                    options=[{"label": "Foi recebida", "value": 1},
                                        {"label": "Receita Recorrente", "value": 2}],
                                    value=[1],
                                    id="switches-input-receita",
                                    switch=True),
                            ], width=4),

                            dbc.Col([
                                html.Label("Categoria da receita"),
                                dbc.Select(id="select_receita", options=[{"label": i, "value": i} for i in cat_receita], value=cat_receita[0])
                            ], width=4)
                        ], style={"margin-top": "25px"}),
                        
                        dbc.Row([
                            dbc.Accordion([
                                    dbc.AccordionItem(children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    html.Legend("Adicionar categoria", style={'color': 'green'}),
                                                    dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-receita", value=""),
                                                    html.Br(),
                                                    dbc.Button("Adicionar", className="btn btn-success", id="add-category-receita", style={"margin-top": "20px"}),
                                                    html.Br(),
                                                    html.Div(id="category-div-add-receita", style={}),
                                                ], width=6),

                                                dbc.Col([
                                                    html.Legend("Excluir categorias", style={'color': 'red'}),
                                                    dbc.Checklist(
                                                        id="checklist-selected-style-receita",
                                                        options=[{"label": i, "value": i} for i in cat_receita],
                                                        value=[],
                                                        label_checked_style={"color": "red"},
                                                        input_checked_style={"backgroundColor": "#fa7268",
                                                            "borderColor": "#ea6258"},
                                                    ),                                                            
                                                    dbc.Button("Remover", color="warning", id="remove-category-receita", style={"margin-top": "20px"}),
                                                ], width=6)
                                            ]),
                                        ], title="Adicionar/Remover Categorias",
                                    ),
                                ], flush=True, start_collapsed=True, id='accordion-receita'),
                                    
                                    html.Div(id="id_teste_receita", style={"padding-top": "20px"}),
                                
                                    dbc.ModalFooter([
                                        dbc.Button("Adicionar Receita", id="salvar_receita", color="success"),
                                        dbc.Popover(dbc.PopoverBody("Receita Salva"), target="salvar_receita", placement="left", trigger="click"),
                                        ])
                            ], style={"margin-top": "25px"}),
                        ])
                ],
                style={"background-color": "rgba(17, 140, 79, 0.05)"},
                id="modal-novo-receita",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True)
            ]),



            ### Modal Despesa ###
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Adicionar despesa")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                                dbc.Label("Descrição: "),
                                dbc.Input(placeholder="Ex.: dividendos da bolsa, herança...", id="txt-despesa"),
                        ], width=6), 
                        dbc.Col([
                                dbc.Label("Valor: "),
                                dbc.Input(placeholder="$100.00", id="valor_despesa", value="")
                        ], width=6)
                    ]),

                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Data: "),
                            dcc.DatePickerSingle(id='date-despesas',
                                min_date_allowed=date(2020, 1, 1),
                                max_date_allowed=date(2030, 12, 31),
                                date=datetime.today(),
                                style={"width": "100%"}
                            ),
                        ], width=4),

                        dbc.Col([
                            dbc.Label("Opções Extras"),
                            dbc.Checklist(
                                options=[{"label": "Foi recebida", "value": 1},
                                    {"label": "despesa Recorrente", "value": 2}],
                                value=[1],
                                id="switches-input-despesa",
                                switch=True),
                        ], width=4),

                        dbc.Col([
                            html.Label("Categoria da despesa"),
                            dbc.Select(id="select_despesa", options=[{"label": i, "value": i} for i in cat_despesa])
                        ], width=4)
                    ], style={"margin-top": "25px"}),
                    
                    dbc.Row([
                        dbc.Accordion([
                                dbc.AccordionItem(children=[
                                    dbc.Row([
                                        dbc.Col([
                                            html.Legend("Adicionar categoria", style={'color': 'green'}),
                                            dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-despesa", value=""),
                                            html.Br(),
                                            dbc.Button("Adicionar", className="btn btn-success", id="add-category-despesa", style={"margin-top": "20px"}),
                                            html.Br(),
                                            html.Div(id="category-div-add-despesa", style={}),
                                        ], width=6),

                                        dbc.Col([
                                            html.Legend("Excluir categorias", style={'color': 'red'}),
                                            dbc.Checklist(
                                                id="checklist-selected-style-despesa",
                                                options=[{"label": i, "value": i} for i in cat_despesa],
                                                value=[],
                                                label_checked_style={"color": "red"},
                                                input_checked_style={"backgroundColor": "#fa7268",
                                                    "borderColor": "#ea6258"},
                                            ),                                                            
                                            dbc.Button("Remover", color="warning", id="remove-category-despesa", style={"margin-top": "20px"}),
                                        ], width=6)
                                    ]),
                                ], title="Adicionar/Remover Categorias",
                                ),
                            ], flush=True, start_collapsed=True, id='accordion-despesa'),
                                                    
                        dbc.ModalFooter([
                            dbc.Button("Adicionar despesa", color="error", id="salvar_despesa", value="despesa"),
                            dbc.Popover(dbc.PopoverBody("Despesa Salva"), target="salvar_despesa", placement="left", trigger="click"),
                        ]
                        )
                    ], style={"margin-top": "25px"}),
                ])
            ],
            style={"background-color": "rgba(17, 140, 79, 0.05)"},
            id="modal-novo-despesa",
            size="lg",
            is_open=False,
            centered=True,
            backdrop=True),
        
# Seção NAV ------------------------
html.Hr(),
dbc.Nav(
    [
        html.Button(
    [html.I(className="fa fa-bars", style={'font-size': '24px', 'color': 'white'})],  # Adjust font-size and color
    id="sidebar_toggle",
    n_clicks=0,
    style={"background-color": "transparent", "border": "none"},
),

        dbc.NavLink(
    dbc.Col(
        [   
            html.I(className="fa fa-home", style={'font-size': '34px', 'color': 'white', 'vertical-align': 'middle'}),
            html.P("Home", style={'color': 'white', 'margin-top': '5px', 'font-size': '14px'}),
        ],
        width="auto",
        align='center',
        style={'transition': 'transform 0.2s'},
        id='navlink-home',
    ),
    href="/Home",
    active="false",
    className="active-link"
    
),
        dbc.NavLink(
    dbc.Col(
        [
            html.I(className="fa fa-money", style={'font-size': '34px', 'color': 'white', 'vertical-align': 'middle'}),
            html.P("Dashboard", style={'color': 'white', 'margin-top': '5px', 'font-size': '14px'}),
        ],
        width="auto",
        align='center',
        style={'transition': 'transform 0.2s'},
        id='navlink-dashboard'
    ),
    href="/dashboards",
    active="false"
),
        dbc.NavLink(
    dbc.Col(
        [
            html.I(className="fa fa-file-text", style={'font-size': '34px', 'color': 'white', 'vertical-align': 'middle'}),
            html.P("Extratos", style={'color': 'white', 'margin-top': '5px', 'font-size': '14px'}),
        ],
        width="auto",
        align='center',
        style={'transition': 'transform 0.2s'},  # Adiciona transição para suavizar a animação
        id='navlink-extratos'  # Adiciona um ID para referência no CSS
    ),
    href="/extratos",
    active="false"
),
        dbc.NavLink(
    dbc.Col(
        [
            html.I(className="fa fa-money", style={'font-size': '34px', 'color': 'white', 'vertical-align': 'middle'}),
            html.P("iafinanças", style={'color': 'white', 'margin-top': '5px', 'font-size': '14px'}),
        ],
        width="auto",
        align='center',
        style={'transition': 'transform 0.2s'},
        id='navlink-iafinancas'
    ),
    href="/iafinanças",
    active="false"
),
    ],
    vertical=True,
    pills=True,
    id='nav_buttons',
    style={"margin-bottom": "40px", "text-align": "center"}
),
             ], id='sidebar_completa', style={"overflowY": "auto",'background-color': '#1d44b8'})






# =========  Callbacks  =========== #


# Pop-up receita
@app.callback(
    Output("modal-novo-receita", "is_open"),
    Input("open-novo-receita", "n_clicks"),
    State("modal-novo-receita", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


# Pop-up despesa
@app.callback(
    Output("modal-novo-despesa", "is_open"),
    Input("open-novo-despesa", "n_clicks"),
    State("modal-novo-despesa", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


# Pop-up perfis
@app.callback(
    Output("modal-perfil", "is_open"),
    Input("botao_avatar", "n_clicks"),
    State("modal-perfil", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Add/Remove categoria despesa
@app.callback(
    [Output("category-div-add-despesa", "children"),
    Output("category-div-add-despesa", "style"),
    Output("select_despesa", "options"),
    Output('checklist-selected-style-despesa', 'options'),
    Output('checklist-selected-style-despesa', 'value'),
    Output('stored-cat-despesas', 'data')],

    [Input("add-category-despesa", "n_clicks"),
    Input("remove-category-despesa", 'n_clicks')],

    [State("input-add-despesa", "value"),
    State('checklist-selected-style-despesa', 'value'),
    State('stored-cat-despesas', 'data')]
)
def add_category(n, n2, txt, check_delete, data):
    cat_despesa = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {'color': 'red'}

        else:
            cat_despesa = cat_despesa + [txt] if txt not in cat_despesa else cat_despesa
            txt1 = f'A categoria {txt} foi adicionada com sucesso!'
            style1 = {'color': 'green'}
    
    if n2:
        if len(check_delete) > 0:
            cat_despesa = [i for i in cat_despesa if i not in check_delete]  
    
    opt_despesa = [{"label": i, "value": i} for i in cat_despesa]
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    data_return = df_cat_despesa.to_dict()

    return [txt1, style1, opt_despesa, opt_despesa, [], data_return]


# Add/Remove categoria receita
@app.callback(
    [Output("category-div-add-receita", "children"),
    Output("category-div-add-receita", "style"),
    Output("select_receita", "options"),
    Output('checklist-selected-style-receita', 'options'),
    Output('checklist-selected-style-receita', 'value'),
    Output('stored-cat-receitas', 'data')],

    [Input("add-category-receita", "n_clicks"),
    Input("remove-category-receita", 'n_clicks')],

    [State("input-add-receita", "value"),
    State('checklist-selected-style-receita', 'value'),
    State('stored-cat-receitas', 'data')]
)
def add_category(n, n2, txt, check_delete, data):
    cat_receita = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {'color': 'red'}

    if n and not(txt == "" or txt == None):
        cat_receita = cat_receita + [txt] if txt not in cat_receita else cat_receita
        txt1 = f'A categoria {txt} foi adicionada com sucesso!'
        style1 = {'color': 'green'}
    
    if n2:
        if check_delete == []:
            pass
        else:
            cat_receita = [i for i in cat_receita if i not in check_delete]  
    
    opt_receita = [{"label": i, "value": i} for i in cat_receita]
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receita.to_csv("df_cat_receita.csv")
    data_return = df_cat_receita.to_dict()

    return [txt1, style1, opt_receita, opt_receita, [], data_return]

    

# Enviar Form receita
@app.callback(
    Output('store-receitas', 'data'),

    Input("salvar_receita", "n_clicks"),

    [
        State("txt-receita", "value"),
        State("valor_receita", "value"),
        State("date-receitas", "date"),
        State("switches-input-receita", "value"),
        State("select_receita", "value"),
        State('store-receitas', 'data')
    ]
)
def salve_form_receita(n, descricao, valor, date, switches, categoria, dict_receitas):
    df_receitas = pd.DataFrame(dict_receitas)

    if n and not(valor == "" or valor== None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0] if type(categoria) == list else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0

        df_receitas.loc[df_receitas.shape[0]] = [valor, recebido, fixo, date, categoria, descricao]
        df_receitas.to_csv("df_receitas.csv")

    data_return = df_receitas.to_dict()
    return data_return


# Enviar Form despesa
@app.callback(
    Output('store-despesas', 'data'),
    Input("salvar_despesa", "n_clicks"),
    [
        State("valor_despesa", "value"),
        State("switches-input-despesa", "value"),
        State("select_despesa", "value"),
        State("date-despesas", "date"),
        State("txt-despesa", "value"),
        State('store-despesas', 'data')
    ]
)
def salve_form_despesa(n, valor, switches, descricao, date, txt, dict_despesas):
    df_despesas = pd.DataFrame(dict_despesas)

    # Inicialize a variável categoria fora do bloco condicional
    categoria = None

    if n and not(valor == "" or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()

        # Atribua um valor à variável categoria dentro do bloco condicional
        categoria = dict_despesas.get('categoria', [])[0] if 'categoria' in dict_despesas else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0
        
        if descricao == None or descricao == "":
            descricao = 0

        df_despesas.loc[df_despesas.shape[0]] = [valor, recebido, fixo, date, descricao, txt]
        df_despesas.to_csv("df_despesas.csv")

    data_return = df_despesas.to_dict()
    return data_return

# Callback para atualizar o título "MyBudget" quando pressionar Enter
@app.callback (
    Output("titulo-iafinanças", "children"),
    Input("input-titulo-iafinanças", "n_submit"),
    State("input-titulo-iafinanças", "value")
)
def update_iafinanças_title_on_submit(n_submit, user_defined_title):
    return user_defined_title or "iafinanças"

@app.callback(
    Output("navbar", "className"),
    Output("nav_buttons", "style"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar", "className")
)
def toggle_navbar(n_clicks, current_class):
    if n_clicks and "show" not in current_class:
        new_class = current_class + " show"
        nav_style = {"text-align": "left"}
    else:
        new_class = current_class.replace(" show", "")
        nav_style = {"text-align": "center"}

    return new_class, nav_style