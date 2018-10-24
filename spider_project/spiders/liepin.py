#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 20:59
# @Author  : ZJ
# @Site    : 
# @File    : liepin.py 猎聘网
# @Software: PyCharm
import scrapy
import json

import time
from lxml import etree

from ..items import SpiderProjectItem


class LiepinSpider(scrapy.Spider):
    name='lp'
    def start_requests(self):

        city_list=['010','020','050020','050090']
        job_list = ['爬虫','大数据','AI','python web']
        for city in city_list:
            for job in job_list:
                url = 'https://www.liepin.com/zhaopin/?dqs=' + city + '&key=' + job
                yield scrapy.Request(url)
    #获取详情页url 查看当前页是否有下一页 如果有 则获取下一页链接 调用当前解析器解析
    def parse(self, response):
        html = etree.HTML(response.text)
        next_page=html.xpath('//a[text()="下一页"]/@href')
        if next_page:
            next_page = 'https://www.liepin.com'+next_page[0]
            yield scrapy.Request(next_page)
        detail_url=html.xpath('//h3/a/@href')
        for url in detail_url:
            if  not url.startswith('http'):
                url = 'https://www.liepin.com'+url
            yield scrapy.Request(url,callback=self.parse1)
    #解析详情页 获取数据
    def parse1(self,rep):
        html = etree.HTML(rep.text)
        position=''
        salary=''
        company=''
        experience=''
        education=''
        work_addr=''
        company_size=''
        job_info=''
        main_business=''
        com_net=''
        department=''
        job_requirements=''
        try:
            com_net=html.xpath('//h3/a/@href')[0]
        except:
            pass
        position = html.xpath('//h1/text()')[0]#职位
        salary=html.xpath('//p[@class="job-item-title"]/text()')
        if salary:
            salary = salary[0]#薪资job-main-title
        else:
            salary = html.xpath('//p[@class="job-main-title"]/text()')[0]

        company=html.xpath('//h3/a/text()')
        if company:
            company = company[0]#公司
        else:
            company = html.xpath('//h3/text()')[0]
        yaoqiu_list=html.xpath('//div[@class="job-qualifications"]/span/text()')
        if yaoqiu_list:
            education=yaoqiu_list[0]#学历
            experience=yaoqiu_list[1]#经验
        else:
            yaoqiu_list = html.xpath('//div[@class="resume clearfix"]/span/text()')
            education = yaoqiu_list[0]  # 学历
            experience = yaoqiu_list[1]  # 经验
        work_addr=html.xpath('//p[@class="basic-infor"]/span/a/text()')#工作地点
        if work_addr:
            work_addr = work_addr[0]
        else:
            work_addr = html.xpath('//p[@class="basic-infor"]/span/text()')[0]#工作地点
        try:
            company_size=html.xpath('//ul[@class="new-compintro"]/li/text()')[1]#公司规模
        except:
            pass
        job_info=''.join(html.xpath('//div[@class="content content-word"]/text()'))#职位要求
        try:
            main_business=html.xpath('//ul[@class="new-compintro"]/li/text()')[0]#主营业务
        except:
            pass
        try:
            department=html.xpath('//div[@class="job-item main-message"]/div/ul/li/label/text()')[0]
        except:
            pass
        print('detail_data',com_net,position,salary,company,work_addr,education,experience,company_size,job_info,main_business)
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
        item['com_net'] = com_net
        item['net'] = '猎聘网'
        return item


