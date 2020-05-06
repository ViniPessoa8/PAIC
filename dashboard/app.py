import dash
import dash_core_components as dcc
import dash_html_components as html
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

### Server Run ###
if (__name__ == '__main__'):
    app.run_server(debug=True)