from urllib.request import urlopen, urlretrieve, quote
from urllib.parse import urljoin
from bs4 import BeautifulSoup

url = 'http://oilandgas.ky.gov/Pages/ProductionReports.aspx'
u = urlopen(url)
try:
    html = u.read().decode('utf-8')
finally:
    u.close()

soup = BeautifulSoup(html, 'features="lxml"' )
for link in soup.select('div[webpartid] a'):
    href = link.get('href')
    if href.startswith('javascript:'):
        continue
    filename = href.rsplit('/', 1)[-1]
    href = urljoin(url, quote(href))
    try:
        urlretrieve(href, filename)
    except:
        print('failed to download')