import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pathlib 
import os

# Configurações do Gráfico
graph_x = 1000
graph_y = 500

# Preparação dos Dados 
dash_path = pathlib.Path(__file__).parent.absolute()
project_path = dash_path.parent.absolute()
ds_path = str(project_path) + '/ds/remuneracao_servidores.csv'

pd.set_option('display.float_format', lambda x: '%.2f' % x) # Remove a notação científica dos valores
df = pd.read_csv(ds_path, sep=',', header=0, decimal='.', parse_dates=['DATA']).drop(columns=['Unnamed: 0'])
df = df.sort_values(by=['ORGAO', 'DATA'])

orgaos = df['ORGAO'].unique()
anos   = df['DATA'].dt.year.drop_duplicates().sort_values()
meses  = df['DATA'].dt.month.drop_duplicates().sort_values()
nomes  = df['NOME'].drop_duplicates()

# Métodos
## ÓRGÃO
### Soma da remuneração legal total por órgão
def org_rem_total(init, end):
    # Preparação dos Dados 
    df_temp = df.loc[:, ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['ORGAO', 'DATA'], as_index=False).sum()
    rem = df_temp['REMUNERACAO LEGAL TOTAL(R$)']
    df_rem_total = df_temp.loc[(rem > init) & (rem < end)]

    # Plot
    layout = go.Layout(width=graph_x, height=graph_y)
    fig = go.Figure(layout=layout)
    fig.update_layout(title='Remuneração Legal Total de cada órgão ')
    for orgao in df_rem_total['ORGAO'].drop_duplicates():
        df_temp = df_rem_total.loc[(df_rem_total['ORGAO'] == orgao)] 
        fig.add_trace(go.Scatter(
            x=df_temp['DATA'], 
            y=df_temp['REMUNERACAO LEGAL TOTAL(R$)'],
            mode='lines+markers',
            name=orgao
        ))
    fig.update_yaxes(automargin=True)

    return fig

### Soma da remuneração legal total individual de um órgão, por mês.
def org_rem_total_ind(orgao):
    # Preparação dos Dados 
    df_org = df.loc[(df.ORGAO == orgao), ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['DATA'], as_index=False).sum()

    # Plot
    layout = go.Layout(width=graph_x, height=graph_y)
    fig = go.Figure(layout=layout)
    fig.update_layout(title='Remuneração Legal Total - '+orgao)
    fig.add_trace(go.Scatter(
        x=df_org['DATA'], 
        y=df_org['REMUNERACAO LEGAL TOTAL(R$)'],
        mode='lines+markers',
        name=orgao
    ))

    return fig

### Orgãos com o maior aumento/corte de um mês para o outro
def org_aumento(mes, ano, valor):
    # Preparação dos Dados 
    # Cálculo do mês anterior
    if mes == 1:
        mes_ant = 12
        ano_ant = ano-1
    else:
        mes_ant = mes-1
        ano_ant = ano

    df_mes_atual    = df.loc[(df['DATA'].dt.month == mes) & (df['DATA'].dt.year == ano)]
    df_mes_atual    = df_mes_atual.groupby(['ORGAO', 'DATA'], as_index=False)['REMUNERACAO LEGAL TOTAL(R$)'].sum()
    df_mes_anterior = df.loc[(df['DATA'].dt.month == mes_ant) & (df['DATA'].dt.year == ano_ant)]
    df_mes_anterior = df_mes_anterior.groupby(['ORGAO', 'DATA'], as_index=False)['REMUNERACAO LEGAL TOTAL(R$)'].sum()

    rem_atual       = df_mes_atual[['ORGAO', 'REMUNERACAO LEGAL TOTAL(R$)', 'DATA']]
    rem_anterior    = df_mes_anterior[['ORGAO', 'REMUNERACAO LEGAL TOTAL(R$)', 'DATA']]

    inner_join      = pd.merge(rem_anterior, rem_atual, how='inner', on='ORGAO', suffixes=(' ANTERIOR', ' ATUAL'))

    diff            = inner_join['REMUNERACAO LEGAL TOTAL(R$) ATUAL'] - inner_join['REMUNERACAO LEGAL TOTAL(R$) ANTERIOR']
    diff            = diff.sort_values(ascending=False)

    orgs_aum     = pd.DataFrame()
    orgs_aum['Órgão'] = rem_atual['ORGAO']
    orgs_aum['Remuneração Legal Total (Soma)'] = diff
    orgs_aum = orgs_aum.sort_values('Remuneração Legal Total (Soma)', ascending=False)

    orgs_aum_prin   = orgs_aum[(orgs_aum['Remuneração Legal Total (Soma)'] > valor)]
    orgs_corte_prin = orgs_aum[(orgs_aum['Remuneração Legal Total (Soma)'] < -valor)]
    
    # Plot
    fig = make_subplots(
        y_title = 'Remuneração Legal Total (R$)'
    )
    fig.add_trace(
        go.Bar(
            name = 'Aumentos',
            y    = orgs_aum_prin['Remuneração Legal Total (Soma)'], 
            x    = orgs_aum_prin['Órgão'],
            base = 0
        )
    )
    fig.add_trace(
        go.Bar(
            name = 'Cortes',
            y    = orgs_corte_prin['Remuneração Legal Total (Soma)'], 
            x    = orgs_corte_prin['Órgão'],
            base = 0
        )
    )
    fig.update_layout(
        title_text = 'Servidores com o maior aumento/corte',
        title_font_size = 17,
        width = graph_x,
        height = graph_y
    )

    return fig

## SERVIDORES
### Busca de servidores
def serv_busca(nome, filter='orgao'):
    # Preparação dos Dados 
    df_bool = (df['NOME'] == nome)
    registros_serv = df.loc[df_bool].sort_values('DATA')
    layout = go.Layout(width=graph_x, height=graph_y)

    # Plot
    if (filter == 'orgao'):
        fig = go.Figure(layout=layout)
        fig.update_layout(title='Remuneração Legal Total de '+nome+' por Cargo e Data')
        for orgao in registros_serv['ORGAO'].drop_duplicates():
            df_temp = registros_serv.loc[(registros_serv['ORGAO'] == orgao)] 
            fig.add_trace(go.Scatter(
                x=df_temp['DATA'], 
                y=df_temp['REMUNERACAO LEGAL TOTAL(R$)'],
                mode='lines+markers',
                name=orgao
            ))
    elif (filter == 'cargo'):
        fig = go.Figure(
            layout=layout,
        )
        fig.update_layout(title='Remuneração Legal Total de '+nome+' por Cargo e Data')
        for cargo in registros_serv['CARGO'].drop_duplicates():
            df_temp = registros_serv.loc[(registros_serv['CARGO'] == cargo)] 
            fig.add_trace(go.Scatter(
                x=df_temp['DATA'], 
                y=df_temp['REMUNERACAO LEGAL TOTAL(R$)'],
                mode='lines+markers',
                name=cargo
            ))
    else:
        fig = go.Figure(layout=layout)
        fig.update_layout(
            title='Remuneração Legal Total de '+nome+' por Cargo e Data'
            )
        for funcao in registros_serv['FUNCAO'].drop_duplicates():
            title='Remuneração Legal Total de '+nome+' por Função e Data', 
            df_temp = registros_serv.loc[(registros_serv['FUNCAO'] == funcao)] 
            fig.add_trace(go.Scatter(
                x=df_temp['DATA'], 
                y=df_temp['REMUNERACAO LEGAL TOTAL(R$)'],
                mode='lines+markers',
                name=funcao
            ))

    return fig

### Órgãos com mais servidores registrados
def serv_num_reg():
    # Preparação dos Dados 
    df_temp = df.drop_duplicates(['ORGAO', 'NOME'])
    df_temp = df_temp.groupby('ORGAO', as_index=False)['NOME'].count()
    df_temp = df_temp.sort_values('NOME', ascending=False)
    df_temp = df_temp.rename(columns={'NOME':'Funcionários', 'ORGAO':'Órgão'})
    df_temp = df_temp[df_temp['Funcionários'] > 1]

    # Plot
    fig = px.bar(
        df_temp, 
        x='Órgão', y='Funcionários', 
        title='Número de funcionários registrados (Por órgão)', 
        height=700, width=graph_x
    )

    return fig

### Número de servidores ativos por órgão
def serv_num_ativos():
    # Preparação dos Dados 
    dt_atual = df['DATA'].max()
    df_temp = df[df['DATA'] == dt_atual]
    df_temp = df_temp.drop_duplicates(['ORGAO', 'NOME'])
    df_temp = df_temp.groupby('ORGAO', as_index=False)['NOME'].count()
    df_temp = df_temp.sort_values('NOME', ascending=False)
    df_temp = df_temp.rename(columns={'NOME':'Funcionários', 'ORGAO':'Órgão'})

    dt_formatada = str(dt_atual.month)+'/'+str(dt_atual.year)

    # Plot 
    fig = px.bar(
        df_temp, 
        x='Órgão', y='Funcionários', 
        title='Número de funcionários ativos em '+dt_formatada+' (Por órgão)', 
        height=700, width=graph_x
    )

    return fig

## Servidores com mais órgãos diferentes
def serv_mais_org():
    # Preparação dos Dados 
    df_temp = df.drop_duplicates(['NOME','ORGAO'])
    df_temp = df_temp.groupby('NOME', as_index=False)[['ORGAO']].count()
    df_temp = df_temp[df_temp['ORGAO'] > 1]
    df_temp = df_temp.sort_values(['ORGAO'], ascending=False)
    df_temp.rename(columns={'NOME':'Número de Servidores'})

    return df_temp

### Servidores duplicados
def serv_duplicados(filter):
    # Preparação dos Dados 
    df_temp    = df[['NOME', 'DATA', 'ORGAO']]
    df_bool    = df_temp.duplicated()
    duplicados = df_temp[df_bool]
    duplicados = duplicados.rename(columns={'NOME':'Número de Servidores'})

    if (filter == 'data'):
        duplicados_data  = duplicados.groupby(duplicados['DATA'].dt.year)['Número de Servidores'].count()
        
        return duplicados_data

    duplicados_orgao = duplicados.groupby(['ORGAO'], as_index=False)['Número de Servidores'].count()
    duplicados_orgao = duplicados_orgao.sort_values('Número de Servidores', ascending=False)

    return duplicados_orgao

### Busca de servidores duplicados
def serv_duplicados_busca(org, ano, mes):
    # Preparação dos Dados 
    df_temp = df.loc[(df.ORGAO == org) & (df['DATA'].dt.year == ano) & (df['DATA'].dt.month == mes)]
    duplicados = df_temp[df_temp.duplicated(['NOME'], keep=False)].sort_values('NOME')
    duplicados = duplicados.drop(columns=['DATA', 'ORGAO'])

    return duplicados

### Servidores com maior líquido disponível
def serv_liq():
    # Preparação dos Dados 
    df_temp = df.loc[(df['LIQUIDO DISPONIVEL(R$)'] > 35000)]
    df_out  = pd.DataFrame()

    df_out['Nome']  = df_temp['NOME']
    df_out['Líquido Disponível(R$)'] = df_temp['LIQUIDO DISPONIVEL(R$)']
    df_out['Órgão'] = df_temp['ORGAO']
    df_out['Data']  = df_temp['DATA'].dt.date

    df_out = df_out.sort_values(by='Líquido Disponível(R$)', ascending=False)

    return df_out

### Servidores com o maior aumento/corte
def serv_aumento(mes, ano, orgao, valor):
    # Cálculo do mês anterior
    if mes == 1:
        mes_ant = 12
        ano_ant = ano-1
    else:
        mes_ant = mes-1
        ano_ant = ano

    # Preparação dos dados
    df_mes_atual    = df.loc[(df['DATA'].dt.month == mes) & (df['DATA'].dt.year == ano) & (df['ORGAO'] == orgao)]
    df_mes_atual    = df_mes_atual.groupby(['NOME', 'DATA', 'ORGAO'], as_index=False)['REMUNERACAO LEGAL TOTAL(R$)'].sum()
    df_mes_anterior = df.loc[(df['DATA'].dt.month == mes_ant) & (df['DATA'].dt.year == ano_ant) & (df['ORGAO'] == orgao)]
    df_mes_anterior = df_mes_anterior.groupby(['NOME', 'DATA', 'ORGAO'], as_index=False)['REMUNERACAO LEGAL TOTAL(R$)'].sum()

    rem_atual       = df_mes_atual[['NOME', 'REMUNERACAO LEGAL TOTAL(R$)', 'ORGAO', 'DATA']]
    rem_anterior    = df_mes_anterior[['NOME', 'REMUNERACAO LEGAL TOTAL(R$)', 'ORGAO', 'DATA']]

    inner_join      = pd.merge(rem_anterior, rem_atual, how='inner', on='NOME', suffixes=(' ANTERIOR', ' ATUAL'))

    diff            = inner_join['REMUNERACAO LEGAL TOTAL(R$) ATUAL'] - inner_join['REMUNERACAO LEGAL TOTAL(R$) ANTERIOR']
    diff            = diff.sort_values(ascending=False)

    orgs_aum = pd.DataFrame()
    orgs_aum['Nome'] = rem_atual['NOME']
    orgs_aum['Remuneração Legal Total (Soma)'] = diff
    orgs_aum = orgs_aum.sort_values('Remuneração Legal Total (Soma)', ascending=False)

    orgs_aum_prin   = orgs_aum[(orgs_aum['Remuneração Legal Total (Soma)'] > valor)]
    orgs_corte_prin = orgs_aum[(orgs_aum['Remuneração Legal Total (Soma)'] < -valor)]

    # Plot
    fig = make_subplots(
        y_title = 'Remuneração Legal Total (R$)'
    )
    fig.add_trace(
        go.Bar(
            name = 'Aumentos',
            y    = orgs_aum_prin['Remuneração Legal Total (Soma)'], 
            x    = orgs_aum_prin['Nome'],
            base = 0
        )
    )
    fig.add_trace(
        go.Bar(
            name = 'Cortes',
            y    = orgs_corte_prin['Remuneração Legal Total (Soma)'], 
            x    = orgs_corte_prin['Nome'],
            base = 0
        )
    )
    fig.update_layout(
        title_text = 'Servidores com o maior aumento/corte',
        title_font_size = 17,
        width = graph_x,
        height = graph_y
    )

    return fig