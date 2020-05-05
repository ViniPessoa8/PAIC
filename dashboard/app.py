import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

### DATA ###
df = pd.read_csv('../ds/remuneracao_servidores.csv', sep=',', header=0, decimal='.', parse_dates=['DATA'])

orgaos = df.sort_values(['ORGAO'], ascending=True)['ORGAO'].unique()
anos = df['DATA'].dt.year.drop_duplicates().sort_values()

print(anos)

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

    html.Div(className='plot-container', children=[
        html.Div(className='plot-1 plot', children=[
            html.H3(id='out', children=['plot 1']),
            dcc.Dropdown(
                id='dropdown1',
                className='input',
                options=[{'label':i, 'value':i} for i in orgaos],
                value='-',
                placeholder='Selecione um Órgão',
                clearable=False,
                searchable=False
            ),
            dcc.Graph(
                id='graph'
            )
        ]),

        html.Div(className='plot-2 plot', children=[
            html.H3('plot 2')
        ])
    ])
])

### Calbacks ###
@app.callback(
    Output('out', 'children'),
    [Input('dropdown1', 'value')]
)
def update_org_name(input):
    print(input)
    return input 

if (__name__ == '__main__'):
    app.run_server(debug=True)