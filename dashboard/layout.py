import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import plotting as pl
import pandas as pd

df = pl.df#pd.read_csv('../ds/remuneracao_servidores.csv', sep=',', header=0, decimal='.', parse_dates=['DATA'])

nomes = df['NOME'].drop_duplicates()
orgaos = pl.orgaos
anos = pl.anos
meses = pl.meses
dt_atual = df['DATA'].max()
dt_formatada = str(dt_atual.month)+'/'+str(dt_atual.year)

df_teste = df[df['DATA'] == dt_atual][['NOME', 'ORGAO']].head(10)

def load_layout():
    component = html.Div(className='main-container', children=[
        html.Div(className='header-container', children=[
            html.H1(className='header', children=[
                'Transparência do Governo do Amazonas'
            ]),
            
            html.H4(className='info', children=[
                'Portal de análise dos dados referentes à remuneração dos servidores públicos do governo  do Amazonas.'
            ])
        ]),

        html.Div(className='plot-header', children=[
            html.H4(className='', children=[
                'Órgãos'
            ])
        ]),

        html.Div(id='orgao', className='plot-container', children=[

            html.Div(className='plot', children=[
                html.H2('Maior Remuneração Legal Total (R$)'),
                html.H3('Soma da Remuneração Legal Total de cada órgão por mês. No gráfico, somente os que receberam acima de 10 milhões.'),
                dcc.Graph(
                    id='graph',
                    figure=pl.org_rem_total(),
                )
            ]),

            html.Div(className='plot', children=[
                html.H2('Remuneração Legal Total Individual (R$)'),
                html.H3('Soma da Remuneração Legal Total por órgão.'),
                html.Div(className='options-container', children=[
                    dcc.Dropdown(
                        id='dropdown2',
                        className='input',
                        options=[{'label':i, 'value':i} for i in orgaos],
                        value=orgaos[0],
                        placeholder='Selecione um Órgão',
                        clearable=False
                    )
                ]),
                dcc.Graph(
                    id='graph_org_rem_total_indiv',
                )
            ]),

            html.Div(className='plot', children=[
                html.H2('Aumento/Corte no orçamento'),
                html.H4('Diferença da soma da remuneração legal total de um mês para o outro. Sendo a diferença maior ou menor que 50.000.'),
                html.Div(className='options-container', children=[
                    html.Div(children=[
                        html.H4('Mês'),
                        dcc.Dropdown(
                            id='dropdown_meses_1',
                            className='input',
                            options=[{'label':i, 'value':i} for i in meses],
                            value=dt_atual.month,
                            placeholder='Mês',
                            clearable=False,
                            searchable=False
                        ),
                    ]),
                    html.Div(children=[
                        html.H4('Ano'),
                        dcc.Dropdown(
                            id='dropdown_anos_1',
                            className='input',
                            options=[{'label':i, 'value':i} for i in anos],
                            value=dt_atual.year,
                            placeholder='Ano',
                            clearable=False,
                            searchable=False
                        )
                    ])
                ]),
                dcc.Graph(
                    id='graph_aumento',
                )
            ])
        ]),

        html.Div(className='plot-header', children=[
            html.H4(className='', children=[
                'Servidores'
            ])
        ]),

        html.Div(id='servidores', className='plot-container', children=[

            html.Div(className=' plot', children=[
                html.Div(
                    id='registrados-container',
                    className='sub-plot',
                    children=[
                        html.H1('Numero de Funcionários'),
                        html.H2(children=[
                            'Registrados (', anos.min(), ' - ', anos.max(), ')'
                        ]),
                        dcc.Graph(
                            id='graph_serv_num_reg',
                            figure=pl.serv_num_reg()
                        ),
                        html.H2(children=[
                            'Ativos (', dt_formatada, ')'
                        ]),
                        dcc.Graph(
                            id='graph_serv_num_ativo',
                            figure=pl.serv_num_ativos()
                        )
                    ]
                ),
                html.Div(
                    id='serv-mais-org-container',
                    className='sub-plot',
                    children=[
                        html.H1('Funcionários presentes em mais de um órgão.'),
                        dt.DataTable(
                            id='dt_serv_mais_org',
                            columns=[{"name": col, "id": col} for col in pl.serv_mais_org().columns],
                            data=pl.serv_mais_org().to_dict('records'),
                            style_table={
                                'display': 'flex',
                                'flex-direction': 'column',
                                'align-itens': 'center'
                            },
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'textAlign': 'center'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            page_size=15
                        )
                    ]
                ),
                html.Div(
                    id='serv-dupl-mesmo-org',
                    className='sub-plot',
                    children=[
                        html.H1('Servidores duplicados no mesmo órgão.'),
                        html.Div(
                            className='serv_dupl_container',
                            children=[
                                html.Div(className='dt-container', children=[
                                    html.H2('Por órgão'),
                                    dt.DataTable(
                                        id='dt_serv_dupl_org',
                                        columns=[{'name': col, 'id': col} for col in pl.serv_duplicados('org').columns],
                                        data=pl.serv_duplicados('org').to_dict('records'),
                                        style_table={
                                            'display': 'flex',
                                            'flex-direction': 'column',
                                            'align-itens': 'center'
                                        },
                                        style_header={
                                            'backgroundColor': 'rgb(30, 30, 30)',
                                            'textAlign': 'center'
                                        },
                                        style_cell={
                                            'backgroundColor': 'rgb(50, 50, 50)',
                                            'color': 'white',
                                            'textAlign': 'left'
                                        },
                                        page_size=15
                                    )
                                ]),
                                html.Div(children=[
                                    html.H2('Por ano'),
                                    dt.DataTable(
                                        id='dt_serv_dupl_ano',
                                        columns=[{'name': col, 'id': col} for col in pl.serv_duplicados('data').reset_index().columns],
                                        data=pl.serv_duplicados('data').reset_index().to_dict('records'),
                                        style_table={
                                            'display': 'flex',
                                            'flex-direction': 'column',
                                            'align-itens': 'center'
                                        },
                                        style_header={
                                            'backgroundColor': 'rgb(30, 30, 30)',
                                            'textAlign': 'center'
                                        },
                                        style_cell={
                                            'backgroundColor': 'rgb(50, 50, 50)',
                                            'color': 'white',
                                            'textAlign': 'left'
                                        },
                                        page_size=15
                                    )
                                ])
                            ]
                        ),
                        html.H2('Busca de servidores duplicados'),
                        html.Div(className='options-container', children=[
                            html.Div(children=[
                                html.H2('Órgão'),
                                dcc.Dropdown(
                                    id='dropdown_busca_org',
                                    className='input',
                                    options=[{'label':i, 'value':i} for i in orgaos],
                                    value=orgaos[3],
                                    placeholder='Mês',
                                    clearable=False,
                                    searchable=False
                                )
                            ]),
                            html.Div(children=[
                                html.H2('Ano'),
                                dcc.Dropdown(
                                    id='dropdown_busca_ano',
                                    className='input',
                                    options=[{'label':i, 'value':i} for i in anos],
                                    value=dt_atual.year,
                                    placeholder='Mês',
                                    clearable=False,
                                    searchable=False
                                )
                            ]),
                            html.Div(children=[
                                html.H2('Mês'),
                                dcc.Dropdown(
                                    id='dropdown_busca_mes',
                                    className='input',
                                    options=[{'label':i, 'value':i} for i in meses],
                                    value=dt_atual.month,
                                    placeholder='Mês',
                                    clearable=False,
                                    searchable=False
                                )
                            ])
                        ]),
                        dt.DataTable(
                            id='dt_serv_dupl_busca',
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'textAlign': 'center'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            style_table={
                                'display': 'flex',
                                'flex-direction': 'column',
                                'align-itens': 'center',
                                'overflowX': 'auto',
                                'minWidth': '50%',
                                'maxWidth': '1000px',
                            },
                            page_size=15
                        )
                    ]
                ),
                html.Div(
                    id='serv_busca',
                    className='sub-plot',
                    children=[
                        html.H1('Busca Individual de Servidores'),
                        html.Div(
                            className='options-container',
                            children=[
                                dcc.Dropdown(
                                    id='serv_busca_input',
                                    className='input',
                                    placeholder='Nome do servidor',
                                    options=[{'label':opt, 'value':opt} for opt in nomes]
                                )
                            ]
                        ),
                        dcc.Graph(
                            id='graph_serv_busca',
                        )
                    ]
                ),
                html.Div(
                    id='serv-liq',
                    className='sub-plot',
                    children=[
                        html.H1('Maior líquido disponível (R$)'),
                        dt.DataTable(
                            id='dt_serv_liq',
                            columns=[{'name': col, 'id': col} for col in pl.serv_liq().columns],
                            data=pl.serv_liq().to_dict('records'),
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'textAlign': 'center'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            style_table={
                                'display': 'flex',
                                'flex-direction': 'column',
                                'align-itens': 'center',
                                'overflowX': 'auto',
                                'minWidth': '50%',
                                'maxWidth': '1000px',
                            },
                            page_size=15
                        )
                    ]
                )
            ]),
        ]),

        html.Footer(className='footer', children=[
            html.P(children=[
                'Fonte: ',
                html.A(href='http://www.transparencia.am.gov.br/pessoal/', children=[
                    'http://www.transparencia.am.gov.br/pessoal/'
                ])
            ])
        ])
    ])

    return component
