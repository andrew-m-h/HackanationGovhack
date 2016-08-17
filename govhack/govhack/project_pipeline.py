# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#def clearner(string):



from django.utils.encoding import smart_str, smart_unicode
def get_attr(item,attr):
    #return smart_str(item[attr])
    r = item[attr]
    if isinstance(r, basestring):
        return r
        #return unicode(r, errors='ignore')
        #return r.decode('unicode').encode('ascii', 'ignore')
    else:
        return r

import hashlib
import sys
sys.path.insert(0, '/home/django/django_project')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'

from django.conf import settings
from hackanation.models import Prizes
from hackanation.models import Projects

def md5(string):
    string = string.split("/")[-1].replace(".html","")
    return hashlib.md5(string).hexdigest()

rename_dict = {
"ABS - That thing we all need"  :  "That thing we all need",
"best innovative hack utilising Statistics NZ data"  :  None,
"Geospatial Prize"  :  "Most Innovative Use Of Location-Based Information Prize",
"Helping small businesses make better decisions"  :  "How can City of Melbourne data be used to help businesses make better decisions?",
"How can we better understand how councils are performing?"  :  None,
"How can we reduce the incidence of dog attacks? / How can we ensure that New Zealanders are excellent dog owners?"  :  None,
"Land Use and Development"  :  "Logan Land Use and Development",
"Melbourne's Ecology"  :  None,
"NZ Best Data Journalism"  :  "Data Journalism 1st",
"NZ Best Open Government"  :  "Open Government 1st",
"Showcase Whanganui"  :  None,
"Student Dropout Rates"  :  "Student Droput Rates",
"Supporing the Best of Brisbane"  :  "Supporting the Best of Brisbane",
"The Northern Agricultural Region Prize"  :  "Sustainable Coastlines Prize",
"The Science Sandpit -  a cutting edge concept"  :  "Create a Cutting Edge Concept - The Science Sandpit!",
"Weather Forecast"  :  "Weather Forecasts",
"Western Australian Entrepeneurial Prize"  :  None,
"Western Australian Solution Prize"  :  None,
"Whanganui community hack"  :  None,
"Fresh Data Hack (API's and Data Services)" : "Fresh Data Hack (APIs and Data Services)",
"International Prize: Community Resilience Hack":"Community Resilience Hack",
"International Prize: Storytelling Hack":"Storytelling Hack",
"International Prize: Machine Learning Hack":"Machine Learning Hack",
}


class ProjectsPipeline(object):

    def process_item(self, item, spider):
        if(spider.name!="govhack"):
            return item

        if(get_attr(item,"is_user")):
            project, created  = Projects.objects.get_or_create(website_hash=md5(item["website"]))

            project.name      = get_attr(item,"project_name")
            project.website   = get_attr(item,"website")
            project.region    = get_attr(item,"region")
            project.event     = get_attr(item,"local_event")
            project.team_name = get_attr(item,"team_name")
            project.save()

        else:
            project = Projects.objects.get(website_hash=md5(item['website']))
            for prize_name in get_attr(item,'prizes'):
                #print("\n\n"+prize_url.split("/")[-1].replace(".html","")+"\n\n")
                #prize = Prizes.objects.get(website_hash=md5(prize_name))
                #print("\n\n"+prize_name+": "+prize_name)
                try:
                    if(prize_name in rename_dict):
                        prize_name = rename_dict[prize_name]
                        if(prize_name==None):
                            break
                    try:
                        prize = Prizes.objects.get(name=prize_name)
    	                project.prizes.add(prize)
                    except:
                        pass

                except Prizes.DoesNotExist:
                    with open("diff.txt","a") as f:
                        try:
                            f.write(n+"\n")
                        except:
                            pass

        return item
