# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamItem(scrapy.Item):
    game_url = scrapy.Field()
    img_url = scrapy.Field()
    game_name = scrapy.Field()
    release_date = scrapy.Field()
    reviews_summary = scrapy.Field()
    final_price = scrapy.Field()