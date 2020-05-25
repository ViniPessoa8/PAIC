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
print('Loading layout...')
app.layout = layout.load_layout(app)

### Calbacks ###
# Mior Remuneração Legal Total
@app.callback(
    Output('graph_rem_leg_total','figure'),
    [Input('slider_rem_leg_total','value')]
)
def rem_leg_total(value):
    return pl.org_rem_total(value[0], value[1])

# Remuneração Total Individual
@app.callback(
    Output('graph_org_rem_total_indiv', 'figure'),
    [Input('dropdown2', 'value')]
)
def rem_org(input):
    return pl.org_rem_total_ind(input)

# Aumento/cortes Remuneração Total
@app.callback(
    Output('graph_org_aumento','figure'),
    [Input('dropdown_meses_1','value'),
    Input('dropdown_anos_1','value'),
    Input('slider_org_aum', 'value')]
)
def org_aumento(mes, ano, valor):
    if (mes == None or ano == None):
        raise PreventUpdate
    else:
        return pl.org_aumento(mes, ano, valor) 

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

# Aumentos/Cortes remuneração servidor
@app.callback(
    Output('graph_serv_aumento_bar','figure'),
    [Input('dropdown_meses_2','value'),
    Input('dropdown_anos_2','value'),
    Input('dropdown_orgao','value')]
)
def serv_aumento(mes, ano, orgao):
    if (mes == None or ano == None):
        raise PreventUpdate
    else:
        return pl.serv_aumento(mes, ano, orgao) 

### Server Run ###
if (__name__ == '__main__'):
    app.run_server(debug=True)