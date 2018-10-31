# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymongo
import pymysql


class JobPipeline1(object):
    def open_spider(self, spider):
        # print('打开爬虫', spider)
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', db='job', password='12345678',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            sql = 'insert into jobs (name,company,salary,post_time) VALUES (%s,%s,%s,%s)'
            self.cursor.execute(sql, (item['name'], item['company'], item['salary'], item['post_time']))
            self.conn.commit()
            print('插入成功')
        except Exception as e:
            print(e)
        return item

    def close_spider(self, spider):
        print("关闭爬虫", spider)


class JobPipeline2(object):
    def process_item(self, item, spider):
        # 同时决定该项目是否应该通过管道或被丢弃且不再处理。 -return item or None
        # print('管道2')
        return item


class JobPipeline3(object):
    def process_item(self, item, spider):
        # 同时决定该项目是否应该通过管道或被丢弃且不再处理。 -return item or None
        # print('管道3')
        return item


class JobsMongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['job']
        self.coll = self.db['job_collection']

    def process_item(self, item, spider):
        try:
            self.coll.insert(dict(item))
            print('插入成功')
            return item

        except Exception as e:
            print(str(e))


    def close_spider(self, spider):
        self.client.close()
