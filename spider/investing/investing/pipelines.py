# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import datetime

month_map = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
}


class InvestingPipeline(object):
    def process_item(self, item, spider):
        return item


class WriteCSVPipeline(object):
    def __init__(self):
        self.code_dict = dict()

    def _add_code(self, code):
        filename = '../data/news/news_%s.csv'%(code)
        self.code_dict[code] = dict()
        self.code_dict[code]['file'] = open(filename, 'w', newline='')
        self.code_dict[code]['csv'] = csv.writer(self.code_dict[code]['file'])
        self.code_dict[code]['csv'].writerow(['code', 'company', 'date', 'text'])


    def _transform_time(self, raw_time):
        raw_time = str(raw_time)
        time = None
        if raw_time.find('ago') != -1:
            # print(raw_time)
            time = datetime.datetime.now()-datetime.timedelta(hours=13)
        else:
            pieces = raw_time.replace(',', ' ').split()
            y = pieces[2]
            m = month_map[pieces[0]]
            d = pieces[1]
            time = datetime.datetime(year=int(y), month=int(m), day=int(d))
        return time.strftime("%Y-%m-%d")

    def process_item(self, item, spider):
        company = str(item['company'])
        time = self._transform_time(item['time'])
        text = str(item['text'])
        code = item['code']
        row = [code, company, time, text]

        if code not in self.code_dict:
            self._add_code(code)
        self.code_dict[code]['csv'].writerow(row)

        return item

    def close_spider(self, spider):
        for code in self.code_dict:
            self.code_dict[code]['file'].close()

