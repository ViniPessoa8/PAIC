import scrapy

class TestSpider(scrapy.Spider):
    name = 'Remuneração dos Servidores'
    allowed_domains = ['transparencia.am.gov.br']
    start_urls = [
        'http://www.transparencia.am.gov.br/pessoal/'
    ]
    
    def parse(self, response):
        print(response)
        for option in response.xpath('//select[@id="nav_orgaos"]/option'):
            yield {option}
        
        
