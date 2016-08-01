# Hackanation Govhack

This is a sketch to show the potential such a site could have, however, the backend is more mature and our data 
be accessed in JSON format at govhack/prizes.json and govhack/projects.json

## Contents
1. [Requirments](#id-SystemRequirements)
2. [Installing](#id-Installing)
*  [Python](#id-InstallingPython2)
*  [Scrapy](#id-InstallingScrapyWebCrawling)
*  [Django](#Django)
*  [MySQL](#MySQL)
3. [Using Scrapy Standalone](#Standalone\ Scrapy)
*  [JSON Format](#JSON\ Format)

<div id="SystemRequirements"/>
## System Requirements
This system has been tested on ubuntu 16.04, however its built atop tools which should work on ANY unix system, and, with a bit of luck, windows. While python is platform inspecific, we advise using a [virtualbox](https://www.virtualbox.org/) with [ubuntu 16.04](http://releases.ubuntu.com/16.04/) installed to make the installation process much easier.

<div id="Installing"/>
## Installing

<div id="InstallingPython2"/>
### Python2
Python is the lanugage upon which this app is built. You must also install the python2 package manager, pip2.
#### Linux
Ubuntu comes with python2 and pip2 pre-installed, check this with
```
python2
pip2
```
Otherwise, install python2 from your repository or from here: [Python 2](https://www.python.org/downloads/release/python-2712/)

with python2 installed, download the script [get-pip.py](https://bootstrap.pypa.io/get-pip.py) and run it to install pip2
```
wget https://bootstrap.pypa.io/get-pip.py
python2 get-pip.py
```

#### Windows
Python2 and pip2 must be downloaded and installed from [here](https://www.python.org/downloads/release/python-2712/), use the get-pip.py script from above to install pip2. Further instructions are [here](https://pip.pypa.io/en/stable/installing/).

<div id="InstallingScrapyWebCrawling"/>
### Scrapy Web Crawling
Scrapy is the framework used to crawl the govhack hackerspace and prizes websites to find all the prize and team data. This can be done standalone or within the context of this web app.

#### Linux

###### setuptools

First of all, one must install [setuptools](https://pypi.python.org/pypi/setuptools#unix-wget) using either wget or curl (osx)

Wget
```
wget https://bootstrap.pypa.io/ez_setup.py -O - | python2

```
Curl
```
curl https://bootstrap.pypa.io/ez_setup.py -o - | python2
```

###### lxml
Scrapy is built atop the [lxml](http://lxml.de/installation.html) parsing library, as such it must be installed.

We've had success by using the ubuntu repository
```
apt-get install libxml2-dev libxslt-dev python-dev #dependencies
apt-get install python-lxml
```
pip2 can also be used.
```
pip2 install lxml
```

###### OpenSSL
This should come pre-shipped, test this by
```
python2
>>>> import ssl
```
however it can also be accessed from the ubuntu repos
```
apt-get install libssl-dev
```
or check your offical repository. Otherwise it can be downloaded from [here](https://pypi.python.org/pypi/pyOpenSSL)

###### Scrapy
Ubuntu users are encouraged to install from the repo.
```
apt-get install python-scrapy
```
however the scrapy devs also release deb packages for debian systems that are often fresher. See the instructions [here](http://doc.scrapy.org/en/latest/topics/ubuntu.html).

Scrapy is pip2 installable
```
pip2 install scrapy
```
and is usually available from your distros repository.

#### Windows and OSX
Windows and Mac users are encouraged to consult the install instructions [here](http://doc.scrapy.org/en/latest/intro/install.html) however we cannot vouch for them.

### Django
Noah write here

### MySQL
Noah write here if you need to

## Standalone Scrapy
The scrapy crawler is located in the govhack/ directory. It can be used as a standalone program to generate json objects or it can be used in conjunction with the django framework to fill a mysql database.

To use standalone, you must disable the 'pipelines' that write output to a database. This is easily done, from the govhack/ directory, edit the file govhack/settings.py and change the lines that read:
```
    'govhack.prizes_pipeline.PrizesPipeline': 300,
    'govhack.prizecheck_pipeline.PrizeCheckPipeline': 100,
    'govhack.project_pipeline.ProjectsPipeline' : 200,
```
to
```
    #'govhack.prizes_pipeline.PrizesPipeline': 300,
    'govhack.prizecheck_pipeline.PrizeCheckPipeline': 100,
    #'govhack.project_pipeline.ProjectsPipeline' : 200,
```
remember to un-comment out these changes if you want to use the database and website.

It is then a simple matter to re-generate either the prizes.json or projects.json files by calling the scrapy tool from the govhack/ directory.
```
scrapy crawl prizes -o prizes.json
scrapy crawl govhack -o projects.json
```
#### JSON Format
##### prizes.json
prizes.json exports two types of records, a set of records linking prize categories to prizes within them, and a set of records linking prize names to the attributes of that prize such as website, description, value and so on.

Both of these types records are guaranteed to have a boolean entry, 'is_category' which is true if the record describes a category -> prizes mapping, and false if it is a prize_name -> attributes mapping.

an example of a category-> prizes record is:
```
{"is_category": true, "prize_name": ["Community Resilience Hack", "Machine Learning Hack", "Storytelling Hack"], "category": "International Prizes"}

```
and a prize_name->attributes record would look like this:
```
{"is_category": false, "prize_name": "Advance Queensland!", "prize_website": "http://portal.govhack.org/prizes/2016/qld/qld-advance-queensland!.html", "prize_value": "Cash prize(s) up to the value of $1000", "prize_descr": "The most innovative use of Advance Queensland data. Tell a story about the innovation movement in Queensland which is data rich, creative and visually appealing to engage, inspire a broad audience."}
```
##### projects.json
projects.json also exports two types of records, a set of records linking the project name to the attributes of that project. These attributes are for example, are website, team name and local event. The second set of records link the website of a project to the prizes that the project is targeting.

Both of these record types export an is_user boolean which is true if the record describes a project_name->attributes mapping, and false if it describes a project_website->prizes mapping.

an example project_name->attributes record is:
```
{"website": "https://2016.hackerspace.govhack.org/content/hackanation", "is_user": true, "project_name": "\tHackanation", "region": "Australian Capital Territory", "local_event": "Canberra", "team_name": "Alpha Hawk Magnum"}
```
and a corresponding website->prizes mapping record looks like this:
```
{"website": "https://2016.hackerspace.govhack.org/content/hackanation", "is_user": false, "prizes": ["ABS - That thing we all need", "Fresh Data Hack (API\u2019s and Data Services)", "Best Data Wrangling", "Best in ACT", "Best Tertiary Hacker Team"]}
```

#### Pipelines and editing
The scrapy crawlers use pipelines described [here](http://doc.scrapy.org/en/latest/topics/item-pipeline.html) to edit the data before outputting it. You can see three pipelines used in this project in the govhack/govhack/ directory. They are 'project_pipeline.py', which inserts the projects into the database, 'prizes_pipeline.py' which inserts the prizes into the database, and prizecheck_pipeline.py which does some editing of the prizes records to fix spelling mistakes and errors in the data as well as verifying it.
