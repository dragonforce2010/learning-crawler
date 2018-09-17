import scrapy
from bs4 import BeautifulSoup
from yelpcrawler.items import MerchantItem

class YelpCrawler(scrapy.Spider):
    name = 'yelp'
    start_urls = ['https://www.yelp.com/search?cflt=contractors&find_loc=1455+Market+St%2C+San+Francisco%2C+CA+94103']

    def parse(self, response):
        domain = 'https://www.yelp.com/'
        res = BeautifulSoup(response.body, features='lxml')
        count = 6
        for merchant in res.select('ul > li[class*="regular-search-result"]'):
            if count <= 0:
                return

            count -= 1
            merchant_name = merchant.select('.indexed-biz-name')[0].text
            merchant_url = domain + merchant.select('.biz-name.js-analytics-click')[0]['href']
            print('[Parse] merchant name: ', merchant_name)
            print('[Parse] merchant url: ', merchant_url)

            yield scrapy.Request(merchant_url, self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.body, features='lxml')
        
        try:
            merchant_name = res.select('.biz-page-title')[0].text.strip()
            merchant_cell = res.select('.biz-phone')[0].text.strip()
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
