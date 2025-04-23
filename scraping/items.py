# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from twisted.web.html import output


class ScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def extract_price(value):
    digits = re.sub(r"[^\d]", '', value)
    return int(digits) if digits else None


class ProductItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    availability = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    old_price = scrapy.Field(
        input_processor=MapCompose(extract_price),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(extract_price),
        output_processor=TakeFirst()
    )
    images = scrapy.Field()
    url = scrapy.Field()
    characteristics = scrapy.Field()
