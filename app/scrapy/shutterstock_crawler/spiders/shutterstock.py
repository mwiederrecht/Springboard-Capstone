# -*- coding: utf-8 -*-
import scrapy
import sys

class ShutterstockSpider(scrapy.Spider):
    name = 'shutterstock-spider'
    allowed_domains = ['shutterstock.com']
    start_urls = []
    user_agent = ''
    custom_settings = {'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'}
    page = 1
    numPagesToScrape = 1
    searchTerm = ""

    def __init__(self,
                 start_url='',
                 search_term='',
                 pages_to_scrape=1,
                 starting_page=1,
                 user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                 **kwargs):
        self.start_urls = [start_url]
        self.user_agent = user_agent
        self.page = int(starting_page)
        self.numPagesToScrape = int(pages_to_scrape)
        self.searchTerm = search_term
        super().__init__(**kwargs)

    def parse(self, response):
        items = response.css('a.z_h_81637')
        for item in items:
            url_string = item.css('::attr(href)').extract_first()
            url = response.urljoin(url_string)
            yield scrapy.Request(url=url, callback=self.parse_details, meta={'pageNum':self.page, 'searchTerm':self.searchTerm})
        self.page += 1
        next_page_url = "https://www.shutterstock.com/search/{}?page={}".format(self.searchTerm, str(self.page))
        if (self.page <= self.numPagesToScrape):
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        img = response.css('img.m_r_c4504::attr(src)').extract_first()
        image_urls = [img]
        pageNum = response.meta.get('pageNum')
        yield {
            'id': ''.join(list(filter(str.isdigit, response.css('p.m_b_4dd9d::text')[1].extract()))),
            'pageNum': pageNum,
            'searchTerm': self.searchTerm,
            'type': response.css('p.m_b_4dd9d > a::text').extract_first().replace('stock ', ''),
            'contributer': response.css('p.oc_Q_7bfac > span > a::attr(href)').extract_first().replace('https://www.shutterstock.com/g/', '').replace('%2B', '+'),
            'description': response.css('h1.m_b_d59a1::text').extract_first(),
            'keywords': response.css('a.C_b_8978e::text').extract(),
            'image_urls': image_urls
        }