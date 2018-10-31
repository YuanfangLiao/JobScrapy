"""
1、先找xpath
jobs //*[@id="resultList"]/div[@class="el"]
for job in jobs:
职位 job.xpath('string(.//p[contains(@class,"t1")])')
公司名 job.xpath('string(.//span[@class="t2"])')
工作地点 job.xpath('string(.//span[@class="t3"])')
薪资 job.xpath('string(.//span[@class="t4"])')
发布时间 job.xpath('string(.//span[@class="t5"])')

2、找下一页链接
next_page = response.xpath('//a[text()="下一页"]')

3、判断是否有下一页
if next_page:
    response.follow()

"""
# -*- coding: utf-8 -*-
import scrapy
import re

from Job.items import JobItem


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    place_code = {
        '杭州': '080200',
        '上海': '020000'

    }

    # start_urls = ['https://search.51job.com/list/080200,000000,0000,00,9,99,python,2,1.html']
    def __init__(self, place='上海', kw='python', **kwargs):
        # super().__init__()
        # super().__init__(**kwargs)
        self.kw = kw
        self.place = place
        self.start_urls = [
            'https://search.51job.com/list/{place_code},000000,0000,00,9,99,{kw},2,55.html?lang=c&stype=1&postchannel='
            '0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&'
            'confirmdate=9'.format(place_code=self.place_code[self.place], kw=self.kw)]

    def parse(self, response):
        jobs = response.xpath('//*[@id="resultList"]/div[@class="el"]')
        for job in jobs:
            item = JobItem()

            item['name'] = job.xpath('string(.//p[contains(@class,"t1")])').get().strip()
            item['company'] = job.xpath('string(.//span[@class="t2"])').get().strip()
            item['place'] = job.xpath('string(.//span[@class="t3"])').get().strip()
            item['salary'] = job.xpath('string(.//span[@class="t4"])').get().strip()
            item['post_time'] = job.xpath('string(.//span[@class="t5"])').get().strip()
            item['href'] = job.xpath('.//p[contains(@class,"t1")]/span/a/@href').get()
            # item['job_info'] = \
            info_req = scrapy.Request(item['href'], callback=self.parse_info, dont_filter=True)
            # print('我生成了一条数据')
            # print(item)
            info_req.meta['item'] = item
            yield info_req

        next_page = response.xpath('//a[text()="下一页"]/@href')
        if next_page:
            # print(next_page.get())
            yield response.follow(next_page.get())

    def parse_info(self, response):
        items = response.meta['item']
        res = response.xpath('//div[@class="bmsg job_msg inbox"]/p')
        job_info = []
        # strinfo = re.compile(r"\<.*?\>")
        for i in res:
            # print(i.get().replace('<p>', '').replace('</p>', '').replace('<span>', '').replace('</span>', ''))
            job_info.append(i.get().strip().replace('<p>', '').replace('</p>', '').replace('<span>', '').replace('</span>', ''))
        items['job_info'] = ''.join(job_info)
        print(items['job_info'])
        yield items
