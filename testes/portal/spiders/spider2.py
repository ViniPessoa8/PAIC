from bs4 import BeautifulSoup
import requests
from selenium import webdriver
b = webdriver.Firefox()
page = requests.get('http://www.transparencia.am.gov.br/wp-admin/admin-ajax.php?action=get_meses_docs&ano=2018&orgao_id=93')
page.raise_for_status()

opcoes = b.find_element_by_id("nav_orgaos")
for opcao in opcoes:
    print(opcao)

soup = BeautifulSoup(page.text, 'html.parser')

select_orgao = soup.select('#nav_orgaos')

print(select_orgao)