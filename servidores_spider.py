from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os
import shutil

#### Funções ####
def finaliza_spider(webdriver):
    webdriver.quit()
    quit()

def inicia_web_driver(url):
    # Preferencias do navegador
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.panel.shown', False)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv,text/csv')
    profile.set_preference('browser.helperApps.neverAsk.openFile', 'application/csv,text/csv')
    profile.set_preference('browser.download.dir', '~/git/PAIC/csv/')

    # Criação do Driver
    web_driver = webdriver.Firefox(profile)
    web_driver.profile = profile

    # Acessa a página de remuneração dos servidores
    web_driver.get(url)
    return web_driver


def get_orgaos(web_driver):
    # Clica na caixa de seleção "Orgão"
    select_orgao = web_driver.find_element_by_id("nav_orgaos")
    select_orgao.click()

    # Recupera uma lista de todos orgãos listados
    orgaos = select_orgao.text.split("\n")

    return orgaos

def get_anos(orgao, web_driver):
    # Clica na caixa de seleção "Ano"
    select_ano = web_driver.find_element_by_id("nav_year")
    select_ano.click()

    # Recupera uma lista de todos anos listados
    anos = select_ano.text.split("\n")

    return anos


def cria_pasta(orgao):
    #cria pasta do órgão
    caminho = os.path.join("./csv/", orgao)
    try:
        os.mkdir(caminho)
    except OSError:
        print(caminho + ' já existe.')

def carrega_tabela(orgao, ano, web_driver):
    # Seleciona a opção do select-box "Orgaos"
        se_orgao = Select(web_driver.find_element_by_id("nav_orgaos"))
        se_orgao.select_by_visible_text(orgao)

        # Seleciona a opção do select-box "Ano"
        se_ano = Select(web_driver.find_element_by_id("nav_year"))
        se_ano.select_by_visible_text(ano)

        loading_flag = web_driver.find_element_by_class_name("main_loader").get_attribute("style")
        print("\n[Carregando tabela %s_%s]" %(orgao, ano))
        while ("display: none;" not in loading_flag):
            loading_flag = web_driver.find_element_by_class_name("main_loader").get_attribute("style")
            time.sleep(1)

def download_csv_meses(orgao, ano, web_driver):
    time.sleep(1)
    
    # Recupera uma lista dos elementos <tr> da tabela de meses.
    try:
        meses_tr = web_driver.find_elements_by_xpath(".//*[@class='a-table']/tbody/tr")
    except:
        meses_tr = None

    if (meses_tr != None):
        print("\nRange(2, %d)" %(len(meses_tr)))
        for i in range(2, len(meses_tr)):
            try:
                # Seleciona o mês de acordo como index da lista de meses
                mes_txt = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[1]").text
            except:
                print("Erro ao ler mês")

            # [LOG] "Orgao_Ano_Mes"
            print("\n" + orgao + "_" + ano + "_" + mes_txt, end='')
            try:    
                # Busca os botões de download ".csv" em cada mês da tabela
                btn_csv = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[2]")

                # Realiza o download do arquivo .csv
                btn_csv.click()
                
            except:   
                print(" [CSV não disponível]", end='')

        print()

def download_em_andamento():
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

def move_arquivos(orgao):
    # Move arquivos para a pasta do órgão
    files = os.listdir("./csv")
    for f in files:
        if (f.endswith(".csv")):        
            try:
                shutil.move(os.path.join("./csv/", f), os.path.join("./csv/", orgao))
            except OSError:
                print(f + " duplicado.")

#### MAIN ####

def main():
    b = inicia_web_driver('http://www.transparencia.am.gov.br/pessoal/')
    orgaos = get_orgaos(b)

    for orgao in orgaos:
        cria_pasta(orgao)
        anos = get_anos(orgao, b)

        for ano in anos:
            carrega_tabela(orgao, ano, b)
            download_csv_meses(orgao, ano, b)
        
        time.sleep(2)
        download_em_andamento()
        move_arquivos(orgao)
        
    # Fecha o webdriver
    finaliza_spider(b)

main()