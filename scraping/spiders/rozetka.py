import scrapy
from scrapy import Item
from scrapy.loader import ItemLoader
from scraping.items import ProductItem


class RozetkaSpider(scrapy.Spider):
    name = "rozetka"
    allowed_domains = ["rozetka.com.ua"]
    start_urls = ["https://rozetka.com.ua/ua/notebooks/c80004/"]

    def parse(self, response):
        pages_urls = [f'{response.url}page={i}/' for i in range(1, 101)]
        for page in pages_urls:
            yield response.follow(page, callback=self.parse_page)

    def parse_page(self, response):
        product_links = response.css('.tile-title::attr(href)').getall()
        for product in product_links:
            yield response.follow(product, callback=self.parse_product)

    def parse_product(self, response):
        loader = ItemLoader(item=ProductItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_css('availability', '.product-price__item::text')
        loader.add_css('old_price', '.product-price__small::text')
        loader.add_css('price', '.product-price__big::text')
        loader.add_css('images', '.simple-slider__item img::attr(src)')
        loader.add_value('url', response.url)
        yield response.follow(
            f'{response.url}characteristics/',
            callback=self.parse_characteristics,
            meta={'loader': loader}
        )

    def parse_characteristics(self, response):
        loader = response.meta['loader']
        characteristics = response.css('.characteristics-full__item')
        char_data = {}
        for row in characteristics:
            name = row.css('.label span::text').get()
            value = row.css('.value span::text').get()
            if name and value:
                char_data[name.strip()] = value.strip()

        loader.add_value('characteristics', char_data)
        yield loader.load_item()

