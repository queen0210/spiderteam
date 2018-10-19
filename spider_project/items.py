# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class SpiderProjectItem(scrapy.Item):
    # define the fields for your item here like:
    position = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    work_addr = scrapy.Field()
    company_size = scrapy.Field()
    job_info = scrapy.Field()
    main_business = scrapy.Field()
    com_net = scrapy.Field()
    department = scrapy.Field()
    job_requirements = scrapy.Field()
    status = scrapy.Field()
    create_time = scrapy.Field()

