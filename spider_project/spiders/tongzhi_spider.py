#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 20:29
# @Author  : ZJ
# @Site    : 
# @File    : tongzhi_spider.py
# @Software: PyCharm
import scrapy
from lxml import etree
class ZhitongSpider(scrapy.Spider):
    name='zt'
    def start_requests(self):
        url = 'http://www.job5156.com/s/result/kt0_kw-%E7%88%AC%E8%99%AB/'
        #ajax_url = 'http://www.job5156.com/s/result/ajax.json?keyword=%E7%88%AC%E8%99%AB&keywordType=0&posTypeList=&locationList=&taoLabelList=&degreeFrom=&propertyList=&industryList=&sortBy=0&urgentFlag=&maxSalary=&salary=&workyearFrom=&workyearTo=&degreeTo=&pageNo=2'
        yield scrapy.Request(url)
    def parse(self,rep):
        html = etree.HTML(rep.text)
        detail_url=html.xpath('//div[@class="col_0 pos_main_msg"]/p/a/@href')
        print(detail_url)
        for i in detail_url:
            yield scrapy.Request(i,callback=self.parse1)
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
        position = html.xpath('//h1[@class="pos_name"]/text()')[0]
        salary=html.xpath('//div[@class="line_1"]/span/text()')[0]
        company=html.xpath('//a[@class="com_name"]/text()')[0]
        yaoqiu_list=html.xpath('//ul[@class="requirements"]/li/p/text()')
        education=yaoqiu_list[0]#学历
        experience=yaoqiu_list[1]#经验
        work_addr=yaoqiu_list[2]#工作地点
        company_size=html.xpath('//span[@class="prop_value"]/text()')[0]#公司规模
        job_descrip=''.join(html.xpath('//div[@class="pos_describle_content"]/pre/text()'))#工作职责
        if '工作职责' not in  job_info or '职责描述' not in job_info:
            job_requirements = job_info
        elif '职位要求' not in job_info or '任职要求' not in job_info:
            job_info = job_info
        else:
            job_list = job_descrip.split('职位要求') or job_descrip.split('任职要求')

        main_business=html.xpath('//a[@class="prop_value"]/text()')#主营业务
        print(position,salary,company,experience,education,work_addr,company_size,job_info)