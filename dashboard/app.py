import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

### DATA ###
df = pd.read_csv('../ds/remuneracao_servidores.csv', sep=',', header=0, decimal='.', parse_dates=['DATA'])

orgaos = df.sort_values(['ORGAO'], ascending=True)['ORGAO'].unique()
anos = df['DATA'].dt.year.drop_duplicates().sort_values()

df_temp = df.loc[:, ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['ORGAO', 'DATA'], as_index=False).sum()
df_rem_total = df_temp[df_temp['REMUNERACAO LEGAL TOTAL(R$)'] > 10000000]
fig = px.line(df_rem_total, title='Remuneração Legal Total de cada órgão ', x='DATA', y="REMUNERACAO LEGAL TOTAL(R$)", color='ORGAO', width=900, height=500)
fig.update_yaxes(automargin=True)

### Numero de Funcionarios
## Registrados

df_temp = df.drop_duplicates(['ORGAO', 'NOME'])
df_temp = df_temp.groupby('ORGAO', as_index=False)['NOME'].count()
df_temp = df_temp.sort_values('NOME', ascending=False)
df_temp = df_temp.rename(columns={'NOME':'Funcionários', 'ORGAO':'Órgão'})

fig_num_func_reg = px.bar(df_temp, x='Órgão', y='Funcionários', title='Número de funcionários registrados (Por órgão)', height=700, width=1000)
fig_num_func_reg.update_yaxes(nticks=10) 

## Ativos
dt_atual = df['DATA'].max()
df_temp = df[df['DATA'] == dt_atual]
df_temp = df_temp.drop_duplicates(['ORGAO', 'NOME'])
df_temp = df_temp.groupby('ORGAO', as_index=False)['NOME'].count()
df_temp = df_temp.sort_values('NOME', ascending=False)
df_temp = df_temp.rename(columns={'NOME':'Funcionários', 'ORGAO':'Órgão'})

dt_formatada = str(dt_atual.month)+'/'+str(dt_atual.year)

fig_num_func_ativo = px.bar(df_temp, x='Órgão', y='Funcionários', title='Número de funcionários ativos em '+dt_formatada+' (Por órgão)', height=700, width=1000)

### Layout ###
app.layout = html.Div(className='main-container', children=[
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
            dcc.Graph(
                id='graph',
                className='graph',
                figure=fig,
            )
        ]),

        html.Div(className='plot', children=[
            html.H2('Remuneração Legal Total Individual (R$)'),
            dcc.Dropdown(
                id='dropdown2',
                className='input',
                options=[{'label':i, 'value':i} for i in orgaos],
                value=orgaos[0],
                placeholder='Selecione um Órgão',
                clearable=False,
                searchable=False
            ),
            dcc.Graph(
                id='graph_org_rem_total_indiv',
                className='graph',
                figure=fig_num_func_reg
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
            html.H1('Numero de Funcionarios'),
            html.Div(
                id='registrados-container',
                className='plot',
                children=[
                    html.H2(children=[
                        'Registrados (', anos.min(), ' - ', anos.max(), ')'
                    ]),
                    dcc.Graph(
                        id='graph_serv_num_reg',
                        className='graph',
                        figure=fig_num_func_reg
                    ),
                ]
            ),
            html.Div(
                id='ativos-container',
                className='plot',
                children=[
                    html.H2(children=[
                        'Ativos (', dt_formatada, ')'
                    ]),
                    dcc.Graph(
                        id='graph_serv_num_ativo',
                        className='graph',
                        figure=fig_num_func_ativo
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

### Calbacks ###
@app.callback(
    Output('graph_org_rem_total_indiv', 'figure'),
    [Input('dropdown2', 'value')]
)
def rem_org(input):
    df_org = df.loc[(df.ORGAO == input), ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['DATA'], as_index=False).sum()

    fig2 = px.line(df_org, title='Remuneração Legal Total - '+input, x='DATA', y='REMUNERACAO LEGAL TOTAL(R$)', width=1000, height=500)
    return fig2

### Server Run ###
if (__name__ == '__main__'):
    app.run_server(debug=True)