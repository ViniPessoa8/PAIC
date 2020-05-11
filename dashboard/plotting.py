import pandas as pd
import plotly.express as px

graph_x = 1000
graph_y = 500

pd.set_option('display.float_format', lambda x: '%.2f' % x) # Remove a notação científica dos valores
df = pd.read_csv('../ds/remuneracao_servidores.csv', sep=',', header=0, decimal='.', parse_dates=['DATA']).drop(columns=['Unnamed: 0'])
df = df.sort_values(by=['ORGAO', 'DATA'])

orgaos = df['ORGAO'].unique()
anos = df['DATA'].dt.year.drop_duplicates().sort_values()
meses = df['DATA'].dt.month.drop_duplicates().sort_values()

def org_rem_total():
    df_temp = df.loc[:, ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['ORGAO', 'DATA'], as_index=False).sum()
    df_rem_total = df_temp[df_temp['REMUNERACAO LEGAL TOTAL(R$)'] > 10000000]

    fig = px.line(
        df_rem_total,
        title='Remuneração Legal Total de cada órgão ', 
        x='DATA', y="REMUNERACAO LEGAL TOTAL(R$)", 
        color='ORGAO', 
        width=graph_x, height=graph_y
    )
    fig.update_yaxes(automargin=True)

    return fig


def org_rem_total_ind(input):
    df_org = df.loc[(df.ORGAO == input), ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['DATA'], as_index=False).sum()

    fig = px.line(
        df_org, 
        title='Remuneração Legal Total - '+input,
        x='DATA', y='REMUNERACAO LEGAL TOTAL(R$)',
        width=graph_x, height=graph_y
    )

    return fig

def serv_num_reg():
    df_temp = df.drop_duplicates(['ORGAO', 'NOME'])
    df_temp = df_temp.groupby('ORGAO', as_index=False)['NOME'].count()
    df_temp = df_temp.sort_values('NOME', ascending=False)
    df_temp = df_temp.rename(columns={'NOME':'Funcionários', 'ORGAO':'Órgão'})
    df_temp = df_temp[df_temp['Funcionários'] > 1]

    fig = px.bar(
        df_temp, 
        x='Órgão', y='Funcionários', 
        title='Número de funcionários registrados (Por órgão)', 
        height=700, width=graph_x
    )

    return fig

def serv_num_ativos():
    dt_atual = df['DATA'].max()
    df_temp = df[df['DATA'] == dt_atual]
    df_temp = df_temp.drop_duplicates(['ORGAO', 'NOME'])
    df_temp = df_temp.groupby('ORGAO', as_index=False)['NOME'].count()
    df_temp = df_temp.sort_values('NOME', ascending=False)
    df_temp = df_temp.rename(columns={'NOME':'Funcionários', 'ORGAO':'Órgão'})

    dt_formatada = str(dt_atual.month)+'/'+str(dt_atual.year)

    fig = px.bar(
        df_temp, 
        x='Órgão', y='Funcionários', 
        title='Número de funcionários ativos em '+dt_formatada+' (Por órgão)', 
        height=700, width=graph_x
    )

    return fig


def serv_mais_org():
    df_temp = df.drop_duplicates(['NOME','ORGAO'])
    df_temp = df_temp.groupby('NOME', as_index=False)[['ORGAO']].count()
    df_temp = df_temp[df_temp['ORGAO'] > 1]
    df_temp = df_temp.sort_values(['ORGAO'], ascending=False)
    df_temp.rename(columns={'NOME':'Número de Servidores'})

    return df_temp

def org_aumento(mes, ano):
    # Cálculo do mês anterior
    if mes == 1:
        mes_ant = 12
        ano_ant = ano-1
    else:
        mes_ant = mes-1
        ano_ant = ano

    # Preparação dos dados
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

    num = 50000

    orgs_aum_prin = orgs_aum[(orgs_aum['Remuneração Legal Total (Soma)'] > num) | (orgs_aum['Remuneração Legal Total (Soma)'] < -num)]
    fig_temp = px.bar(orgs_aum_prin, y='Remuneração Legal Total (Soma)', x='Órgão', width=graph_x, height=graph_y)

    return fig_temp

def serv_duplicados(filter):
    # Preparação dos dados
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

def serv_duplicados_busca(org, ano, mes):
    df_temp = df.loc[(df.ORGAO == org) & (df['DATA'].dt.year == ano) & (df['DATA'].dt.month == mes)]
    duplicados = df_temp[df_temp.duplicated(['NOME'], keep=False)].sort_values('NOME')

    return duplicados

def serv_busca(nome):
    registros_serv = df.loc[(df.NOME == nome), :].sort_values('DATA')
    fig = px.line(registros_serv, title='Remuneração de '+nome, y='REMUNERACAO LEGAL TOTAL(R$)', x='DATA', color='ORGAO')

    return fig
