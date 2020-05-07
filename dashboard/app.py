import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotting as pl
import layout
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

### DATA ###
df = pd.read_csv('../ds/remuneracao_servidores.csv', sep=',', header=0, decimal='.', parse_dates=['DATA'])

orgaos = pl.orgaos
anos = pl.anos
dt_atual = layout.dt_atual
dt_formatada = layout.dt_formatada

### Layout ###
app.layout = layout.load_layout()

### Calbacks ###
@app.callback(
    Output('graph_org_rem_total_indiv', 'figure'),
    [Input('dropdown2', 'value')]
)
def rem_org(input):
    return pl.org_rem_total_ind(input)

@app.callback(
    Output('graph_aumento','figure'),
    [Input('dropdown_meses_1','value'),
    Input('dropdown_anos_1','value')]
)
def org_aumento(mes, ano):
    if (mes == None or ano == None):
        raise PreventUpdate
    else:
        return pl.org_aumento(mes, ano) 

### Server Run ###
if (__name__ == '__main__'):
    app.run_server(debug=True)