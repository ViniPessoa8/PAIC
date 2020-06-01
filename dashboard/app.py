import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotting as pl
import layout
import util
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

### ÓRGÃOS

# Mior Remuneração Legal Total
@app.callback(
    Output('graph_rem_leg_total','figure'),
    [Input('slider_rem_leg_total','value')]
)
def rem_leg_total(value):
    response = pl.org_rem_total(value[0], value[1])
    if (response != None ):
        return response
    else:
        print('Erro: Entrada inválida.')

# Remuneração Total Individual
@app.callback(
    Output('graph_org_rem_total_indiv', 'figure'),
    [Input('dropdown2', 'value')]
)
def rem_org(input):
    response = pl.org_rem_total_ind(input) 
    if (response != None ):
        return response
    else:
        print('Erro: Entrada inválida.')

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
        response = pl.org_aumento(mes, ano, valor)
        if (response != None ):
            return response   
        else:
            print('Erro: Entrada inválida.')

@app.callback(
    Output('org_aum_corte_H3','children'),
    [Input('slider_org_aum', 'value')]
)
def org_aumento(valor):
    str_out = 'Diferença da soma da remuneração legal total de um mês para o outro. Sendo a diferença maior ou menor que '+util.format_number(valor)+'.'
    return str_out 

### SERVIDORES

# Busca servidores duplicados
@app.callback(
    Output('dt_serv_dupl_busca','data'),
    [Input('dropdown_busca_org','value'),
    Input('dropdown_busca_ano','value'),
    Input('dropdown_busca_mes','value')]
)
def serv_busca_duplicados(org, ano, mes):
    response = pl.serv_duplicados_busca(org, ano, mes).to_dict('records') 
    if (response != None ):
        return response
    else:
        print('Erro: Entrada inválida.')

@app.callback(
    Output('dt_serv_dupl_busca','columns'),
    [Input('dropdown_busca_org','value'),
    Input('dropdown_busca_ano','value'),
    Input('dropdown_busca_mes','value')]
)
def serv_busca_duplicados(org, ano, mes):
    response = pl.serv_duplicados_busca(org, ano, mes).columns
    if (response.any()):
        return [{'name': col, 'id': col} for col in response]
    else:
        print('Erro: Entrada inválida.')

# Busca individual de servidor
## Por órgão
@app.callback(
    Output('graph_serv_busca_orgao','figure'),
    [Input('serv_busca_input','value')]
)
def serv_busca(nome):
    
    if((nome == None) or (nome not in pl.nomes.values)):
        raise PreventUpdate
    else:    
        response = pl.serv_busca(nome, 'orgao')
        if(response != None ):
            return response
        else:
            print('Erro: Entrada inválida.')
            
## Por cargo 
@app.callback(
    Output('graph_serv_busca_cargo','figure'),
    [Input('serv_busca_input','value')]
)
def serv_busca(nome):
    if((nome == None) or (nome not in pl.nomes.values)):
        raise PreventUpdate
    else:
        response = pl.serv_busca(nome, 'cargo')
        if (response != None ):
            return response
        else:
            print('Erro: Entrada inválida.')

## Por Funcao
@app.callback(
    Output('graph_serv_busca_funcao','figure'),
    [Input('serv_busca_input','value')]
)
def serv_busca(nome):
    if((nome == None) or (nome not in pl.nomes.values)):
        raise PreventUpdate
    else:
        response = pl.serv_busca(nome, 'funcao')
        if (response != None ):
            return response
        else:
            print('Erro: Entrada inválida.')


# Aumentos/Cortes remuneração servidor
@app.callback(
    Output('graph_serv_aumento_bar','figure'),
    [Input('dropdown_meses_2','value'),
    Input('dropdown_anos_2','value'),
    Input('dropdown_orgao','value'),
    Input('slider_serv_aum','value')]
)
def serv_aumento(mes, ano, orgao, valor):
    if (mes == None or ano == None):
        raise PreventUpdate
    else:
        response = pl.serv_aumento(mes, ano, orgao, valor)  
        if (response != None ):
            return response
        else:
            print('Erro: Entrada inválida.')

@app.callback(
    Output('serv_aum_corte_H3','children'),
    [Input('slider_serv_aum', 'value')]
)
def org_aumento(valor):
    str_out = 'Diferença da soma da remuneração legal total de um mês para o outro. Sendo a diferença maior ou menor que '+util.format_number(valor)+'.'
    return str_out 

### Server Run ###
if (__name__ == '__main__'):
    app.run_server(debug=True)