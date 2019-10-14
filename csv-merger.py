#!/usr/bin/env python
# coding: utf-8

# In[183]:


import pandas as pd
import os
import re

def list_dirs(path):
    dirs=[]
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for direc in d:
            print(direc)
            if '.txt' not in direc:
                dirs.append(os.path.join(r, direc))
    return dirs


def list_files(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                f_out = os.path.join(r, file)
                files.append(f_out)
    return files

def cria_df_orgao(path):
    files = list_files(path)
    df_orgao = pd.DataFrame()
    for f in files:
        if '.csv' in f:
            df_mes = pd.read_csv(f, sep=';', header=0, decimal=',')
            
            file_name = f.split("_")[1]
            orgao_name = path.split("/")[1]
            
            mes = file_name[4:6]
            ano = file_name[0:4]
            
            df_mes["ANO"] = ano
            df_mes["MES"] = mes
            
            df_orgao= pd.concat([df_orgao, df_mes], ignore_index=True)
            df_orgao["ORGAO"] = orgao_name
    try:
        df_orgao.drop(['Unnamed: 10'], axis=1, inplace=True)
    except:
        print('Sem Coluna Unnamed')
    return df_orgao

def cria_df_geral(path):
    df_geral = pd.DataFrame()
    dirs = list_dirs(path)
    for d in dirs:
        if (str(d) == "csv/PM-ATIVOS" or str(d) == "csv/FUNDAÇÃO VILA OLIMPICA" or str(d)=="csv/PRODAM"):
            continue
        print("Processando diretório:", str(d))
        nome_dir = d.split("/")[1]
        ds_orgao = pd.DataFrame()
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

def main():
    path = 'csv/'
    df_geral = cria_df_geral(path)
    #temporaly display 999 rows
    with pd.option_context('display.max_rows', 999):
        print (df_geral)
#     print(df_geral)
    
main()

