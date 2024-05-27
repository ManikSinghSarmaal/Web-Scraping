# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SubredditItem(scrapy.Item):
    post = scrapy.Field()
    link = scrapy.Field()
    comments = scrapy.Field()
    subreddit_url = scrapy.Field()
