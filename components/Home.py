import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, render_template
from datetime import datetime
import pandas as pd

# Carregar os dados
df_despesas = pd.read_csv('df_despesas.csv')
df_receitas = pd.read_csv('df_receitas.csv')

app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.now().strftime("%B, %Y")
    return render_template('index.html', today=today)

if __name__ == '__main__':
    app.run(debug=True)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def criar_card_iafinancas():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H2("Bem-vindos ao IAFINANÇAS"),
                    html.Div(className="card-divider"),
                    html.P(
                    "Bem vindo ao iafinanças"                    ),
                    
                ]
            ),
        ],
        className='card',
    )

def criar_card_disciplina():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H2("Acesse a Plataforma Disciplina Financeira"),
                    html.Div(className="card-divider"),
                    html.P(
                        "Se você está determinado a dar um salto em direção ao seu futuro financeiro sólido, "
                        "então está na hora de explorar a plataforma de investimentos do 'Disciplina Financeira'. "
                        "Aqui, não apenas falamos sobre disciplina financeira, mas também fornecemos as ferramentas "
                        "e recursos necessários para colocar seus planos em ação."
                    ),
                    dbc.Button(
                        'Acessar Plataforma',
                        id='btn-disciplina',
                        n_clicks=0,
                        href='https://disciplinafinanceira.orama.com.br/login#/',
                        target="_blank",
                        color="primary",
                        className='btn-card'
                    ),
                ],
                style={"overflow": "auto"}
            ),
        ],
        className='card',
    )
def criar_card_podcasts():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H2("PodCasts"),
                    html.Div(className="card-divider"),
                    html.P(
                        "Assista os podcasts do discplina"
                    ),
                    dbc.Button(
                        'Acessar Plataforma',
                        id='btn-disciplina',
                        n_clicks=0,
                        href='https://www.youtube.com/@discilplinafinanceirapodcast',
                        target="_blank",
                        color="primary",
                        className='btn-card'
                    ),
                ],
                style={"overflow": "auto"}
            ),
        ],
        className='card',
    )


def criar_card_calendario():
    today = datetime.now().strftime("%d/%m")
    proxima_rotina_texto = atualizar_proxima_rotina()

    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Calendário de Rotinas", className='text-center mb-4'),  # Centralizar o título
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P(
                                    f"{today}",
                                    id='current-date',
                                    className='text-center py-2 px-3 rounded',
                                    style={
                                        "fontSize": "18px",  # Tamanho da fonte reduzido
                                        "fontWeight": "bold",
                                        "margin": "0",
                                        "border": "2px solid #2925A2",
                                        "background-color": "#007BFF",  # Fundo azul
                                        "color": "white",  # Texto em branco
                                        "border-radius": "5px",
                                        "width": "fit-content",  # Ajusta a largura conforme o conteúdo
                                        "float": "left",  # Alinha no canto esquerdo
                                         "margin-right": "10px",  # Adiciona um espaçamento à direita se necessário
                                    }
                                ),
                                html.P(
                                    proxima_rotina_texto,
                                    id='next-routine',
                                    className='text-center py-2 rounded',
                                    style={
                                        "fontSize": "20px",
                                        "margin": "0",
                                        "border-radius": "10px",
                                         "border": "2px solid #CED4DA",  # Adiciona a borda cinza
                                        "padding": "10px",  # Adiciona preenchimento interno para a borda
                                    }
                                ),
                            ],
                            md=6,  # Ajuste este valor conforme necessário
                        ),
                    ]
                ),
            ]
        ),
        className='card'
    )
def criar_card_financas():
  # card_icon = {"fontSize": "4em", "color": "#FFD700", "max-height": "150px","overflow":"auto"}  # Ajuste conforme necessário
    card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H2("Suas Finanças"),
                    html.Div(className="card-divider"),
                    html.P(
                        
                    ),
                    dbc.CardGroup(
                        [
                            dbc.Card(
                                [
                                    html.Legend("Saldo"),
                                    html.H5("R$ -", id="p-saldo-dashboards", style={}),
                                ],
                                style={"padding-left": "20px", "padding-top": "10px","max-height":"100px","overflow":"auto"},
                            ),
                            dbc.Card(
                                html.Div(className="fa fa-university", style=card_icon),
                                color="warning",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            ),
                        ]
                    ),
                ]
            ),
        ],
        className='card',
    )

def atualizar_proxima_rotina():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar se as colunas necessárias estão presentes nos dataframes
    required_columns = ['Data', 'Categoria']
    if not all(col in df_despesas.columns for col in required_columns) or not all(col in df_receitas.columns for col in required_columns):
        return "Erro: Colunas necessárias ausentes nos dataframes."

    # Concatenar despesas e receitas
    rotinas_fixas = pd.concat([df_receitas, df_despesas], ignore_index=True)
    
    # Garantir que a coluna 'Data' esteja no formato datetime
    rotinas_fixas['Data'] = pd.to_datetime(rotinas_fixas['Data'], errors='coerce')
    
    # Filtrar rotinas futuras
    rotinas_futuras = rotinas_fixas[rotinas_fixas['Data'].notnull() & (rotinas_fixas['Data'] >= today)]
    
    # Ordenar por data
    rotinas_futuras = rotinas_futuras.sort_values(by='Data')

    if not rotinas_futuras.empty:
        proxima_rotina = rotinas_futuras.iloc[0]
        proxima_data = proxima_rotina['Data'].strftime('%Y-%m-%d')
        if proxima_data == today:
            proxima_rotina_texto = f"Próxima rotina HOJE: {proxima_rotina['Categoria']}"
        else:
            proxima_rotina_texto = f"Próxima rotina em {proxima_rotina['Data'].strftime('%d/%m/%y')}: {proxima_rotina['Categoria']}"
        return proxima_rotina_texto
    else:
        return "Não há rotinas fixas futuras."
    


layout = html.Div(
    [
       
        dbc.Row(
            [
                dbc.Col(criar_card_iafinancas(), width='auto', className='col-md-4 tres-primeiros-cards'),
                dbc.Col(criar_card_disciplina(), width='auto', className='col-md-4 tres-primeiros-cards'),
                dbc.Col(criar_card_podcasts(), width='auto', className='col-md-4 tres-primeiros-cards'),
                dbc.Col(criar_card_calendario(), width='auto', className='col-md-8'),
                dbc.Col(criar_card_financas(), width='auto', className='col-md-4'),
            ],
            className='card-container',
        ),

        html.Div(id='info-output'),
        
        dcc.Interval(
            id='calendario-update',
            interval=60000,  # Atualizar a cada 60 segundos (ajuste conforme necessário)
            n_intervals=0
        ),
    ],
    className='main-container',
)

@app.callback(
    Output('info-output', 'children'),
    [Input('btn-iafinancas', 'n_clicks'), Input('btn-disciplina', 'n_clicks')],
)
def show_info(btn_iafinancas, btn_disciplina):
    ctx = dash.callback_context
    if not ctx.triggered_id:
        return ""

    button_id = ctx.triggered_id('.')[0]
    if button_id == 'btn-iafinancas':
        return "Você clicou no botão 'Acessar IAFINANÇAS'."
    elif button_id == 'btn-disciplina':
        return "Você clicou no botão 'Acessar Disciplina Financeira'."
    else:
        return ""

@app.callback(
    Output('current-date', 'children'),
    [Input('calendario-update', 'n_intervals')]
)
def update_calendario(n_intervals):
    return atualizar_proxima_rotina()



if __name__ == '__main__':
    app.run_server(debug=True)
