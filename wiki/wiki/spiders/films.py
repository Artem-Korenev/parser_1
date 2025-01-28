import scrapy


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/AFI%27s_100_Years...100_Movie"]

    def parse(self, response):
        pass
