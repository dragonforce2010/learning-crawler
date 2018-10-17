# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class YelpPipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect('merchant.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists merchant(name varchar(100), address varchar(100), cell varchar(20), website_url varchar(50))')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        col = ','.join(item.keys())
        placeholders = ','.join(len(item.keys()) * '?')
        sql = 'insert into merchant({}) values({})'
        self.cur.execute(sql.format(col, placeholders),tuple(item.values()))
        return item
