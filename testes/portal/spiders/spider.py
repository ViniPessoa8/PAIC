import scrapy

class TestSpider(scrapy.Spider):
    name = 'teste'
    allowed_domains = ['transparencia.am.gov.br']
    start_urls = [
        'http://www.transparencia.am.gov.br/pessoal/'
    ]
    
    def start_requests(self):
        urls = [
            'http://www.transparencia.am.gov.br/pessoal/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("\n\n\n")
        print(response)
        print("\n\n\n")
        for option in response.xpath('//select[@name="year"]/option/text()'):
            self.log(option)
        # yield options
        
        
