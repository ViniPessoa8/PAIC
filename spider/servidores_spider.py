#### Imports ####
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os
import shutil

#### Global Variables ####
project_path = "/home/vini/git/"
csv_path = project_path + "PAIC/csv/"

#### Funções ####
def finaliza_spider(webdriver):
    webdriver.quit()

def inicia_web_driver(url):
    options = webdriver.ChromeOptions()

    # Define as preferências do webdriver
    prefs = { 
        "download.default_directory" : csv_path,
        "directory_upgrade": True
    }
    options.add_argument("disable-popup-blocking")
    options.add_experimental_option("prefs", prefs)
    
    # Instancía o webdriver
    web_driver = webdriver.Chrome(chrome_options=options)

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
    if (not os.path.exists(csv_path)):
        os.mkdir(csv_path)

    caminho = os.path.join(csv_path, orgao)
    if (not os.path.exists(caminho)):
        os.mkdir(caminho)
    else :
        print(caminho + ": Diretório já existente")

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
    
    # Recupera uma lista dos elementos <tr> da tabela de meses.
    try:
        meses_tr = web_driver.find_elements_by_xpath(".//*[@class='a-table']/tbody/tr")
    except:
        meses_tr = None

    if (meses_tr != None):
        for i in range(2, len(meses_tr)+1):
            try:
                # Seleciona o mês de acordo como index da lista de meses
                mes_txt = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[1]").text
            except:
                print("Erro ao ler mês")

            # [LOG] "Orgao_Ano_Mes"
            print("\n" + orgao + "_" + ano + "_" + mes_txt, end='')

            # Busca os botões de download ".csv" em cada mês da tabela
            try:    
                btn_csv = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[2]")
                if (btn_csv.text == '.csv'):
                    # Realiza o download do arquivo .csv
                    btn_csv.click()
                else:
                    btn_csv = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[1]")
                    if (btn_csv.text == '.csv'):
                        # Realiza o download do arquivo .csv
                        btn_csv.click()
            except:   
                print(" [CSV não disponível]", end='')

        print()

def download_em_andamento():
    print("\n[Baixando arquivos]")
    # Verifica se há aquivos sendo baixados
    baixando = True
    while (baixando):
        files = os.listdir(csv_path)
        safe_move = True
        for f in files:
            if (f.endswith(".crdownload")):
                safe_move = False
        if (safe_move):
            baixando = False
            time.sleep(1)


def renomeia_arquivos():
  files = os.listdir(csv_path)
  for f in files:
    if (f.endswith("(1).csv")):
      novo_nome = f[:8] + "13.csv" 
      os.rename(csv_path+f, csv_path+novo_nome)

def move_arquivos(orgao):
    # Move arquivos para a pasta do órgão
    files = os.listdir(csv_path)
    for f in files:
        if (f.endswith(".csv")):        
            try:
                shutil.move(os.path.join(csv_path, f), os.path.join(csv_path, orgao))
            except OSError:
                print(f + " duplicado.")

def remove_arquivos(dir):
    if os.path.isdir(dir):
      shutil.rmtree(dir)

#### MAIN ####

def main():
    remove_arquivos(csv_path)
    b = inicia_web_driver('http://www.transparencia.am.gov.br/pessoal/')
    orgaos = get_orgaos(b)
    
    fim = time.time()
    print(fim - inicio)
    
    for orgao in orgaos:
        cria_pasta(orgao)
        anos = get_anos(orgao, b)

        for ano in anos:
            carrega_tabela(orgao, ano, b)
            download_csv_meses(orgao, ano, b)
            time.sleep(1)
        
        time.sleep(1)
        download_em_andamento()
        renomeia_arquivos()
        move_arquivos(orgao)
        
    # Fecha o webdriver
    finaliza_spider(b)

# Marca o incio do processamento
inicio = time.time()

main()

# Marca o fim do processamento
fim = time.time()

# Printa o tempo decorrido em segundos 
print(fim - inicio)

quit()
