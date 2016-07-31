from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from hackanation.models import Projects, Prizes

def index(request):
    context = {}
    return render(request, 'hackanation/index.html', context)

def under_rated_prizes(request):
    loc = request.GET.get('location', '')

    prize_dict = {}
    for prize in Prizes.objects.all():
        if prize.category == loc or loc == '':
            prize_dict[prize] = 0

    for proj in Projects.objects.all():
        for prize in proj.prizes.all():
            if prize.category == loc or loc == '':
                prize_dict[prize] += 1

    sorted_prizes = sorted(prize_dict.items(), key=lambda x : x[1])
    context = {'project_lis': sorted_prizes, "page":"underrated"}
    return render(request, 'hackanation/prizes.html', context)

def most_loved_prizes(request):
    loc = request.GET.get('location', '')

    prize_dict = {}
    for prize in Prizes.objects.all():
        if prize.category == loc or loc == '':
            prize_dict[prize] = 0

    for proj in Projects.objects.all():
        for prize in proj.prizes.all():
            if prize.category == loc or loc == '':
                prize_dict[prize] += 1

    sorted_prizes = sorted(prize_dict.items(), key=lambda x : x[1], reverse=True)
    context = {'project_lis': sorted_prizes, "page":"loved"}
    return render(request, 'hackanation/prizes.html', context)



def most_rewarded_prizes(request):
    loc = request.GET.get('location', '')

    prize_dict = {}
    for prize in Prizes.objects.order_by('value'):
        if prize.category == loc or loc == '':
            prize_dict[prize] = prize.value

    sorted_prizes = sorted(prize_dict.items(), key=lambda x : x[1], reverse=True)
    context = {'project_lis': sorted_prizes, "page":"rewarded"}
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

