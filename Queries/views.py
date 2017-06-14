from operator import itemgetter


from django.db.models import Count
from django.shortcuts import render
import pandas as pd
from Football.models import *
from collections import Counter
import numpy as np
import itertools

def report1(request):
    data = pd.DataFrame(list(Club.objects.all().values('Name', 'City__Name', 'Year').order_by('Name'
                                                                                              )))
    data = data.rename(columns={"Name": "Название", "City__Name": "Город размещения", "Year": "Год основания"})
    data = data.reindex_axis(['Название', 'Город размещения', 'Год основания'], axis=1)
    return render(request, 'reports/myreport.html',
                  {"title": 'Клубы', "national_pivot_table": data.to_html(), "count": len(data)})


def report2(request):
    data = pd.DataFrame(list(Player.objects.all().filter(Position__Name='Нападающий').values('Position').annotate(
        count_attackers=Count('Position')) \
                             .filter(count_attackers__gt=5) \
                             .values('count_attackers', 'Club__Name').order_by('Club__Name')))
    data = data.rename(columns={"count_attackers": "Количество нападающих", "Club__Name": "Название клуба"})
    data = data.reindex_axis(['Название клуба', 'Количество нападающих'], axis=1)
    return render(request, 'reports/myreport1.html', {"title": 'Список клубов, в которых больше пяти нападающих',
                                                      "national_pivot_table": data.to_html(), "count": len(data),
                                                      "mean": data['Количество нападающих'].mean()})


def report3(request):
    prices = Player.objects.values('Contract_cost').order_by('-Contract_cost')
    data = pd.DataFrame(list(
        Player.objects.values('Name', 'Contract_cost', 'Position__Name').filter(Contract_cost__in=prices[:5]).order_by(
            '-Contract_cost')))
    data = data.rename(columns={"Name": "ФИО футболиста", "Contract_cost": "Стоимость контракта",
                                "Position__Name": "Позиция в команде"})
    data = data.reindex_axis(['ФИО футболиста', 'Стоимость контракта', 'Позиция в команде'], axis=1)
    mean = Counter(data['Позиция в команде']).most_common(1)[0][0]
    prices1 = Player.objects.values('Contract_cost').order_by('Contract_cost')
    data1 = pd.DataFrame(list(
        Player.objects.values('Name', 'Contract_cost', 'Position__Name').filter(Contract_cost__in=prices1[:5]).order_by(
            'Contract_cost')))
    data1 = data1.rename(columns={"Name": "ФИО футболиста", "Contract_cost": "Стоимость контракта",
                                  "Position__Name": "Позиция в команде"})
    data1 = data1.reindex_axis(['ФИО футболиста', 'Стоимость контракта', 'Позиция в команде'], axis=1)
    mean1 = Counter(data1['Позиция в команде']).most_common(1)[0][0]

    return render(request, 'reports/myreport2.html', {"title2": 'Топ 5 ',
                                                      "national_pivot_table": data.to_html(),
                                                      "mean": mean,
                                                      "title1": "Топ 5 низкооплачиваемых футболистов",
                                                      "national_pivot_table1": data1.to_html(),
                                                      "mean1": mean1, "title":'Топ 5 высокооплачеваемых футболистов'})


def diagram(request):
    data = pd.DataFrame(list(Player.objects.all().filter(Position__Name='Нападающий').values('Position').annotate(
        count_attackers=Count('Position')) \
                             .filter(count_attackers__gt=5) \
                             .values('count_attackers', 'Club__Name').order_by('Club__Name')))
    res = [ list(a) for a in zip((data['Club__Name'].values.tolist()), data['count_attackers'].values.tolist())]
    header = [['Клуб', 'Количество нападающих']]
    res = header + res
    return render(request, 'reports/diagram.html', {"data": res})


def histogram(request):
    data = pd.DataFrame(list(Match.objects.filter(Date__year__gt=2012).values('Club__Name').annotate(count_games=Count('Club__Name'))\
            .values('count_games', 'Club__Name').order_by('Club__Name')))
    res = [list(a) for a in zip((data['Club__Name'].values.tolist()), data['count_games'].values.tolist())]
    header = [['Клуб', 'Количество сыгранных игр']]
    res = header + res
    return render(request, 'reports/histogram.html', {"data": res})
