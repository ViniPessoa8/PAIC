#### Imports ####
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from collections import Counter
import time
import os
import shutil
import re

#### Global Variables ####
project_path  = os.path.dirname(os.path.abspath(__file__)).replace('spider', '')
csv_path      = project_path + 'csv/'
log_file_path = project_path + 'log/'
driver_path   = project_path + 'bin/chromedriver' 
pastas        = {}

#### Funções ####
def get_driver_path():
    print(os.name)

def finaliza_spider(webdriver):
    webdriver.quit()
    with get_log_file() as f:        
        f.write("[INFO] Spider finalizada.\n")

def inicia_web_driver(url):
    with get_log_file() as f:
        f.write("[INFO] Iniciando web driver\n")
    options     = webdriver.ChromeOptions()

    # Define as preferências do webdriver
    prefs = { 
        "download.default_directory" : csv_path,
        "directory_upgrade": True
    }
    options.add_argument("disable-popup-blocking")
    options.add_experimental_option("prefs", prefs)
    
    # Instancía o webdriver
    web_driver = webdriver.Chrome(driver_path, chrome_options=options)

    # Acessa a página de remuneração dos servidores
    web_driver.get(url)
    
    return web_driver

# Cria o arquivo de log
def get_log_file():
    if not os.path.isdir(log_file_path):
        os.mkdir(log_file_path)
    
    log_file = open(log_file_path+'/spider_log.txt', 'at')
    return log_file
        

def get_orgaos(web_driver):
    with get_log_file() as f:
        f.write("[INFO] Carregando órgãos\n")
    # Clica na caixa de seleção "Orgão"
    select_orgao = web_driver.find_element_by_id("nav_orgaos")
    select_orgao.click()

    # Recupera uma lista de todos orgãos listados
    orgaos = select_orgao.text.split("\n")

    return orgaos

def get_anos(orgao, web_driver):
    with get_log_file() as f:
        f.write("[INFO] Carregado anos do órgão "+orgao+"\n")
    # Clica na caixa de seleção "Ano"
    select_ano = web_driver.find_element_by_id("nav_year")
    select_ano.click()

    # Recupera uma lista de todos anos listados
    anos = select_ano.text.split("\n")

    return anos


def cria_pasta(orgao):
    # Cria a pasta /csv
    if (not os.path.exists(csv_path)):
        with get_log_file() as f:
            f.write("[INFO] Criando pasta csv/\n")
        os.mkdir(csv_path)

    # Cria pasta do órgão
    caminho = os.path.join(csv_path, orgao)
    if (not os.path.exists(caminho)):
        with get_log_file() as f:
            f.write("[INFO] Criando pasta do órgão "+orgao+"\n")
        os.mkdir(caminho)
    else :
        print(caminho + ": Diretório já existente")

def carrega_tabela(orgao, ano, web_driver):
    with get_log_file() as f:
        f.write("[INFO] Carregando tabela %s_%s\n" %(orgao, ano))
    # Seleciona a opção do select-box "Orgaos"
    se_orgao = Select(web_driver.find_element_by_id("nav_orgaos"))
    se_orgao.select_by_visible_text(orgao)

    # Seleciona a opção do select-box "Ano"
    se_ano = Select(web_driver.find_element_by_id("nav_year"))
    se_ano.select_by_visible_text(ano)

    loading_flag = web_driver.find_element_by_class_name("main_loader").get_attribute("style")
    print("\n[Carregando tabela %s_%s]\n" %(orgao, ano))
    while ("display: none;" not in loading_flag):
        loading_flag = web_driver.find_element_by_class_name("main_loader").get_attribute("style")
    time.sleep(1)

def download_csv_meses(orgao, ano, web_driver):
    # Recupera uma lista dos elementos <tr> da tabela de meses.
    try:
        meses_tr = web_driver.find_elements_by_xpath(".//*[@class='a-table']/tbody/tr")
    except:
        with get_log_file() as f:
            f.write("\n[ERRO] Tabela não encontrada\n")
        meses_tr = None

    if (meses_tr != None):
        for i in range(2, len(meses_tr)+1):
            try:
                # Seleciona o mês de acordo como index da lista de meses
                mes_txt = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[1]").text
            except:
                print("Erro ao ler mês")
                with get_log_file() as f:
                    f.write("\n[BUG] Erro ao ler mês\n")
                exit()

            # [LOG] "Orgao_Ano_Mes"
            print("\n" + orgao + "_" + ano + "_" + mes_txt, end='')
            
            # Busca os botões de download ".csv" em cada mês da tabela
            try:    
                btn_csv = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[2]")
                if (btn_csv.text == '.csv'):
                    # Realiza o download do arquivo .csv
                    with get_log_file() as f:
                        f.write("[INFO] " + orgao + "_" + ano + "_" + mes_txt + "\n")
                    btn_csv.click()
                else:
                    btn_csv = web_driver.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[1]")
                    if (btn_csv.text == '.csv'):
                        with get_log_file() as f:
                            f.write("[INFO] " + orgao + "_" + ano + "_" + mes_txt + "\n")
                        # Realiza o download do arquivo .csv
                        btn_csv.click()
            except:   
                print(" [CSV não disponível]", end='')
                with get_log_file() as f:
                    f.write("[WARN] " + orgao + "_" + ano + "_" + mes_txt + " - CSV indisponível\n")

        print()

def download_em_andamento():
    print("\n[Baixando arquivos]")
    with get_log_file() as f:
        f.write("[INFO] Baixando arquivos\n")
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

# Renomeia os arquivos duplicados de dezembro. 
# "...12(1).csv" -> "...13.csv"
def renomeia_arquivos():
    with get_log_file() as f:
        f.write("[INFO] Renomeando arquivos '12 (1).csv' para '13.csv'\n")
    files = os.listdir(csv_path)
    for f in files:
        if (f.endswith("12 (1).csv")):
            novo_nome = f.replace("12 (1).csv", "13.csv")
            os.rename(csv_path+f, csv_path+novo_nome)

def move_arquivos(orgao):
    with get_log_file() as f:
        f.write("[INFO] Movendo arquivos para a pasta destino\n")
    # Move arquivos para a pasta do órgão
    files = os.listdir(csv_path)
    for f in files:
        if (f.endswith(".csv")):        
            try:
                org_num = re.split("_", f)
                if org_num[0] in pastas.keys():
                    shutil.move(os.path.join(csv_path, f), os.path.join(csv_path, pastas[org_num[0]]))
            except OSError:
                with get_log_file() as f:
                    f.write("\n[ERRO] arquivo duplicado:" + f + "\n")
                print(f + " duplicado.")

# Verifica se a pasta de um órgão já está mapeada
def verif_pasta(orgao):
    if orgao in pastas.values():
        return True
    else:
        return False

# Retorna o item mais frequente de uma lista
def mais_freq(L):
    x = Counter(L)
    return x.most_common(1)[0][0]

# Mapeia o código do arquivo com a pasta do respectivo órgão.
# Usa o código mais frequente para determinar o órgão atual.
def mapeia_pasta(orgao):
    files = os.listdir(csv_path)
    lista = []

    if not verif_pasta(orgao):
        for f in files:
            if (f.endswith(".csv")):        
                org_num = re.split("_", f)
                lista.append(org_num[0])
        
        if len(lista) > 0:
            mf = mais_freq(lista)
            pastas[mf] = orgao

# Apaga um diretório e tudo que tem nele
def remove_arquivos(direc):
    if os.path.isdir(direc):
        with get_log_file() as f:
            f.write("[INFO] Removendo arquivos de '"+direc+"'\n")
        shutil.rmtree(direc)

def prepare_log():
    path = log_file_path+'spider_log.txt'
    print(path)

#### MAIN ####
def main():
    prepare_log()
    #remove_arquivos(csv_path)
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
        
        # time.sleep(1)
        download_em_andamento()
        mapeia_pasta(orgao)
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
