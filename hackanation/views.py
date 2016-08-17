from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from hackanation.models import Projects, Prizes

def index(request):
    context = {}
    return render(request, 'hackanation/index.html', context)


location_map = {
    "International":["International Prizes"],
    "Australia":["Major Category Prizes","Bounty Prizes"],
    "New Zealand":["New Zealand Major Prizes","New Zealand Bounty Prizes"]
}
def get_prizes(loc):
    all_prizes = Prizes.objects.all()
    prizes = []
    for prize in all_prizes:
        if loc=='' or loc=="Everywhere" or loc in location_map and prize.category in location_map[loc] or prize.category==loc:
           prizes.append(prize)
    return prizes

def under_rated_prizes(request):
    loc = request.GET.get('loc', '')

    prize_dict = {}
    prizes = get_prizes(loc)
    for prize in prizes:
        prize_dict[prize] = 0

    for proj in Projects.objects.all():
        for prize in proj.prizes.all():
            if prize in prize_dict:
	        prize_dict[prize] += 1

    sorted_prizes = sorted(prize_dict.items(), key=lambda x : x[1])
    context = {'project_lis': sorted_prizes, "page":"underrated","location":loc}
    return render(request, 'hackanation/prizes.html', context)

def most_loved_prizes(request):
    loc = request.GET.get('loc', '')

    prize_dict = {}
    prizes = get_prizes(loc)
    for prize in prizes:
        prize_dict[prize] = 0

    for proj in Projects.objects.all():
        for prize in proj.prizes.all():
            if prize in prize_dict:
	        prize_dict[prize] += 1

    sorted_prizes = sorted(prize_dict.items(), key=lambda x : x[1], reverse=True)
    context = {'project_lis': sorted_prizes, "page":"loved","location":loc}
    return render(request, 'hackanation/prizes.html', context)



def most_rewarded_prizes(request):
    loc = request.GET.get('loc', '')

    prize_dict = {}
    prizes = get_prizes(loc)

    for prize in prizes:
        prize_dict[prize] = prize.value

    sorted_prizes = sorted(prize_dict.items(), key=lambda x : x[1], reverse=True)
    context = {'project_lis': sorted_prizes, "page":"rewarded","location":loc}
    return render(request, 'hackanation/prizes.html', context)



def prize(request):
    name = request.GET.get('name', '')
    prize = Prizes.objects.filter(name=name)[0]

    lst = []

    for proj in Projects.objects.all():
        if prize in proj.prizes.all():
            lst.append(proj)

    context = {'prize': prize, 'projects':lst}
    return render(request, 'hackanation/prize.html', context)

def search(request):
    context = {}
    return render(request, 'hackanation/search.html', context)


def data(request):
    context = {}
    return render(request, 'hackanation/data.html', context)
