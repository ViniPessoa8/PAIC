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

    html.Div(className='plot-container', children=[

        html.Div(className='plot-1 plot', children=[
            html.H2('Maior Remuneração Legal Total (R$)'),
            dcc.Graph(
                id='graph',
                className='graph',
                figure=fig,
            )
        ]),

        html.Div(className='plot-2 plot', children=[
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
                id='graph2',
                className='graph'
            )
        ])
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
    Output('graph2', 'figure'),
    [Input('dropdown2', 'value')]
)
def rem_org(input):
    df_org = df.loc[(df.ORGAO == input), ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['DATA'], as_index=False).sum()

    fig2 = px.line(df_org, title='Remuneração Legal Total - '+input, x='DATA', y='REMUNERACAO LEGAL TOTAL(R$)', width=1000, height=500)
    return fig2

### Server Run ###
if (__name__ == '__main__'):
    app.run_server(debug=True)