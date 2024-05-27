from typing import Any, Iterable
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Response
from ..items import SubredditItem

class SubReddit(scrapy.Spider):   
    name = 'subreddit_data'
    allowed_domains = ["old.reddit.com"]
    subreddits = ['ipl']
    
    def url_lists(self, subreddits):
        start_urls = []                         
        for subs in subreddits:
            start_urls.append('https://old.reddit.com/r/' + subs + '/')
        return start_urls
    
    def start_requests(self):
        urls = self.url_lists(subreddits=self.subreddits)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'subreddit_url': url})
    
    def parse(self, response):
        blocks = response.xpath('//div[contains(@class,"thing")]')
        for block in blocks:
            item = SubredditItem()
            item["post"] = block.xpath(".//div[@class='top-matter']/p[@class='title']/a/text()").get()
            item["link"] = block.xpath(".//div[@class='top-matter']/p[@class='title']/a/@href").get()
            item['subreddit_url'] = response.meta.get('subreddit_url')
            yield item
            
            # Extract the links for further crawling
            links = block.xpath(".//div[@class='top-matter']/ul/li[@class='first']/a/@href").getall()
            for link in links[:4]:
                yield scrapy.Request(url=link, callback=self.parse_comments, meta={'item': item})
            
    def parse_comments(self, response):
        item = response.meta.get('item')
        item['comments'] = response.xpath("//div[@class='sitetable nestedlisting']/div/div[@class='entry unvoted']/form/div/div/p/text()").getall()
        yield item
