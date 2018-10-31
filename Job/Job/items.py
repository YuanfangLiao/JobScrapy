# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    place = scrapy.Field()
    salary = scrapy.Field()
    post_time = scrapy.Field()
    href = scrapy.Field()
    job_info = scrapy.Field()
