# -*- coding: utf-8 -*-
import scrapy
import sys

class SpecificUser(scrapy.Spider):
    name = 'specific-user'
    allowed_domains = ['shutterstock.com']
    start_urls = ['https://www.shutterstock.com/g/limolida?searchterm=seamless&sort=newest&page=21']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    custom_settings = {'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'}
    page=1

    def parse(self, response):
        items = response.css('a.z_h_g')
        for item in items:
            url_string = item.css('::attr(href)').extract_first()
            url = response.urljoin(url_string)
            yield scrapy.Request(url=url, callback=self.parse_details)
        self.page += 1
        next_page_url = "https://www.shutterstock.com/g/limolida?searchterm=seamless&sort=newest&page=" + str(self.page)
        if (self.page <= 188):
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        img = response.css('img.m_k_g::attr(src)').extract_first()
        #thumb = img.replace('600w', '260nw')
        image_urls = [img]
        yield {
            'id': ''.join(list(filter(str.isdigit, response.css('p.m_b_a::text')[1].extract()))),
            'type': response.css('p.m_b_a > a::text').extract_first().replace('stock ', ''),
            'contributer': response.css('p.oc_B_g > span > a::attr(href)').extract_first().replace('/g/', '').replace('%2B', '+'),
            'categories': response.css('p.m_l_a > span > span > a::text').extract(),
            'description': response.css('h1.m_b_b::text').extract_first(),
            #'description': response.css('h1.m_b_b::text').extract_first().lower().replace('.', ' ').replace(',', ' ').replace('  ', ' '),
            'keywords': response.css('a.b_aF_b::text').extract(),
            'image_urls': image_urls
        }

# scrapy shell https://www.shutterstock.com/search/seamless+pattern -s USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
# scrapy shell https://www.shutterstock.com/image-vector/poppy-red-flowers-seamless-pattern-on-1434812726 -s USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

