#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 20:29
# @Author  : ZJ
# @Site    :
# @File    : tongzhi_spider.py 智通网
# @Software: PyCharm
import json

import scrapy
from lxml import etree

from ..items import SpiderProjectItem


class ZhitongSpider(scrapy.Spider):
    page=1
    name='zt'
    page_list=[]
    def start_requests(self):
        # 城市
        city_list = ['14030000', '11000000', '10000000', '14020000']
        # 职位
        job_list = ['爬虫', '大数据', 'AI', 'python web']
        for city in city_list:
            for job in job_list:
                print(city,job)
                url = 'http://www.job5156.com/s/result/kt0_kw-'+job+'_wl'+city+'/'
                yield scrapy.Request(url)

    def parse(self,rep):
        html = etree.HTML(rep.text)
        job_list = html.xpath('//input[@id="keyword1"]/@value')
        job='大数据'
        if job_list:
            job = job_list[0]
        city_list = html.xpath('//input[@id="id_searchCity"]/@value')
        city='14030000'
        if city_list:
            city = city_list[0]
        page = html.xpath('//p[@class="load_more "]/text()')
        print('page',page)
        if page:
            page = ''.join(page)
            if '加载更多结果' in page:
                print('判断是否有第二页')
                ajax_url = 'http://www.job5156.com/s/result/ajax.json?keyword='+job+'&locationList='+city+'&pageNo=2'
                yield scrapy.Request(ajax_url,callback=self.parse1)
        detail_url=html.xpath('//div[@class="col_0 pos_main_msg"]/p/a/@href')
        for i in detail_url:
            yield scrapy.Request(i,callback=self.parse2)
    def parse1(self,rep):
        print('进入第二页')
        datas = json.loads(rep.text)
        page_size=datas['page']['context']['pageSize']
        job = datas['searchPosForm']['keyword']
        city = datas['searchPosForm']['locationList'][0]
        print('-------',job,city)
        index=2
        while 1:
            print(index,page_size)
            if index>page_size:
                break
            ajax_url = 'http://www.job5156.com/s/result/ajax.json?keyword=' + job + '&locationList=' + str(city) + '&pageNo='+str(index)
            yield scrapy.Request(ajax_url,callback=self.parse3)
            index+=1
    def parse2(self,rep):
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
            com_net=html.xpath('//a[@class="com_name"]/@href')[0]
            position = html.xpath('//h1[@class="pos_name"]/text()')[0]
            salary=html.xpath('//div[@class="line_1"]/span/text()')[0]
            company=html.xpath('//a[@class="com_name"]/text()')[0]
            yaoqiu_list=html.xpath('//ul[@class="requirements"]/li/p/text()')
            education=yaoqiu_list[0]#学历
            experience=yaoqiu_list[1]#经验
            work_addr=yaoqiu_list[2]#工作地点
            company_size=html.xpath('//span[@class="prop_value"]/text()')[0]#公司规模
            job_descrip=''.join(html.xpath('//div[@class="pos_describle_content"]/pre/text()'))
            if '任职要求'in job_descrip and '职责描述' in job_descrip or '工作职责' in job_descrip and '职责要求' in job_descrip :
                if '职责要求' in job_descrip:
                    job_list = job_descrip.split('职责要求')
                elif '任职要求' in job_descrip:
                    job_list = job_descrip.split('任职要求')
                job_info = job_list[0]
                job_requirements = job_list[1]
            elif '职责描述' in job_descrip and '任职要求' not in job_descrip or '工作职责' in job_descrip and '职责需求' not in job_descrip:
                job_info = job_descrip
            elif '职责描述' not in job_descrip and '任职要求' in job_descrip or '工作职责' not in job_descrip and '职责需求' in job_descrip:
                job_requirements = job_descrip
            else:
                job_info = job_descrip
            main_business=html.xpath('//a[@class="prop_value"]/text()')[0]#主营业务
            print('detail_data',position,salary,work_addr)
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
            item['com_net'] = 'http://www.job5156.com'+com_net
            item['net'] = '智通网'
            return item
        except:
            pass
    #解析异步请求
    def parse3(self,rep):
        datas=json.loads(rep.text)
        detail_urls=datas['page']['items']
        for url in detail_urls:
            yield scrapy.Request('http://www.job5156.com'+url['posDetailUrl'],callback=self.parse2)

