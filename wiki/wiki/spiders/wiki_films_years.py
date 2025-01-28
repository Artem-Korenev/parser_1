import scrapy
import re

class WikiFilmsYearsSpider(scrapy.Spider):
    name = "wiki_films_years"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_годам"]
    visited_urls = set()

    def parse(self, response):
        # Извлекаем названия гиперссылок и следуем по ним
        for link in response.css('div.mw-category-group a'):
       #     title = link.css('::text').get()
            href = link.css('::attr(href)').get()
            if href:
                full_url = response.urljoin(href)
                if full_url not in self.visited_urls:
                    self.visited_urls.add(full_url)
                    yield response.follow(href, self.parse_link)

    def parse(self, response):
        for link in response.css('div.mw-category-group a'): # переходим по гиперссылкам
            href = link.css('::attr(href)').get()
            if href:
                full_url = response.urljoin(href)
                if full_url not in self.visited_urls: # если не заходили ранее по этой ссылке, то переходим и запоминаем ее
                    self.visited_urls.add(full_url)
                    yield response.follow(href, self.parse)

        infobox = response.xpath('//table[contains(@class, "infobox")]') # Если больше нет ссылок, ищем сводную таблицу на странице со всеми данными

        # aa = response.css('th:contains("Исполнения роли") + td ::text').getall()
        # if aa:

        if infobox:
            title = response.xpath('//h1[@id="firstHeading"]/span/text() | //h1[@id="firstHeading"]/i/text()').getall() #получение названия
            genre = response.css(
            'th:contains("Жанр") + td ::text, '
            'th:contains("Жанры") + td ::text, '
            'th:contains("Техника анимации") + td ::text'
            ).getall() #получение жанра
            genre = self.clean_text(genre)
            director = response.css('th:contains("Режиссёр") + td ::text, th:contains("Режиссёры") + td ::text').getall() #получение продюссера
            director = self.clean_text(director)
            country = response.css('th:contains("Страна") + td ::text, th:contains("Страны") + td ::text').getall() #получение страны
            country = self.clean_text(country)
            year = response.css('th:contains("Год") + td ::text, '
                            'th:contains("Дата выхода") + td ::text, '
                            'th:contains("Премьерный показ") + td ::text, '
                            'th:contains("Публикация") + td ::text').getall() #получение года
            year = self.clean_text(year)
            yield {
                'Название': title,
                'Жанр': genre,
                'Продюссер': director,
                'Страна': country,
                'Год': year
                }
    def clean_text(self, text_list):  # функция для очистки текста
            if not text_list:
                return ''
            text = ' '.join(text_list)
            return re.sub(r'\[.*?\]|\n|\xa0', '', text).strip()