import scrapy
from scrapy.http.request import Request

URL = 'http://rraae.org.ec/Search/Results?type=AllFields'
URL2 = '&page=%d'
pagina_inicial = 0
pagina_final = 5

class rraae(scrapy.Spider):
    name = 'rraae'
    start_urls = [URL + (URL2 % pagina_inicial)]

    def parse_pagina(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        if extract_with_css('tr:nth-child(11) th:nth-child(1)::text') == 'institution':
            institucion = extract_with_css('tr:nth-child(11) td:nth-child(2)::text')
        else:
            institucion = ""

        if extract_with_css('tr:nth-child(16) th:nth-child(1)::text') == 'author':
            author = extract_with_css('tr:nth-child(16) td:nth-child(2)::text')
        else:
            author = ""

        if extract_with_css('tr:nth-child(2) th:nth-child(1)::text') == 'Format:':
            publishDate = extract_with_css('td:nth-child(2) > span:nth-child(2)::text')
            languaje = extract_with_css('tr:nth-child(3) > td:nth-child(2)::text')

            if extract_with_css('tr:nth-child(25) > th:nth-child(1)::text') == 'topic':
                topic = response.css('tr:nth-child(25) > td:nth-child(2)::text').extract()
                topic = [x.strip('\n') for x in topic]
                topic = [x.strip(' ') for x in topic]
                topic = [x for x in topic if x]
            else:
                topic = ""

            autores_sec = ""
        else:
            publishDate = extract_with_css('td:nth-child(2) > span:nth-child(2)::text')
            languaje = extract_with_css('tr:nth-child(4) > td:nth-child(2)::text')

            if extract_with_css('tr:nth-child(27) > th:nth-child(1)::text') == 'topic':
                topic = response.css('tr:nth-child(27) > td:nth-child(2)::text').extract()
                topic = [x.strip('\n') for x in topic]
                topic = [x.strip(' ') for x in topic]
                topic = [x for x in topic if x]
            else:
                topic = ""

            autores_sec = response.css('tr:nth-child(19) > td:nth-child(2)::text').extract()
            autores_sec = [x.strip('\n') for x in autores_sec]
            autores_sec = [x.strip(' ') for x in autores_sec]
            autores_sec = [x for x in autores_sec if x]

        if extract_with_css('tr:nth-child(13) th:nth-child(1)::text') == 'format':
            format = extract_with_css('tr:nth-child(13) td:nth-child(2)::text')
        else:
            format = ""

        if extract_with_css('tr:nth-child(15) th:nth-child(1)::text') == 'eu_rights':
            eu_rights = extract_with_css('tr:nth-child(15) td:nth-child(2)::text')
        else:
            eu_rights = ""

        yield {
            'titulo': extract_with_css('h3::text'),
            'institucion': institucion,
            'autor': author,
            'autor_sec': autores_sec,
            'fecha_pub': publishDate,
            'formato': format,
            'subjects': topic,
            'idioma': languaje,
            'eu_rights': eu_rights,
        }

    def parse(self, response):
        for href in response.css("a.title::attr(href)"):
            href = href.extract()
            yield response.follow(href+'/Details#tabnav', self.parse_pagina)

        for self.page_number in range(pagina_inicial+1,pagina_final+1):
            yield Request(URL + (URL2 % self.page_number))
