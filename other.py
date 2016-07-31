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
p = Projects(name="http:...",region="Test",event="Test",team_name="..",website="100$3")
p.save()

#add prize to project
#p = Projects[0] # or is it Projects.objects[0]
#p.prizes.add(Prizes[0])

