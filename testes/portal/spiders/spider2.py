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
profile.set_preference('browser.download.panel.shown', False)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv,text/csv,application/pdf,application/x-pdf')
profile.set_preference('browser.helperApps.neverAsk.openFile', 'application/csv,text/csv,application/pdf,application/x-pdf')
profile.set_preference('browser.download.dir', '/home/vini/git/PAIC/csv/')
profile.set_preference("pdfjs.disabled", 'true')

# Acesso do Driver
b = webdriver.Firefox(profile)
b.get('http://www.transparencia.am.gov.br/pessoal/')

select_orgao = b.find_element_by_id("nav_orgaos")
select_orgao.click()
orgaos = select_orgao.text.split("\n")

for orgao in orgaos:
    select_ano = b.find_element_by_id("nav_year")
    select_ano.click()
    anos = select_ano.text.split("\n")
    for ano in anos:


        se_orgao = Select(b.find_element_by_id("nav_orgaos"))
        se_ano = Select(b.find_element_by_id("nav_year"))

        se_orgao.select_by_visible_text(orgao)
        se_ano.select_by_visible_text(ano)
        time.sleep(1)

        meses_tr = b.find_elements_by_xpath(".//*[@class='a-table']/tbody/tr")
        for i in range(2, len(meses_tr)):
            mes_txt = b.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[1]").text
            print(orgao + "_" + ano + "_", end='')
            print(mes_txt, end='')
            try:    
                btn_csv = b.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[2]")
                print(btn_csv.text)
                btn_csv.click()
            except:     
                btn_pdf = b.find_element_by_xpath(".//*[@class='a-table']/tbody/tr["+str(i)+"]/td[2]/a[1]")
                print(btn_pdf.text)
                btn_pdf.click()

    b.quit()
    break