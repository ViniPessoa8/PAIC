import pandas as pd
import plotly.express as px

df = pd.read_csv('../ds/remuneracao_servidores.csv', sep=',', header=0, decimal='.', parse_dates=['DATA'])

orgaos = df.sort_values(['ORGAO'], ascending=True)['ORGAO'].unique()
anos = df['DATA'].dt.year.drop_duplicates().sort_values()

def org_rem_total():
    df_temp = df.loc[:, ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['ORGAO', 'DATA'], as_index=False).sum()
    df_rem_total = df_temp[df_temp['REMUNERACAO LEGAL TOTAL(R$)'] > 10000000]

    fig = px.line(
        df_rem_total,
        title='Remuneração Legal Total de cada órgão ', 
        x='DATA', y="REMUNERACAO LEGAL TOTAL(R$)", 
        color='ORGAO', 
        width=900, height=500
    )
    fig.update_yaxes(automargin=True)

    return fig


def org_rem_total_ind(input):
    df_org = df.loc[(df.ORGAO == input), ['REMUNERACAO LEGAL TOTAL(R$)', 'DATA', 'ORGAO']].groupby(by=['DATA'], as_index=False).sum()

    fig = px.line(
        df_org, 
        title='Remuneração Legal Total - '+input,
        x='DATA', y='REMUNERACAO LEGAL TOTAL(R$)',
        width=1000, height=500
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
        height=700, width=1100
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
        height=700, width=1000
    )

    return fig