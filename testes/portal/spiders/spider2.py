from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

# page = requests.get('http://www.transparencia.am.gov.br/pessoal/')
# page.raise_for_status()

# Preferencias
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/home/vinicius/git/PAIC/csv/')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv')
profile.set_preference("browser.download.panel.shown", False)

# Acesso do Driver
b = webdriver.Firefox(profile)
b.get('http://www.transparencia.am.gov.br/pessoal/')

select_orgao = b.find_element_by_id("nav_orgaos")
select_orgao.click()
orgaos = select_orgao.text.split("\n");

for orgao in orgaos:
    select_ano = b.find_element_by_id("nav_year")
    select_ano.click()
    anos = select_ano.text.split("\n");
    for ano in anos:


        print(orgao, ano);
        se_orgao = Select(b.find_element_by_id("nav_orgaos"))
        se_ano = Select(b.find_element_by_id("nav_year"))

        se_orgao.select_by_visible_text(orgao)
        se_ano.select_by_visible_text(ano)
        time.sleep(1)

        tabela = b.find_element_by_xpath("//table[@class='a-table']/tbody")
        mes_txt = tabela.find_elements_by_xpath("/td/td")
        for i in mes_txt:
            print(i)

        try:
            btn_csv = b.find_element_by_xpath("//a[contains(.,'.csv')]")
            btn_csv.click()
        except:     
            btn_pdf = b.find_element_by_xpath("//a[contains(.,'.pdf')]")
            btn_pdf.click()

    b.quit()