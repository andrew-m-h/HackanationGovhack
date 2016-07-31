# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from django.utils.encoding import smart_str, smart_unicode
def get_attr(item,attr):
    #return smart_str(item[attr])
    r = item[attr]
    return r

import hashlib
import re
import sys
sys.path.insert(0, '/home/django/django_project')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'

from django.conf import settings
from hackanation.models import Prizes
from hackanation.models import Projects

#create prizes
#p = Prizes(website="http:...2",name="Test",description="Test",category="..",value=100,value_description="100$")
#p.save()

#get prizes
#project_list = Prizes.objects.order_by('name')[:5]
#print(project_list[0].name)

#create project
#p = Projects(name="http:...",region="Test",event="Test",team_name="..",website="100$4")
#p.save()

#add prize to project
#p = Projects[0] # or is it Projects.objects[0]
#p.prizes.add(Prizes[0])


def md5(string):
    string = string.split("/")[-1].replace(".html","")
    return hashlib.md5(string).hexdigest()


class PrizesPipeline(object):
    def __init__(self):
        self.cat_dict = {}
    def process_item(self, item, spider):
        if(spider.name!="prizes"):
            return item

        if(get_attr(item,"is_category")):
            for prize_name in get_attr(item,"prize_name"):
                self.cat_dict[prize_name] = get_attr(item,"category")
        else:
            try:
                 Prizes.objects.get(name=get_attr(item, "prize_name"))
            except Prizes.DoesNotExist:
                value = max(re.findall(r'\d+', get_attr(item,"prize_value").replace(",","")))
                prize, created = Prizes.objects.get_or_create(website_hash=md5(get_attr(item,"prize_website")),value=value)
                prize.name = get_attr(item,"prize_name")
                prize.website = get_attr(item,"prize_website")
                prize.description = get_attr(item,"prize_descr")[:2000].encode("utf-8")
                prize.category = self.cat_dict[get_attr(item,"prize_name")]
                prize.value_description = get_attr(item,"prize_value")
                prize.value = value
                prize.save()

        return item
    def close_spider(self,spider):
        self.cat_dict = None
