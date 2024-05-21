import scrapy
from scrapy_playwright.page import PageMethod
from inshorts.items import InshortsItem
import re

class InshortSpider(scrapy.Spider):
    name = "inshort"
    allowed_domains = ["inshorts.com"]
    start_urls = ["https://inshorts.com/en/read"]

    custom_settings = {
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': False,  # Run in non-headless mode
        }
    }

    def __init__(self, keywords=None, *args, **kwargs):
        super(InshortSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords.split(',') if keywords else []

    def start_requests(self):
        yield scrapy.Request(
            url="https://inshorts.com/en/read",
            meta={
                "playwright": True,
                "playwright_page_coroutines": [
                    PageMethod("wait_for_load_state", "networkidle"),
                    PageMethod("wait_for_timeout", 10000)  # Wait to ensure all content loads
                ],
                "playwright_context": "default",
                "playwright_context_kwargs": {
                    "viewport": {"width": 1280, "height": 720},
                },
                "playwright_page_kwargs": {
                    "wait_until": "networkidle",
                    "timeout": 60000  # Increase timeout to 60 seconds
                }
            }
        )

    def parse(self, response):
        headlines = response.css('[itemprop=headline]::text').getall()
        news = response.css('[itemprop=articleBody]::text').getall()

        self.log(f'Number of headlines: {len(headlines)}')
        self.log(f'Number of news articles: {len(news)}')
        
        for headline, article in zip(headlines, news):
            print(f"Headline: {headline}")
            print(f"News: {article}\n")

        for headline, article in zip(headlines, news):
            if self.contains_keywords(headline) or self.contains_keywords(article):
                item = InshortsItem()
                item['headline'] = headline
                item['news'] = article
                item['keyword_matches'] = self.extract_matches(headline + " " + article)
                yield item
                
        next_page_url = response.css('')

    def contains_keywords(self, text):
        for keyword in self.keywords:
            if re.search(keyword, text, re.IGNORECASE):
                return True
        return False

    def extract_matches(self, text):
        matches = {}
        for keyword in self.keywords:
            pattern = re.compile(f'.{{0,30}}{keyword}.{{0,30}}', re.IGNORECASE)
            matches[keyword] = pattern.findall(text)
        return matches