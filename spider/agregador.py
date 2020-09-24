import pandas as pd
import os
import re
import gc
import csv
import sys

csv.field_size_limit(sys.maxsize)

def lista_dirs(path):
    dirs=[]
    # r = raiz, d = diretorios, f = arquivos
    for r, d, f in os.walk(path):
        for direc in d:
            if '.txt' not in direc:
                dirs.append(os.path.join(r, direc))
    return dirs

def lista_arqs(path):
    files = []
    # r = raiz, d = diretorios, f = arquivos
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                f_out = os.path.join(r, file)
                files.append(f_out)
    return files

def cria_df_orgao(path):
    skip_13 = True # Pular o mês 13 (décimo terceiro salário)
    
    files = lista_arqs(path)
    df_orgao = pd.DataFrame()
    for f in files:
        if '.csv' in f:
            if f.endswith("13.csv"):
                continue
            df_mes = pd.read_csv(f, sep=';', header=0, decimal=',', engine='python',error_bad_lines=False)
            
            file_name = f.split("_")[1]
            orgao_name = path.split("/")[2]
            
            mes = file_name[4:6]
            ano = file_name[0:4]
            
            if skip_13 and mes == '13':
                continue
            else:
                data_string = ano+'-'+mes+'-01'
                df_mes["DATA"] = pd.to_datetime(data_string)

                df_orgao = pd.concat([df_orgao, df_mes], ignore_index=True)
                df_orgao["ORGAO"] = orgao_name
    try:
        df_orgao.drop(['Unnamed: 10'], axis=1, inplace=True)
    except:
        print('')
    return df_orgao

def cria_df_geral(path):
    df_geral = pd.DataFrame()
    dirs = lista_dirs(path)
    for d in dirs:
        if (str(d) == "../csv/PRODAM"):
            continue
        print("Processando diretório:", str(d))
        nome_dir = d.split("/")[1]
        df_orgao = cria_df_orgao(d)
        df_geral = pd.concat([df_geral,df_orgao], ignore_index=True)
        df_geral = trata_nan(df_geral)
    return df_geral

def trata_nan(df):
    for col in df.columns:
        if(df[col].dtype == 'object'):
            df[col] = df[col].fillna('-')
        if(df[col].dtype == 'float64'):
            df[col] = df[col].fillna(0.00)
    
    return df

def salva_df(df):
    path = r'../ds/'
    if (not os.path.exists(path)):
        os.mkdir(path)
    df.to_csv(path + r'remuneracao_servidores.csv')

def main():
    path = '../csv/'
    gc.enable()
    df_geral = cria_df_geral(path)
    salva_df(df_geral)

main()