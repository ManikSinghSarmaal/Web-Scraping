import scrapy
from w3lib.html import remove_tags
from scrapy.selector import Selector
import json
from ..items import SteamItem

base_url = "https://store.steampowered.com/search/results/?query&start={}&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_7000_7&filter=topsellers&infinite=1"

class BestSellingSpider(scrapy.Spider):
    name = "infinite_scroll"
    allowed_domains = ["store.steampowered.com"]
    
    start_urls = [base_url.format(0)]
    
    def remove_html(self, review_summary):
        cleaned_review_summary = ''
        try:
            cleaned_review_summary = remove_tags(review_summary)
        except TypeError:
            cleaned_review_summary = 'No Reviews'
        return cleaned_review_summary
    
    def parse(self, response):
        # Parse the JSON response
        resp = json.loads(response.body)
        
        # Debug: Print the keys of the response to ensure we're getting the correct JSON structure
        print("JSON Keys:", resp.keys())
        
        html = resp.get('results_html')
        data = Selector(text=html)
        games = data.xpath('//a')
        steam_item = SteamItem()
        for game in games:
            steam_item['game_url']= game.xpath("//div[@id='search_resultsRows']/a/@href").get()
            steam_item['img_url']= game.xpath('.//div[@class="col search_capsule"]/img/@src').get()
            steam_item['game_name']= game.xpath('.//span[@class="title"]/text()').get()
            steam_item['release_date']= game.xpath('.//div[@class="col search_released responsive_secondrow"]/text()').get().strip()
            steam_item['final_price']=game.xpath('.//div[contains(@class,"discount_final_price")]/text()').get()
            steam_item['reviews_summary']= self.remove_html(game.xpath('//span[contains(@class,"search_review_summary")]/@data-tooltip-html').get())
                      
            yield steam_item
            
            
        #infinite scrolling
        start = resp.get('start') + 50
        total_count = resp.get('total_count')
        if start < total_count:
            next_page = base_url.format(start)
            yield scrapy.Request(next_page, callback=self.parse)