# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import happybase


class SpiderProjectPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='192.168.0.99',
            port=3306,
            user='root',
            password='123456',
            db='spiderteam',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.hbase_conn=happybase.Connection(host='192.168.0.99',port=9090)
    def process_item(self, item, spider):
        self.insert(item)
        return item

    def insert(self,data):
        data=[data['position'],data['company'],data['salary'],
               data['job_info'],data['job_requirements'],data['experience'],
               data['education'],data['work_addr'],data['department'],
               data['company_size'],data['main_business'],data['com_net'],data['net']]
        select_sql='select count(*) from t_recruit'
        self.cursor.execute(select_sql)
        count = self.cursor.fetchone()
        print('--------------',count)
        if count[0]<=50:
            sql='insert into t_recruit(position,company,salary,job_info,' \
                'job_requirements,experience,education,work_addr,department,' \
                'company_size,main_business,com_net)' \
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,data[:-1])
            self.conn.commit()
        else:
            table = self.hbase_conn.table("spiderteam:t_recruit")
            #rowkey 地区 职位 网站 公司 薪资
            rowkey=data[7]+':'+data[0]+':'+data[-1]+':'+data[2]+':'+data[2]
            #职位，公司 薪资任职要求 经验要求 学历要求 公司地点 部门
            table.put(rowkey, {"common:position": data[0],"common:company":data[1],"common:salary":data[2],"common:job_info":data[3],"common:job_requirements":data[4],"common:experience":data[5],"common:education":data[6],"common:work_addr":data[7],"common:department":data[8],"common:company_size":data[9],"common:main_business":data[10],"common:com_net":data[11]})

