import scrapy
import string
from bs4 import BeautifulSoup

class Enname(scrapy.Spider):
    name = 'enname'
    start_urls = ['http://ename.dict.cn/list/all/' + letter for letter in string.ascii_uppercase]

    def parse(self, response):
        domain = 'http://ename.dict.cn/'
        res = BeautifulSoup(response.body, featuers='lxml')

        for name_ele in res.select('table[class="enname-all"] tr td a'):
            name = name_ele.text