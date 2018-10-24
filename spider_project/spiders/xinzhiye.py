#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 14:17
# @Author  : ZJ
# @Site    : 
# @File    : xinzhiye.py 新职业网
# @Software: PyCharm
import json

import time
from lxml import etree

import scrapy

from ..items import SpiderProjectItem


class NewjobSpider(scrapy.Spider):
    name='nj'
    def start_requests(self):
        city_list=['11','31','440100','440300']
        job_list=['爬虫','大数据','AI','python web']
        for city in city_list:
            for job in job_list:
                url='https://job.ncss.org.cn/student/jobs/jobslist/ajax/?jobType=&areaCode='+city+'&jobName='+job+'&monthPay=&industrySectors=&property=&categoryCode=&limit=10&_=1540102372921&offset=1'
                yield scrapy.Request(url,callback=self.parse)
                time.sleep(3)
    def parse(self, response):
        url=str(response.url).strip().split('offset=')[0]
        datas = json.loads(response.text)
        # 当前页
        offset = datas['data']['pagenation']['offset']
        # #总页数pagenation
        total = datas['data']['pagenation']['total']
        if offset < total :
            offset=str(int(offset)+1)
            print(offset, total)
            url = url+'offset='+offset
            yield scrapy.Request(url,callback=self.parse)
        for data in datas['data']['list']:
            url='https://job.ncss.org.cn/student/jobs/'+data['jobId']+'/detail.html'
            yield scrapy.Request(url,callback=self.parse1)
            time.sleep(3)
    def parse1(self,rep):
        html = etree.HTML(rep.text)
        position = ''
        salary = ''
        company = ''
        experience = ''
        education = ''
        work_addr = ''
        company_size = ''
        job_info = ''
        main_business = ''
        com_net = ''
        department = ''
        job_requirements = ''
        wang=html.xpath('//span[@class="iconfont icon-wangzhi"]')
        try:
            if wang:
                com_net=wang[0].xpath('./../../span/text()')[2]
        except:
            pass
        position = html.xpath('//li[@class="job-title"]/text()')[0]  # 职位
        salary = html.xpath('//ul[@class="salary clearfix"]/li/span/text()')[0]
        company = html.xpath('//p[@id="corpName"]/span/text()')[0]
        education = ''.join(html.xpath('//ul[@class="salary clearfix"]/li/span/text()')[1].split())
        work_addr = html.xpath('//div[@class="site-tag"]/text()')[0]  # 工作地点
        try:
            size = html.xpath('//span[@class="iconfont icon-guim"]')
            if size:
                company_size = size[0].xpath('./../../span[@class="show fr"]/text()')[0]

        except:
            pass
        job_info = ''.join(''.join(html.xpath('//pre[@class="mainContent mainContent"]/text()')).split())  # 职位要求
        if not job_info:
            job_info=''.join(''.join(html.xpath('//div[@class="mainContent mainContent-geshi"]/text()')).split())
        try:
            main_business = html.xpath('//span[@id="mainindustries"]/text()')[0]

        except:
            pass
        print('detail_data', com_net, position, salary, company, work_addr, education, experience, company_size,
              job_info, main_business)
        item = SpiderProjectItem()
        item['position'] = position
        item['company'] = company
        item['salary'] = salary
        item['job_info'] = job_info
        item['job_requirements'] = job_requirements
        item['experience'] = experience
        item['education'] = education
        item['work_addr'] = work_addr
        item['department'] = department
        item['company_size'] = company_size
        item['main_business'] = main_business
        item['com_net']=com_net
        item['net']='新职业'
        return item
