import scrapy
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from yelpcrawler.items import MerchantItem

class YelpCrawler(scrapy.Spider):
    name = 'yelp'

    def __init__(self):
        self.domain = 'https://www.yelp.com/'
        self.start_urls = self.gen_start_urls()

    def parse(self, response):
        res = BeautifulSoup(response.body, features='lxml')
        for merchant in res.select('ul > li[class*="regular-search-result"]'):
            merchant_name = merchant.select('.indexed-biz-name')[0].text
            merchant_url = self.domain + merchant.select('.biz-name.js-analytics-click')[0]['href']
            print('[Parse] merchant name: ', merchant_name)
            print('[Parse] merchant url: ', merchant_url)

            yield scrapy.Request(merchant_url, self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.body, features='lxml')
        
        try:
            merchant_name = res.select('.biz-page-title')[0].text.strip()
            merchant_cell = res.select('.biz-phone')[0].text.strip().replace(' ', '')
            merchant_website_url = res.select('.biz-website a')[0].text.strip()
            merchant_address = res.select('address')[0].text.strip()

            merchantItem = MerchantItem()
            merchantItem['name'] = merchant_name
            merchantItem['cell'] = merchant_cell
            merchantItem['website_url'] = merchant_website_url
            merchantItem['address'] = merchant_address

            return merchantItem
        except:
            return None

    def gen_start_urls(self):
        start_urls = []
        base_url = 'https://www.yelp.com/search?find_loc='
        city_names = self.get_city_names()

        for target_city_name in city_names:
            target_city_url = base_url + target_city_name.replace(' ', '+')
            start_urls.append(target_city_url)

        return start_urls

    def get_city_names(self):
        cities_page_url = 'https://www.yelp.com/city'
        city_names = []

        city_page_html = urlopen(cities_page_url).read().decode('utf-8')
        soup = BeautifulSoup(city_page_html, features='lxml')
        city_href_links = soup.find_all('a', {'href': re.compile('/city/.*?')})
        for link in city_href_links:
            city_names.append(link.get_text())

        return city_names
