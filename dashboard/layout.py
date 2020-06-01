import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import plotting as pl
import pandas as pd
import pathlib
import math
# import json

uea_logo = str(pl.dash_path) + '/assets/UEA-EST.png'
print('Dataset path:', pl.ds_path)

df = pl.df

nomes = pl.nomes
orgaos = pl.orgaos
anos = pl.anos
meses = pl.meses
dt_atual = df['DATA'].max()
dt_formatada = str(dt_atual.month)+'/'+str(dt_atual.year)
max_sal = df['REMUNERACAO LEGAL TOTAL(R$)'].max()

df_teste = df[df['DATA'] == dt_atual][['NOME', 'ORGAO']].head(10)

def load_layout(app):    
    component = html.Div(className='container', children=[
        html.Div(id='datalist-container', className='datalist-container'),
        html.Div(className='header-container', children=[
            html.H1(className='header', children=[
                'Transparência do Governo do Amazonas'
            ]),
            html.H3(className='info', children=[
                'Portal de análise dos dados referentes à remuneração dos servidores públicos do governo  do Amazonas.'
            ]),
            html.P(children=[
                'Fonte: ',
                html.A(href='http://www.transparencia.am.gov.br/pessoal/', children=[
                    'http://www.transparencia.am.gov.br/pessoal/'
                ])
            ]),
        ]),
        html.Div(className='main-container', children =[
            html.Div(className='sidenav', children=[
                html.Div(className='summary', children=[
                    html.A(className='sum-header', href='#orgaos', children=['Órgãos']),
                    html.A(className='', href='#org-rem-leg-total', children=['Remuneração Legal Total (Maior)']),
                    html.A(className='', href='#org-rem-leg-indiv', children=['Remuneração Legal Total (Individual)']),
                    html.A(className='', href='#org-aum-corte', children=['Aumentos e Cortes']),
                    html.A(className='sum-header', href='#servidores', children=['Servidores']),
                    html.A(className='', href='#serv-busca', children=['Busca']),
                    html.A(className='', href='#serv-reg', children=['Quantidade por órgão']),
                    html.A(className='', href='#serv-mais-org', children=['Presentes em mais de um órgão']),
                    html.A(className='', href='#serv-dupl-mesmo-org', children=['Duplicados no mesmo órgão']),
                    html.A(className='', href='#serv-liq', children=['Maior Líquido']),
                    html.A(className='', href='#serv-aum-corte', children=['Aumentos e Cortes'])
                ])
            ]),
            html.Div(className='plot-container', children=[
                html.Div(id='orgaos', className='plot-container section', children=[
                    html.Div(className='plot-header', children=[
                        html.H3('Órgãos')
                    ]),
                    html.Div(id='org-rem-leg-total', className='sub-plot  section', children=[
                        html.H1('Maior Remuneração Legal Total (R$)'),
                        html.H2('Soma da Remuneração Legal Total de cada órgão por mês.'),
                        dcc.RangeSlider(
                            id         = 'slider_rem_leg_total',
                            className  = 'slider',
                            min        = 0,
                            max        = 140000000,
                            step       = None,
                            allowCross = False,
                            value      = [10000000, 140000000],
                            marks      = {0:'0', 500000:'500K', 1000000:'1M', 10000000:'10M', 50000000:'50M', 100000000:'100M', 140000000:'140M'}
                        ),
                        dcc.Graph(
                            id='graph_rem_leg_total',
                        )
                    ]),
                    html.Div(id='org-rem-leg-indiv', className='sub-plot  section', children=[
                        html.H1('Remuneração Legal Total Individual (R$)'),
                        html.H2('Soma da Remuneração Legal Total por órgão.'),
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
                    html.Div(id='org-aum-corte', className='sub-plot section', children=[
                        html.H1('Aumento/Corte no orçamento'),
                        html.H3(id='org_aum_corte_H3'),
                        html.Div(className='options-container', children=[
                            html.Div(children=[
                                html.H3('Mês'),
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
                                html.H3('Ano'),
                                dcc.Dropdown(
                                    id='dropdown_anos_1',
                                    className='input',
                                    options=[{'label':i, 'value':i} for i in anos],
                                    value=dt_atual.year,
                                    placeholder='Ano',
                                    clearable=False,
                                    searchable=False
                                )
                            ]),
                        ]),
                        html.Div(children=[
                            html.H3('Valor mínimo'),
                            dcc.Slider(
                                id         = 'slider_org_aum',
                                className  = 'slider-2',
                                min        = 0,
                                max        = 1000000,
                                step       = None,
                                value      = 100000,
                                marks      = {0:'0', 10000:'10K', 100000:'100K', 500000:'500K', 1000000:'1M', 10000000:'10M'}
                            ),
                        ]),
                        dcc.Graph(
                            id='graph_org_aumento',
                        )
                    ])
                ]),
                html.Div(id='servidores', className='plot-container section', children=[
                    html.Div(className='plot-header', children=[
                        html.H3(className='', children=[
                            'Servidores'
                        ])
                    ]),
                    html.Div(
                        id='serv-busca',
                        className='sub-plot section',
                        children=[
                            html.H1('Busca Individual de Servidores'),
                            html.Div(
                                className='options-container',
                                children=[
                                    dcc.Input(
                                        id='serv_busca_input',
                                        className='input_name',
                                        type='search',
                                        debounce=True,
                                        placeholder='Nome do servidor',
                                        list=str(pl.nomes),
                                        value='FRANCISCO DAS CHAGAS DA SILVA',
                                    ),
                                    html.Button('Pesquisar', id='serv-submit-btn')
                                ]
                            ),
                            html.H1('Por órgão'),
                            dcc.Graph(
                                id='graph_serv_busca_orgao',
                            ),
                            html.H1('Por cargo'),
                            dcc.Graph(
                                id='graph_serv_busca_cargo'
                            ),
                            html.H1('Por função'),
                            dcc.Graph(
                                id='graph_serv_busca_funcao'
                            )
                        ]
                    ),
                    html.Div(
                        id='serv-reg',
                        className='sub-plot section',
                        children=[
                            html.H1('Numero de Funcionários'),
                            html.H1(children=[
                                'Registrados (', anos.min(), ' - ', anos.max(), ')'
                            ]),
                            dcc.Graph(
                                id='graph_serv_num_reg',
                                figure=pl.serv_num_reg()
                            ),
                            html.H1(children=[
                                'Ativos (', dt_formatada, ')'
                            ]),
                            dcc.Graph(
                                id='graph_serv_num_ativo',
                                figure=pl.serv_num_ativos()
                            )
                        ]
                    ),
                    html.Div(
                        id='serv-mais-org',
                        className='sub-plot section',
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
                        className='sub-plot section',
                        children=[
                            html.H1('Servidores duplicados no mesmo órgão.'),
                            html.Div(
                                className='serv_dupl_container',
                                children=[
                                    html.Div(className='dt-container', children=[
                                        html.H1('Por órgão'),
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
                                        html.H1('Por ano'),
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
                            html.H1('Busca de servidores duplicados'),
                            html.Div(className='options-container', children=[
                                html.Div(children=[
                                    html.H1('Órgão'),
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
                                    html.H1('Ano'),
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
                                    html.H1('Mês'),
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
                        id='serv-liq',
                        className='sub-plot section',
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
                    ),
                    html.Div(id='serv-aum-corte', className='sub-plot section', children=[
                        html.H1('Aumento/Corte no orçamento'),
                        html.H3(id='serv_aum_corte_H3'),
                        html.Div(className='options-container', children=[
                            html.Div(children=[
                                html.H3('Mês'),
                                dcc.Dropdown(
                                    id='dropdown_meses_2',
                                    className='input',
                                    options=[{'label':i, 'value':i} for i in meses],
                                    value=dt_atual.month,
                                    placeholder='Mês',
                                    clearable=False,
                                    searchable=False
                                ),
                            ]),
                            html.Div(children=[
                                html.H3('Ano'),
                                dcc.Dropdown(
                                    id='dropdown_anos_2',
                                    className='input',
                                    options=[{'label':i, 'value':i} for i in anos],
                                    value=dt_atual.year,
                                    placeholder='Ano',
                                    clearable=False,
                                    searchable=False
                                )
                            ]),
                            html.Div(children=[
                                html.H3('Órgão'),
                                dcc.Dropdown(
                                    id='dropdown_orgao',
                                    className='input',
                                    options=[{'label':i, 'value':i} for i in orgaos],
                                    value=orgaos[0],
                                    placeholder='Órgão',
                                    clearable=False,
                                    searchable=False
                                )
                            ])
                        ]),
                        html.Div(children=[
                            html.H3('Valor mínimo'),
                            dcc.Slider(
                                id         = 'slider_serv_aum',
                                className  = 'slider-2',
                                min        = 0,
                                max        = 500000,
                                step       = None,
                                value      = 0,
                                marks      = {0:'0', 10000:'10K', 50000:'50K', 100000:'100K', 500000:'500K'}
                            ),
                        ]),
                        dcc.Graph(
                            id='graph_serv_aumento_bar',
                        )
                    ])
                ])
            ])
        ]),
        html.Footer(className='footer', children=[
            html.Div(className='footer-image-container', children=[
                html.Img(src=app.get_asset_url('media/UEA-EST.png')),
                html.Img(src=app.get_asset_url('media/LSI.jpg')),
            ])
        ])
    ])

    return component
