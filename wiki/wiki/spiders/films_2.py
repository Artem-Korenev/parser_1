import scrapy


class Films2Spider(scrapy.Spider):
    name = "films_2"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/AFI%27s_100_Years...100_Movies"]

    # def parse(self, response):
    #     pass
    def parse(self, response):
        # Извлекаем названия фильмов из таблицы
        rows = response.xpath('//table[@class="wikitable sortable"]//tr')
        for row in rows[1:]:  # Пропускаем заголовок таблицы
            movie_name = row.xpath('.//td[1]//i/a/text()').get()
            if movie_name:
                yield {'title': movie_name}


    def parse(self, response):
        # Извлекаем названия фильмов и их порядковые номера из таблицы
        rows = response.xpath('//table[@class="wikitable sortable"]//tr')
        for index, row in enumerate(rows[1:], start=1):  # Пропускаем заголовок таблицы и начинаем нумерацию с 1
            movie_name = row.xpath('.//td[1]//i/a/text()').get()
            if movie_name:
                yield {
                    'rank': index,
                    'name': movie_name}