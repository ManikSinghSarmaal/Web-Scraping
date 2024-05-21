import json
import scrapy

class BusinessNewsSpider(scrapy.Spider):
    name = "businessnews"
    start_urls = [
        "https://inshorts.com/api/en/search/trending_topics/business?page=2",
    ]

    def parse(self, response):
        data = json.loads(response.text)
        for article in data['data']['suggested_news']:
            news_obj = article['news_obj']
            yield {
                'headline': news_obj.get('title'),
                'content': news_obj.get('content'),
                'date': news_obj.get('created_at'),
                'url': news_obj.get('source_url')
            }
        
        total_pages = data['data']['total_page']
        current_page = data['data']['page_num']
        
        if current_page < total_pages:
            next_page = current_page + 1
            next_page_url = f"https://inshorts.com/api/en/search/trending_topics/business?page={next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse_next_pages)

    def parse_next_pages(self, response):
        data = json.loads(response.text)
        for article in data['data']['suggested_news']:
            news_obj = article['news_obj']
            yield {
                'headline': news_obj.get('title'),
                'content': news_obj.get('content'),
                'date': news_obj.get('created_at'),
                'url': news_obj.get('source_url')
            }
        
        total_pages = data['data']['total_page']
        current_page = data['data']['page_num']
        
        if current_page < total_pages:
            next_page = current_page + 1
            next_page_url = f"https://inshorts.com/api/en/search/trending_topics/business?page={next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse_next_pages)
