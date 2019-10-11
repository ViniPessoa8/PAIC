from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os
import shutil

DOWNLOAD_PATH = "~git/PAIC/csv";

#### Funções ####
def finalizaSpider(webdriver):
    webdriver.quit()
    quit()

####  Webdriver ####
# Preferencias do navegador
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.panel.shown', False)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv,text/csv')
profile.set_preference('browser.helperApps.neverAsk.openFile', 'application/csv,text/csv')
profile.set_preference('browser.download.dir', '~/git/PAIC/csv/')

# Criação do Driver
b = webdriver.Firefox(profile)
b.profile = profile

# Acessa a página de remuneração dos servidores
b.get('http://www.transparencia.am.gov.br/pessoal/')

# Clica na caixa de seleção "Orgão"
select_orgao = b.find_element_by_id("nav_orgaos")
select_orgao.click()

# Recupera uma lista de todos orgãos listados
orgaos = select_orgao.text.split("\n")

for orgao in orgaos:
    # Clica na caixa de seleção "Ano"
    select_ano = b.find_element_by_id("nav_year")
    select_ano.click()

    # Recupera uma lista de todos anos listados
    anos = select_ano.text.split("\n")

    #cria pasta do órgão
    caminho = os.path.join("./csv/", orgao)
    try:
        os.mkdir(caminho)
    except OSError as e:
        print(caminho + ' já existe.')

    for ano in anos:
        # Seleciona a opção do select-box "Orgaos"
        se_orgao = Select(b.find_element_by_id("nav_orgaos"))
        se_orgao.select_by_visible_text(orgao)

        # Seleciona a opção do select-box "Ano"
        se_ano = Select(b.find_element_by_id("nav_year"))
        se_ano.select_by_visible_text(ano)

        # intervalo para que a tabela seja carregada
        time.sleep(3)

        # Recupera uma lista dos elementos <tr> da tabela de meses.
        meses_tr = b.find_elements_by_xpath(".//*[@class='a-table']/tbody/tr")
        print ("\n[Debug] len(meses_tr) = "+str(len(meses_tr)))

        for i in range(2, len(meses_tr)):
            print("\n" + str(i) + " ", end='')
            # Seleciona o mês de acordo como index da lista de meses
            mes_txt = b.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[1]").text
            

            try:    
                # [LOG] "Orgao_Ano_Mes"
                print(orgao + "_" + ano + "_" + mes_txt, end='')
                # Busca os botões de download ".csv" em cada mês da tabela
                btn_csv = b.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[2]")

                # Realiza o download do arquivo .csv
                btn_csv.click()
                
            except:   
                print(" - Erro ao ler arquivo", end='')
    
    time.sleep(1)


    # Verifica se há aquivos sendo baixados
    baixando = True
    while (baixando):
        files = os.listdir("./csv")
        safe_move = True
        print("\n[Baixando arquivos]")
        for f in files:
            if (f.endswith(".part")):
                print("\n.part")
                safe_move = False

        if (safe_move):
            baixando = False
        

    # Move arquivos para a pasta do órgão
    
    for f in files:
        if (f.endswith(".csv")):        
            try:
                shutil.move(os.path.join("./csv/", f), os.path.join("./csv/", orgao))
            except:
                print(f + " duplicado.")

# Fecha o webdriver
finalizaSpider(b)
