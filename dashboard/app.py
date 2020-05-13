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
df = pl.df

orgaos = pl.orgaos
anos = pl.anos
dt_atual = layout.dt_atual
dt_formatada = layout.dt_formatada

### Layout ###
app.layout = layout.load_layout()

### Calbacks ###
# Remuneração Total Individual
@app.callback(
    Output('graph_org_rem_total_indiv', 'figure'),
    [Input('dropdown2', 'value')]
)
def rem_org(input):
    return pl.org_rem_total_ind(input)

# Aumento/cortes Remuneração Total
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

# Busca servidores duplicados
@app.callback(
    Output('dt_serv_dupl_busca','data'),
    [Input('dropdown_busca_org','value'),
    Input('dropdown_busca_ano','value'),
    Input('dropdown_busca_mes','value')]
)
def serv_busca_duplicados(org, ano, mes):
    return pl.serv_duplicados_busca(org, ano, mes).to_dict('records')

@app.callback(
    Output('dt_serv_dupl_busca','columns'),
    [Input('dropdown_busca_org','value'),
    Input('dropdown_busca_ano','value'),
    Input('dropdown_busca_mes','value')]
)
def serv_busca_duplicados(org, ano, mes):
    return [{'name': col, 'id': col} for col in pl.serv_duplicados_busca(org, ano, mes).columns]

# Busca individual de servidor
@app.callback(
    Output('graph_serv_busca_orgao','figure'),
    [Input('serv_busca_input','value')]
)
def serv_busca(nome):
    if(nome == None):
        raise PreventUpdate
    else:    
        return pl.serv_busca(nome, 'orgao')

@app.callback(
    Output('graph_serv_busca_cargo','figure'),
    [Input('serv_busca_input','value')]
)
def serv_busca(nome):
    if(nome == None):
        raise PreventUpdate
    else:    
        return pl.serv_busca(nome, 'cargo')

### Server Run ###
if (__name__ == '__main__'):
    app.run_server(debug=True)